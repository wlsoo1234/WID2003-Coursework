"""
config.py — Centralized constants for the WID2003 eye-tracking pipeline.
All column names, task definitions, and AOI mappings live here.
"""
from pathlib import Path

# ── Project paths ─────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_RAW        = ROOT / "data" / "raw"
DATA_PROCESSED  = ROOT / "data" / "processed"
DATA_EXTERNAL   = ROOT / "data" / "external"
OUTPUTS_FIGURES = ROOT / "outputs" / "figures"
OUTPUTS_MODELS  = ROOT / "outputs" / "models"
OUTPUTS_REPORTS = ROOT / "outputs" / "reports"

# ── Raw file names ─────────────────────────────────────────────────────────────
METRICS_TSV    = DATA_RAW / "VisualTask with recording Metrics.tsv"
# METRICS_TSV = DATA_RAW / "mock_VisualTask_Metrics.tsv"
DATAEXPORT_TSV = DATA_RAW / "VisualTask with recording Data export.tsv"
# DATAEXPORT_TSV = DATA_RAW / "mock_VisualTask_Data_export.tsv"

# ── Stimuli paths ─────────────────────────────────────────────────────────────
DATA_STIMULI = ROOT / "data" / "stimuli"

def stimulus_png(task_name: str):
    """Return Path to a task's PNG image file."""
    return DATA_STIMULI / f"{task_name}.png"

def stimulus_aois(task_name: str):
    """Return Path to a task's .aois file."""
    return DATA_STIMULI / f"{task_name}Aois.aois"

# ── All tasks including practice/warm-up ──────────────────────────────────────
# spotNeedleInst is treated as a task in analysis (confirmed in answer_key.json)
PRACTICE_TRIAL_NAME = "spotNeedleInst"  # kept for backward compatibility

# ── Processed file names ───────────────────────────────────────────────────────
METRICS_CLEAN_PKL    = DATA_PROCESSED / "metrics_clean.parquet"
RAWGAZE_CLEAN_PKL    = DATA_PROCESSED / "raw_gaze_clean.parquet"
FEATURES_PER_TASK    = DATA_PROCESSED / "features_per_task.parquet"
LABELS_CSV           = DATA_PROCESSED / "labels.csv"
DATASET_FINAL        = DATA_PROCESSED / "dataset_final.parquet"
SCALER_PKL           = DATA_PROCESSED / "scaler.pkl"

# ── External config files ──────────────────────────────────────────────────────
AOI_MAP_JSON    = DATA_EXTERNAL / "task_correct_aoi_map.json"
ANSWER_KEY_JSON = DATA_EXTERNAL / "answer_key.json"

# ── Tobii Pro Lab: Metrics TSV column names ────────────────────────────────────
class MetricsCols:
    RECORDING   = "Recording"
    PARTICIPANT = "Participant"
    TIMELINE    = "Timeline"
    TOI         = "TOI"
    INTERVAL    = "Interval"
    MEDIA       = "Media"
    AOI         = "AOI"

    DURATION_OF_INTERVAL  = "Duration_of_interval"
    START_OF_INTERVAL     = "Start_of_interval"
    LAST_KEY_PRESS        = "Last_key_press"

    # Fixations
    TOTAL_FIX_DUR   = "Total_duration_of_fixations"
    AVG_FIX_DUR     = "Average_duration_of_fixations"
    MIN_FIX_DUR     = "Minimum_duration_of_fixations"
    MAX_FIX_DUR     = "Maximum_duration_of_fixations"
    NUM_FIXATIONS   = "Number_of_fixations"
    TIME_FIRST_FIX  = "Time_to_first_fixation"
    DUR_FIRST_FIX   = "Duration_of_first_fixation"

    # Whole fixations
    TOTAL_WHOLE_FIX_DUR  = "Total_duration_of_whole_fixations"
    AVG_WHOLE_FIX_DUR    = "Average_duration_of_whole_fixations"
    NUM_WHOLE_FIXATIONS  = "Number_of_whole_fixations"
    TIME_FIRST_WHOLE_FIX = "Time_to_first_whole_fixation"

    # Visits
    TOTAL_VISIT_DUR  = "Total_duration_of_Visit"
    AVG_VISIT_DUR    = "Average_duration_of_Visit"
    MIN_VISIT_DUR    = "Minimum_duration_of_Visit"
    MAX_VISIT_DUR    = "Maximum_duration_of_Visit"
    NUM_VISITS       = "Number_of_Visits"
    TIME_FIRST_VISIT = "Time_to_first_Visit"
    DUR_FIRST_VISIT  = "Duration_of_first_Visit"

    # Glances
    TOTAL_GLANCE_DUR  = "Total_duration_of_Glances"
    AVG_GLANCE_DUR    = "Average_duration_of_Glances"
    NUM_GLANCES       = "Number_of_Glances"
    TIME_FIRST_GLANCE = "Time_to_first_Glance"

    # Mouse
    NUM_MOUSE_CLICKS           = "Number_of_mouse_clicks"
    TIME_FIRST_MOUSE_CLICK     = "Time_to_first_mouse_click"
    TIME_FIX_TO_CLICK          = "Time_from_first_fixation_to_mouse_click"
    NUM_MOUSE_CLICKS_RELEASES  = "Number_of_mouse_clicks_and_releases"

    # Saccades
    NUM_SACCADES          = "Number_of_saccades_in_AOI"
    TIME_ENTRY_SACCADE    = "Time_to_entry_saccade"
    TIME_EXIT_SACCADE     = "Time_to_exit_saccade"
    PEAK_VEL_ENTRY_SACC   = "Peak_velocity_of_entry_saccade"
    PEAK_VEL_EXIT_SACC    = "Peak_velocity_of_exit_saccade"

    # Physiology
    AVG_PUPIL_DIAMETER = "Average_pupil_diameter"
    AVG_EYE_OPENNESS   = "Average_eye_openness"
    LAST_AOI_VIEWED    = "Last_AOI_viewed"
    AOI_AT_INTERVAL_END = "AOI_at_interval_end"


# ── Tobii Pro Lab: Data Export TSV column names ────────────────────────────────
class ExportCols:
    RECORDING_TIMESTAMP   = "Recording timestamp"
    PARTICIPANT_NAME      = "Participant name"
    RECORDING_NAME        = "Recording name"
    EYETRACKER_TIMESTAMP  = "Eyetracker timestamp"
    EVENT                 = "Event"
    EVENT_VALUE           = "Event value"

    GAZE_X        = "Gaze point X"
    GAZE_Y        = "Gaze point Y"
    FIXATION_X    = "Fixation point X"
    FIXATION_Y    = "Fixation point Y"

    PUPIL_LEFT     = "Pupil diameter left"
    PUPIL_RIGHT    = "Pupil diameter right"
    PUPIL_FILTERED = "Pupil diameter filtered"
    EYE_OPEN_LEFT  = "Eye openness left"
    EYE_OPEN_RIGHT = "Eye openness right"
    EYE_OPEN_FILT  = "Eye openness filtered"
    VALIDITY_LEFT  = "Validity left"
    VALIDITY_RIGHT = "Validity right"

    EYE_MOVEMENT_TYPE     = "Eye movement type"
    EYE_MOVEMENT_DURATION = "Eye movement event duration"
    EYE_MOVEMENT_INDEX    = "Eye movement type index"

    PRESENTED_STIMULUS    = "Presented Stimulus name"
    PRESENTED_MEDIA       = "Presented Media name"
    PRESENTED_MEDIA_W     = "Presented Media width"
    PRESENTED_MEDIA_H     = "Presented Media height"

    # Calibration/validation
    AVG_CAL_ACCURACY_DEG  = "Average calibration accuracy (degrees)"
    AVG_VAL_ACCURACY_DEG  = "Average validation accuracy (degrees)"

    # AOI hit column prefix pattern: "AOI hit [{task} - {aoi}]"
    AOI_HIT_PREFIX = "AOI hit"


# ── Eye movement type values ───────────────────────────────────────────────────
class EyeMovementType:
    FIXATION     = "Fixation"
    SACCADE      = "Saccade"
    UNCLASSIFIED = "Unclassified"

VALID_EYE_MOVEMENT_TYPES = {
    EyeMovementType.FIXATION,
    EyeMovementType.SACCADE,
    EyeMovementType.UNCLASSIFIED,
}

# ── Task names (must match Tobii "Presented Media name" / "Media" column) ──────
TASKS = [
    "findDice",
    "findYummy",
    "frogInBathroom",
    "headphoneInBathroom",
    "frog",
    "whoCheats",
    "whoThief",
    "spotNeedleInst",
]

# ── Features to extract from Metrics file per (Participant, Media, AOI) ────────
METRICS_FEATURE_COLS = [
    MetricsCols.TOTAL_FIX_DUR,
    MetricsCols.AVG_FIX_DUR,
    MetricsCols.NUM_FIXATIONS,
    MetricsCols.TIME_FIRST_FIX,
    MetricsCols.DUR_FIRST_FIX,
    MetricsCols.TOTAL_VISIT_DUR,
    MetricsCols.NUM_VISITS,
    MetricsCols.TIME_FIRST_VISIT,
    MetricsCols.AVG_VISIT_DUR,
    MetricsCols.TOTAL_GLANCE_DUR,
    MetricsCols.NUM_GLANCES,
    MetricsCols.NUM_SACCADES,
    MetricsCols.PEAK_VEL_ENTRY_SACC,
    MetricsCols.PEAK_VEL_EXIT_SACC,
    MetricsCols.AVG_PUPIL_DIAMETER,
    MetricsCols.AVG_EYE_OPENNESS,
    MetricsCols.TIME_FIRST_MOUSE_CLICK,
    MetricsCols.TIME_FIX_TO_CLICK,
    MetricsCols.NUM_MOUSE_CLICKS,
]

# ── Label constants ────────────────────────────────────────────────────────────
LABEL_HIGH = 1
LABEL_LOW  = 0
LABEL_FAST = 1
LABEL_SLOW = 0

PERFORMANCE_LABEL_COL = "performance_label"
SPEED_LABEL_COL       = "speed_label"

# ── Modeling constants ─────────────────────────────────────────────────────────
RANDOM_STATE = 42
TEST_SIZE    = 0.2
CV_FOLDS_LARGE = 5   # for N >= 30
CV_FOLDS_SMALL = None  # triggers LOO-CV when N < 30
MIN_N_FOR_KFOLD = 30
