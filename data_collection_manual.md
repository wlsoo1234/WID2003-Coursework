# Data Collection Manual
## Eye-Tracking Study: Predicting Cognitive Processing Style from Visual Search

This document is a standalone guide for study operators. No coding background is required. Follow each section in order before running the analysis notebooks.

---

## Overview

**Study goal:** Record eye-tracking data while students complete 13 visual search tasks, then use machine learning to classify students as High/Low performers based on their gaze patterns.

**What you need to prepare:**
1. Eye-tracker hardware (Tobii Pro)
2. 13 visual search task stimuli (images)
3. AOI definitions in Tobii Pro Lab
4. This manual filled in with correct answers and AOI labels

**Roles during data collection:**
| Role | Responsibility |
|------|----------------|
| Operator | Runs the eye-tracker, starts/stops recordings |
| Participant manager | Brings in the next student, explains the task |
| Response recorder | Notes which region the student clicked per task (or leaves this to the automated extraction — see Part C) |
| Observer | Monitors data quality, flags tracking issues |
| Data recorder | Enters/verifies response data in `student_responses.csv` |

---

## Part A: Preparation Checklist

Complete this before the first participant arrives.

### A1. Stimuli preparation
- [ ] All 13 task images are loaded into Tobii Pro Lab as separate "slides" or "media"
- [ ] Task names in Pro Lab exactly match these (case-sensitive):
  - `Crown`
  - `findDice`
  - `Hat`
  - `Iguana`
  - `Rabbit`
  - `Shoe`
  - `T1_Prisoner-15sec`
  - `T2_Ring-15sec`
  - `T3_Umbrella-15 sec` (note the space before "sec")
  - `T4_Pen-15sec`
  - `T5_Fish-15sec`
  - `T6_Heart-15sec`
  - `Toothbrush`
- [ ] Instruction/calibration screens (`Welcome`, `StudyInst`, `PracticeInst`, `TaskInst`, `CheckInst`, `EndTask`) are prepared separately and are not scored tasks
- [ ] Task display order is fixed — all participants see tasks in the same order

### A2. AOI definition (do this in Tobii Pro Lab)
- [ ] For each of the 13 tasks, open the AOI editor in Pro Lab
- [ ] Draw one rectangle per candidate region where the hidden target could be (the correct region plus every distractor region) — each task typically has 10–17 candidate regions, not a fixed A/B/C/D set
- [ ] Name each rectangle using consistent labels — see Part E for naming rules
- [ ] Export the project once to confirm AOI hit columns appear in the Data export TSV
- [ ] Fill in `data/external/task_correct_aoi_map.json` (see Part E)

### A3. Hardware setup
- [ ] Eye tracker is mounted and powered on
- [ ] Monitor resolution matches the project settings in Pro Lab
- [ ] Room lighting is consistent (no direct light in participant's eyes)
- [ ] Chin rest is in place (strongly recommended for data quality)
- [ ] Test recording runs without errors on a lab member

### A4. Response recording
- [ ] Confirm participants respond by mouse-clicking the region where they found the hidden target
- [ ] Confirm the correct AOI per task is recorded in `data/external/answer_key.json`, known only to the study designer
- [ ] Confirm `scripts/extract_click_responses.py` will be run on the raw Data export TSV after data collection to auto-populate `student_responses.csv` (see Part C) — manual response recording is a fallback, not the primary path

---

## Part B: Data Collection Protocol

Repeat this procedure for every participant.

### B1. Setup
1. Ask the participant to sit in front of the eye tracker with their head in the chin rest
2. Adjust the chin rest height so the participant looks naturally at the center of the screen
3. Make sure the eye tracker camera can see both eyes (check the Pro Lab camera view)

### B2. Calibration
1. In Tobii Pro Lab: start a new recording for this participant
2. Enter the participant's name exactly as it appears on the class roster (see naming rules below)
3. Run the 5-point or 9-point calibration
4. Check calibration accuracy — **reject and redo** if any point has accuracy worse than 1.0°
5. Run validation if Pro Lab offers it; record the result in your notes

> **Participant naming rules (critical):**
> - Use the same format for every participant: e.g., `P01`, `P02`, ... `P30`
> - No spaces, no special characters
> - This name must exactly match what you write in `student_responses.csv`
> - If a name is entered incorrectly, note it on the reconciliation sheet (see Part F)

### B3. Practice trial
1. Show the `PracticeInst` screen / practice image
2. Tell the participant: *"You will see a picture with a hidden object somewhere in the scene. When you find it, click on it with the mouse."*
3. Wait for the participant to respond; confirm they understood the task
4. Do **not** give feedback on whether the practice answer was correct

### B4. Experimental trials
1. Show the 13 task images one by one, in the pre-defined order
2. Start recording gaze **before** the image appears on screen
3. The participant clicks the region where they found the hidden target; the click is captured automatically in the Data export TSV (`Event = MouseEvent`, `Event value = Down, Left`) — no manual response recording is required
4. Mark any trial where the participant looks away, blinks excessively, or the tracker loses gaze for > 2 seconds — these trials may need to be excluded
5. After all 13 tasks, stop the recording

### B5. Post-session
1. Save the recording in Pro Lab immediately
2. After all participants are done, run `scripts/extract_click_responses.py` against the exported Data export TSV to populate `student_responses.csv` (see Part C)
3. Move to the next participant

---

## Part C: Recording Response Data — `student_responses.csv`

### Preferred path: automated extraction
After all participants are done, run:
```
python scripts/extract_click_responses.py
```
This reads `data/raw/VisualTask_CogSci Data export.tsv`, finds each participant's first mouse-click within each task's on-screen interval, determines which AOI it landed in (via the `AOI hit [...]` columns), and cross-references `data/external/answer_key.json` to write `data/raw/student_responses.csv` automatically — no manual entry needed. It also writes `data/processed/click_events_detailed.csv`, a full audit log of every click (including `response_status` — `valid_answer`, `no_click`, `outside_aoi`, `multiple_clicks`, or `missing_stimulus_end`) for quality review.

### Fallback: manual entry
If the automated extraction can't be run, enter responses by hand.

### File location
`data/raw/student_responses.csv`

### Required column names (exact spelling, case-sensitive)

| Column | Description | Allowed values |
|--------|-------------|----------------|
| `participant_id` | Participant name as entered in Tobii Pro Lab, **lowercase** | e.g., `vt1`, `vt2` |
| `Crown_response` | Whether the participant clicked the correct AOI for Crown | `1`, `0`, or blank |
| `findDice_response` | Whether the participant clicked the correct AOI for findDice | `1`, `0`, or blank |
| `Hat_response` | Whether the participant clicked the correct AOI for Hat | `1`, `0`, or blank |
| `Iguana_response` | Whether the participant clicked the correct AOI for Iguana | `1`, `0`, or blank |
| `Rabbit_response` | Whether the participant clicked the correct AOI for Rabbit | `1`, `0`, or blank |
| `Shoe_response` | Whether the participant clicked the correct AOI for Shoe | `1`, `0`, or blank |
| `T1_Prisoner-15sec_response` | Whether the participant clicked the correct AOI for T1_Prisoner-15sec | `1`, `0`, or blank |
| `T2_Ring-15sec_response` | Whether the participant clicked the correct AOI for T2_Ring-15sec | `1`, `0`, or blank |
| `T3_Umbrella-15 sec_response` | Whether the participant clicked the correct AOI for T3_Umbrella-15 sec | `1`, `0`, or blank |
| `T4_Pen-15sec_response` | Whether the participant clicked the correct AOI for T4_Pen-15sec | `1`, `0`, or blank |
| `T5_Fish-15sec_response` | Whether the participant clicked the correct AOI for T5_Fish-15sec | `1`, `0`, or blank |
| `T6_Heart-15sec_response` | Whether the participant clicked the correct AOI for T6_Heart-15sec | `1`, `0`, or blank |
| `Toothbrush_response` | Whether the participant clicked the correct AOI for Toothbrush | `1`, `0`, or blank |

### Example file content
```
participant_id,Crown_response,findDice_response,Hat_response,Iguana_response,Rabbit_response,Shoe_response,T1_Prisoner-15sec_response,T2_Ring-15sec_response,T3_Umbrella-15 sec_response,T4_Pen-15sec_response,T5_Fish-15sec_response,T6_Heart-15sec_response,Toothbrush_response
vt1,1,1,0,1,1,1,0,1,1,1,0,1,1
vt2,0,1,1,1,0,1,1,1,0,1,1,1,0
```

### Rules
- Leave blank (not `NA`) if a participant did not click anywhere within a task's interval
- `participant_id` must be **lowercase**
- Do not add extra columns or change column order
- Save as UTF-8 CSV

---

## Part D: Answer Key Creation — `answer_key.json`

This file tells the pipeline which AOI is the correct target region for each task.

**Only the study designer (who prepared the stimuli) should fill this in.**

### File location
`data/external/answer_key.json`

### How to fill it in

Open the file and set `correct_aoi` to the exact AOI name (from the `.aois` file, e.g. `C1`, `D1`) that covers the hidden target:

```json
{
  "Crown":               { "correct_aoi": "C1", "task_type": "find_object", "confirmed": true },
  "findDice":            { "correct_aoi": "D1", "task_type": "find_object", "confirmed": true },
  "Hat":                 { "correct_aoi": "H1", "task_type": "find_object", "confirmed": true }
}
```

There is no A/B/C/D convention in this study — each task has one correct AOI among several candidate regions (10–17 per task), and every other AOI in that stimulus is a distractor (recorded in `task_correct_aoi_map.json`, Part E).

---

## Part E: Correct AOI Verification — `task_correct_aoi_map.json`

This file tells the pipeline which AOI rectangle is correct and which are distractors, for each task.

### Why this matters
In Tobii Pro Lab, AOIs are named as rectangles. The Data export TSV has columns like:
```
AOI hit [Crown - C1]
AOI hit [Crown - C2]
AOI hit [findDice - D1]
```
You must confirm which rectangle is the correct answer AOI for each task.

### Step-by-step verification

1. Open Tobii Pro Lab
2. Navigate to the project → click on a task stimulus (e.g., `Crown`)
3. Open the AOI editor (View → AOI Editor, or similar)
4. Look at which rectangle is drawn over the **correct answer area**
5. Note the exact rectangle label (e.g., `C1`)
6. Repeat for all 13 tasks

### File location
`data/external/task_correct_aoi_map.json`

### How to fill it in

For each task, update the `"correct_aoi"` field to the exact label you saw in Pro Lab, and list every other AOI for that stimulus as `distractor_aois`:

```json
{
  "Crown": {
    "correct_aoi": "C1",
    "distractor_aois": ["C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]
  },
  "findDice": {
    "correct_aoi": "D1",
    "distractor_aois": ["D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"]
  }
}
```

**The label must match exactly** what appears in the TSV column header after the dash:
- Column: `AOI hit [Crown - C1]`
- → correct_aoi: `"C1"`

> **Tip:** To see all available AOI names for a task, open the Data export TSV in Excel or a text editor and search for `AOI hit [Crown`. All columns with that prefix list the available AOI labels.

---

## Part F: Participant ID Reconciliation

If a participant name was typed incorrectly in Tobii Pro Lab (e.g., `P01` instead of `p01`, or `Prticipant03`), the notebooks will flag a mismatch between the eye-tracking data and the response CSV.

### How to fix

1. Run notebook `01_data_preprocessing.ipynb` — it prints all participant IDs found in both files
2. If you see IDs in one file but not the other, check for:
   - Typos (extra spaces, wrong capitalization, missing digit)
   - Extra leading/trailing spaces in the Tobii name
3. Create a reconciliation file `data/external/participant_id_reconciliation.csv`:

```
tobii_id,correct_id
prticipant03,p03
P 04,p04
```

4. Add a cell to notebook `01` to apply this mapping before saving the cleaned data

---

## Part G: Data Export from Tobii Pro Lab

Before running the notebooks, make sure both TSV files are exported from Pro Lab using the correct settings.

### Metrics TSV export settings
- Export type: **Metrics** (per AOI / per TOI)
- Include: all TOIs, all AOIs
- Metrics to include: fixations, visits, glances, saccades, pupil diameter, mouse clicks
- File name: `VisualTask with recording Metrics.tsv`
- Save to: `data/raw/`

### Data export TSV settings
- Export type: **Raw data / Data export**
- Include: Gaze points, fixation events, saccade events, AOI hits, pupil data, mouse events
- Coordinate system: pixels (DACSpx) preferred, plus normalized MCSnorm
- File name: `VisualTask with recording Data export.tsv`
- Save to: `data/raw/`

> **Check:** After exporting, open the Data export TSV and verify that `AOI hit [taskName - aoiName]` columns are present. If they are missing, the AOIs may not have been defined in Pro Lab before recording.

---

## Quick Reference: What to Prepare Before Each Notebook

| Notebook | What you need ready |
|----------|---------------------|
| `01_data_preprocessing` | Both TSV files in `data/raw/` |
| `02_feature_extraction` | `data/external/task_correct_aoi_map.json` filled and verified |
| `03_label_creation` | `data/raw/student_responses.csv` created; `data/external/answer_key.json` filled |
| `04_dataset_creation` | Notebooks 02 and 03 completed successfully |
| `05_exploratory_analysis` | Notebook 04 completed |
| `06_prediction_models` | Notebook 04 completed |
| `07_interpretation` | Notebook 06 completed |

---

## Contact

If you encounter issues with the data files or the notebooks, contact the AI modeling team member assigned to this project.
