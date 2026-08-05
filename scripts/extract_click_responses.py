"""
extract_click_responses.py — Derive each participant's clicked answer per
visual-search task directly from the raw Tobii Pro Lab Data export TSV.

Replaces manual response entry (data_collection_manual.md Part C) for the
new 13-task stimulus set: reads DATAEXPORT_TSV, finds each participant's
mouse clicks, attributes them to a task interval and to whichever AOI the
click landed in, and cross-references answer_key.json for correctness.

How a click is resolved (verified against the real export, not assumed):
  - A left mouse-down is two adjacent physical rows sharing the same
    "Recording timestamp": one row has Event="MouseEvent" / Event value=
    "Down, Left" (Sensor blank); the very next row has Sensor="Mouse" and
    carries "Mouse position X/Y" plus the "AOI hit [...]" columns for that
    instant. We never use "Up, Left" (the release can land after the next
    stimulus has already started).
  - "ImageStimulusStart"/"ImageStimulusEnd" rows carry the stimulus name
    directly in "Event value" and bracket each task's on-screen interval.
  - Rather than re-deriving point-in-rectangle geometry against the
    .aois files, we read the correct AOI straight off Tobii's own
    precomputed "AOI hit [task - aoi]" boolean columns (same convention
    notebook 02 already relies on).

The file is ~3GB / 4.5M rows, so it is streamed in chunks with a narrow
`usecols` (metadata columns + only the AOI hit columns for our 13 tasks),
keeping only the sparse Event/Sensor=Mouse rows that matter and carrying
at most one boundary row across chunks so a MouseEvent row that lands at
the very end of a chunk still pairs correctly with its companion row at
the start of the next chunk.

Outputs:
  - data/processed/click_events_detailed.csv  (one row per click event)
  - data/raw/student_responses.csv            (one row per participant,
    wide `{task}_response` columns — overwrites the existing file)
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import (
    DATAEXPORT_TSV, DATA_PROCESSED, DATA_RAW,
    AOI_MAP_JSON, ANSWER_KEY_JSON, TASKS,
    ExportCols, MouseEventValue, StimulusEvent, MOUSE_EVENT, MOUSE_SENSOR,
)

CHUNKSIZE = 300_000
CLICK_EVENTS_CSV = DATA_PROCESSED / "click_events_detailed.csv"
STUDENT_RESPONSES_CSV = DATA_RAW / "student_responses.csv"


def build_aoi_hit_col(task: str, aoi: str) -> str:
    """Same naming convention as notebook 02: 'AOI hit [{task} - {aoi}]'."""
    return f"AOI hit [{task} - {aoi}]"


def load_task_aois() -> dict:
    """task -> list of (aoi_name, aoi_hit_column) for every AOI in that task."""
    aoi_map = json.loads(AOI_MAP_JSON.read_text())
    task_aois = {}
    for task in TASKS:
        entry = aoi_map[task]
        aois = [entry["correct_aoi"], *entry["distractor_aois"]]
        task_aois[task] = [(aoi, build_aoi_hit_col(task, aoi)) for aoi in aois]
    return task_aois


def resolve_usecols(task_aois: dict) -> list:
    """Intersect our expected columns with what's actually in the file header."""
    header = pd.read_csv(DATAEXPORT_TSV, sep="\t", nrows=0).columns
    header_set = set(header)

    metadata_cols = [
        ExportCols.RECORDING_TIMESTAMP,
        ExportCols.PARTICIPANT_NAME,
        ExportCols.RECORDING_NAME,
        ExportCols.SENSOR,
        ExportCols.EVENT,
        ExportCols.EVENT_VALUE,
        ExportCols.MOUSE_X,
        ExportCols.MOUSE_Y,
    ]
    aoi_hit_cols = [col for aois in task_aois.values() for _, col in aois]

    missing_aoi_cols = [c for c in aoi_hit_cols if c not in header_set]
    if missing_aoi_cols:
        print(f"WARNING: {len(missing_aoi_cols)} configured AOI hit columns "
              f"not found in the TSV header, e.g. {missing_aoi_cols[:5]}")

    usecols = [c for c in metadata_cols if c in header_set]
    usecols += [c for c in aoi_hit_cols if c in header_set]
    return usecols


def process_chunks(usecols: list, task_aois: dict):
    """
    Single streaming pass over the TSV. Returns (clicks, intervals):
      clicks    — list of dicts, one per resolved MouseEvent/Down,Left click
      intervals — list of dicts, one per ImageStimulusStart/End event
    """
    clicks = []
    intervals = []
    carry = None  # last row of the previous chunk, if it's an unresolved click

    reader = pd.read_csv(
        DATAEXPORT_TSV, sep="\t", usecols=usecols, chunksize=CHUNKSIZE,
        dtype=str, low_memory=False,
    )

    for chunk_num, chunk in enumerate(reader):
        if carry is not None:
            chunk = pd.concat([carry, chunk], ignore_index=True)
            carry = None

        event = chunk[ExportCols.EVENT]
        event_value = chunk[ExportCols.EVENT_VALUE]

        # Stimulus interval boundaries: Event value already holds the task name.
        interval_mask = event.isin([StimulusEvent.START, StimulusEvent.END])
        for _, row in chunk.loc[interval_mask].iterrows():
            intervals.append({
                "participant_id": row[ExportCols.PARTICIPANT_NAME],
                "recording_name": row[ExportCols.RECORDING_NAME],
                "task": row[ExportCols.EVENT_VALUE],
                "is_start": row[ExportCols.EVENT] == StimulusEvent.START,
                "timestamp": row[ExportCols.RECORDING_TIMESTAMP],
            })

        # Left mouse-down events: pair each with the very next row (same
        # Recording timestamp, Sensor="Mouse") to get coordinates + AOI hits.
        down_mask = (event == MOUSE_EVENT) & (event_value == MouseEventValue.DOWN_LEFT)
        down_positions = np.flatnonzero(down_mask.to_numpy())

        last_idx = len(chunk) - 1
        for pos in down_positions:
            if pos == last_idx:
                # Companion row isn't in this chunk yet — carry forward.
                carry = chunk.iloc[[pos]]
                continue

            down_row = chunk.iloc[pos]
            companion = chunk.iloc[pos + 1]

            if (companion[ExportCols.SENSOR] != MOUSE_SENSOR
                    or companion[ExportCols.RECORDING_TIMESTAMP] != down_row[ExportCols.RECORDING_TIMESTAMP]):
                # Not the expected adjacency — skip rather than guess.
                continue

            clicks.append({
                "participant_id": down_row[ExportCols.PARTICIPANT_NAME],
                "recording_name": down_row[ExportCols.RECORDING_NAME],
                "timestamp": down_row[ExportCols.RECORDING_TIMESTAMP],
                "mouse_x": companion[ExportCols.MOUSE_X],
                "mouse_y": companion[ExportCols.MOUSE_Y],
                "_companion_row": companion,
            })

        print(f"  chunk {chunk_num}: {len(chunk)} rows, "
              f"{len(intervals)} intervals so far, {len(clicks)} clicks so far")

    return clicks, intervals


def resolve_selected_aoi(companion_row: pd.Series, task: str, task_aois: dict) -> str:
    """Which AOI hit column (if any) is '1' on the click's companion row."""
    hits = []
    for aoi_name, col in task_aois.get(task, []):
        if col in companion_row.index and str(companion_row[col]).strip() == "1":
            hits.append(aoi_name)
    return hits[0] if hits else None


def build_intervals_df(intervals: list) -> pd.DataFrame:
    df = pd.DataFrame(intervals)
    if df.empty:
        return df
    df["participant_id"] = df["participant_id"].astype(str).str.strip().str.lower()
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
    df = df[df["task"].isin(TASKS)]  # drop instruction/calibration screens

    starts = df[df["is_start"]].rename(columns={"timestamp": "start_ts"})
    ends = df[~df["is_start"]].rename(columns={"timestamp": "end_ts"})
    merged = pd.merge(
        starts[["participant_id", "recording_name", "task", "start_ts"]],
        ends[["participant_id", "recording_name", "task", "end_ts"]],
        on=["participant_id", "recording_name", "task"], how="left",
    )
    return merged


def attribute_clicks(clicks: list, intervals_df: pd.DataFrame, task_aois: dict) -> pd.DataFrame:
    rows = []
    for click in clicks:
        pid = str(click["participant_id"]).strip().lower()
        ts = pd.to_numeric(click["timestamp"], errors="coerce")
        candidates = intervals_df[
            (intervals_df["participant_id"] == pid)
            & (intervals_df["start_ts"] <= ts)
            & ((intervals_df["end_ts"].isna()) | (ts <= intervals_df["end_ts"]))
        ]
        if candidates.empty:
            continue  # click outside any scored task interval (instructions, calibration, etc.)

        interval = candidates.iloc[0]
        task = interval["task"]
        selected_aoi = resolve_selected_aoi(click["_companion_row"], task, task_aois)
        end_ts = interval["end_ts"]

        rows.append({
            "participant_id": pid,
            "task": task,
            "stimulus_start_ts": interval["start_ts"],
            "stimulus_end_ts": end_ts,
            "mousedown_ts": ts,
            "response_time_seconds": (ts - interval["start_ts"]) / 1_000_000,
            "mouse_x": pd.to_numeric(click["mouse_x"], errors="coerce"),
            "mouse_y": pd.to_numeric(click["mouse_y"], errors="coerce"),
            "selected_answer_aoi": selected_aoi,
            "missing_stimulus_end": pd.isna(end_ts),
        })

    return pd.DataFrame(rows)


def classify_responses(clicks_df: pd.DataFrame, intervals_df: pd.DataFrame) -> pd.DataFrame:
    """One row per (participant, task): status, first-click answer, multiple_clicks flag."""
    all_pairs = intervals_df[["participant_id", "task"]].drop_duplicates()

    if clicks_df.empty:
        summary = all_pairs.copy()
        summary["response_status"] = "no_click"
        summary["selected_answer_aoi"] = None
        summary["click_count"] = 0
        summary["multiple_clicks"] = False
        summary["response_time_seconds"] = np.nan
        return summary

    clicks_df = clicks_df.sort_values(["participant_id", "task", "mousedown_ts"])
    counts = clicks_df.groupby(["participant_id", "task"]).size().rename("click_count")
    first_click = clicks_df.groupby(["participant_id", "task"], as_index=False).first()
    first_click = first_click.merge(counts, on=["participant_id", "task"])
    first_click["multiple_clicks"] = first_click["click_count"] > 1

    def status(row):
        if row["missing_stimulus_end"]:
            return "missing_stimulus_end"
        if row["multiple_clicks"]:
            return "multiple_clicks"
        if pd.isna(row["selected_answer_aoi"]):
            return "outside_aoi"
        return "valid_answer"

    first_click["response_status"] = first_click.apply(status, axis=1)

    summary = all_pairs.merge(first_click, on=["participant_id", "task"], how="left")
    summary["response_status"] = summary["response_status"].astype("object").where(
        summary["response_status"].notna(), "no_click")
    summary["click_count"] = summary["click_count"].fillna(0).astype(int)
    summary["multiple_clicks"] = summary["multiple_clicks"].astype("object").where(
        summary["multiple_clicks"].notna(), False).astype(bool)
    return summary


def write_detailed_csv(summary: pd.DataFrame):
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    cols = [
        "participant_id", "task", "response_status", "selected_answer_aoi",
        "click_count", "multiple_clicks", "response_time_seconds",
        "stimulus_start_ts", "stimulus_end_ts", "mousedown_ts", "mouse_x", "mouse_y",
    ]
    cols = [c for c in cols if c in summary.columns]
    summary[cols].to_csv(CLICK_EVENTS_CSV, index=False)
    print(f"Wrote {len(summary)} rows to {CLICK_EVENTS_CSV}")


def write_student_responses_csv(summary: pd.DataFrame):
    answer_key = json.loads(ANSWER_KEY_JSON.read_text())
    df = summary.copy()
    df["correct_aoi"] = df["task"].map(lambda t: answer_key[t]["correct_aoi"])
    df["correct"] = (df["selected_answer_aoi"] == df["correct_aoi"]).astype(int).astype(object)
    df.loc[df["response_status"].isin(["no_click", "missing_stimulus_end"]), "correct"] = ""

    wide = df.pivot(index="participant_id", columns="task", values="correct")
    wide = wide.reindex(columns=TASKS)
    wide.columns = [f"{task}_response" for task in wide.columns]
    wide = wide.reset_index().sort_values("participant_id")

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    wide.to_csv(STUDENT_RESPONSES_CSV, index=False)
    print(f"Wrote {len(wide)} participants to {STUDENT_RESPONSES_CSV}")


def main():
    task_aois = load_task_aois()
    usecols = resolve_usecols(task_aois)
    print(f"Reading {DATAEXPORT_TSV} with {len(usecols)} columns, chunksize={CHUNKSIZE}...")

    clicks, intervals = process_chunks(usecols, task_aois)
    print(f"Found {len(clicks)} raw clicks, {len(intervals)} stimulus start/end events.")

    intervals_df = build_intervals_df(intervals)
    clicks_df = attribute_clicks(clicks, intervals_df, task_aois)
    summary = classify_responses(clicks_df, intervals_df)

    print(summary["response_status"].value_counts())

    write_detailed_csv(summary)
    write_student_responses_csv(summary)


if __name__ == "__main__":
    main()
