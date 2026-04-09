# Data Collection Manual
## Eye-Tracking Study: Predicting Cognitive Processing Style from Visual Search

This document is a standalone guide for study operators. No coding background is required. Follow each section in order before running the analysis notebooks.

---

## Overview

**Study goal:** Record eye-tracking data while students complete 7 visual search tasks, then use machine learning to classify students as High/Low performers based on their gaze patterns.

**What you need to prepare:**
1. Eye-tracker hardware (Tobii Pro)
2. 7 visual search task stimuli (images)
3. AOI definitions in Tobii Pro Lab
4. This manual filled in with correct answers and AOI labels

**Roles during data collection:**
| Role | Responsibility |
|------|----------------|
| Operator | Runs the eye-tracker, starts/stops recordings |
| Participant manager | Brings in the next student, explains the task |
| Response recorder | Notes which answer (A/B/C/D) each student gave per question |
| Observer | Monitors data quality, flags tracking issues |
| Data recorder | Enters response data into `student_responses.csv` |

---

## Part A: Preparation Checklist

Complete this before the first participant arrives.

### A1. Stimuli preparation
- [ ] All 7 task images are loaded into Tobii Pro Lab as separate "slides" or "media"
- [ ] Task names in Pro Lab exactly match these (case-sensitive):
  - `findDice`
  - `findYummy`
  - `frogInBathroom`
  - `headphoneInBathroom`
  - `frog`
  - `whoCheats`
  - `whoThief`
- [ ] A practice trial image (not one of the 7 tasks) is prepared
- [ ] Task display order is fixed — all participants see tasks in the same order

### A2. AOI definition (do this in Tobii Pro Lab)
- [ ] For each of the 7 tasks, open the AOI editor in Pro Lab
- [ ] Draw rectangles over: the question/problem area, and each answer option (A, B, C, D)
- [ ] Name each rectangle using consistent labels — see Part E for naming rules
- [ ] Export the project once to confirm AOI hit columns appear in the Data export TSV
- [ ] Fill in `data/external/task_correct_aoi_map.json` (see Part E)

### A3. Hardware setup
- [ ] Eye tracker is mounted and powered on
- [ ] Monitor resolution matches the project settings in Pro Lab
- [ ] Room lighting is consistent (no direct light in participant's eyes)
- [ ] Chin rest is in place (strongly recommended for data quality)
- [ ] Test recording runs without errors on a lab member

### A4. Response recording sheet
- [ ] Print the response sheet (or open `student_responses.csv` on a separate device)
- [ ] Confirm that the response recorder knows what "A/B/C/D" correspond to on screen
- [ ] Confirm the correct answers are sealed in an envelope / known only to the study designer

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
1. Show the practice image
2. Tell the participant: *"You will see a picture with a question. Look at the question, then look at the answer options. When you know the answer, press the key / click on your choice."*
3. Wait for the participant to respond; confirm they understood the task
4. Do **not** give feedback on whether the practice answer was correct

### B4. Experimental trials
1. Show the 7 task images one by one, in the pre-defined order
2. Start recording gaze **before** the image appears on screen
3. The response recorder notes the participant's answer (A/B/C/D) for each task
4. Mark any trial where the participant looks away, blinks excessively, or the tracker loses gaze for > 2 seconds — these trials may need to be excluded
5. After all 7 tasks, stop the recording

### B5. Post-session
1. Save the recording in Pro Lab immediately
2. Hand the participant list to the data recorder to enter responses into `student_responses.csv`
3. Move to the next participant

---

## Part C: Recording Response Data — `student_responses.csv`

After all participants are done, enter their responses into this file.

### File location
`data/raw/student_responses.csv`

### Required column names (exact spelling, case-sensitive)

| Column | Description | Allowed values |
|--------|-------------|----------------|
| `participant_id` | Participant name as entered in Tobii Pro Lab, **lowercase** | e.g., `p01`, `p02` |
| `findDice_response` | Answer given for the findDice task | `A`, `B`, `C`, `D`, or `NA` |
| `findYummy_response` | Answer for findYummy | `A`, `B`, `C`, `D`, or `NA` |
| `frogInBathroom_response` | Answer for frogInBathroom | `A`, `B`, `C`, `D`, or `NA` |
| `headphoneInBathroom_response` | Answer for headphoneInBathroom | `A`, `B`, `C`, `D`, or `NA` |
| `frog_response` | Answer for frog | `A`, `B`, `C`, `D`, or `NA` |
| `whoCheats_response` | Answer for whoCheats | `A`, `B`, `C`, `D`, or `NA` |
| `whoThief_response` | Answer for whoThief | `A`, `B`, `C`, `D`, or `NA` |

### Example file content
```
participant_id,findDice_response,findYummy_response,frogInBathroom_response,headphoneInBathroom_response,frog_response,whoCheats_response,whoThief_response
p01,B,A,C,D,A,B,C
p02,A,A,C,D,B,B,A
p03,NA,C,A,D,A,C,C
```

### Rules
- Use `NA` (not blank, not 0) if a participant did not respond to a task
- `participant_id` must be **lowercase** (the notebook normalizes Tobii names to lowercase automatically)
- Do not add extra columns or change column order
- Save as UTF-8 CSV

---

## Part D: Answer Key Creation — `answer_key.json`

This file tells the notebook which answer letter (A/B/C/D) is correct for each task.

**Only the study designer (who prepared the stimuli) should fill this in.**

### File location
`data/external/answer_key.json`

### How to fill it in

Open the file and replace each `"?"` with the correct letter:

```json
{
  "findDice":            "B",
  "findYummy":           "A",
  "frogInBathroom":      "C",
  "headphoneInBathroom": "D",
  "frog":                "A",
  "whoCheats":           "B",
  "whoThief":            "C"
}
```

**What A/B/C/D means:** This corresponds to the layout of answer options on screen. You must define a consistent mapping. Recommended convention:

| Letter | Screen position |
|--------|----------------|
| A | Top-left |
| B | Top-right |
| C | Bottom-left |
| D | Bottom-right |

Document this mapping somewhere so the response recorder uses the same convention.

---

## Part E: Correct AOI Verification — `task_correct_aoi_map.json`

This file tells the notebook which AOI rectangle corresponds to the correct answer for each task.

### Why this matters
In Tobii Pro Lab, AOIs are named as rectangles. The Data export TSV has columns like:
```
AOI hit [findDice - Dice]
AOI hit [findDice - M1]
AOI hit [findDice - Rectangle 3]
```
You must confirm which rectangle is the correct answer AOI for each task.

### Step-by-step verification

1. Open Tobii Pro Lab
2. Navigate to the project → click on a task stimulus (e.g., `findDice`)
3. Open the AOI editor (View → AOI Editor, or similar)
4. Look at which rectangle is drawn over the **correct answer area**
5. Note the exact rectangle label (e.g., "Dice", "Rectangle", "Rectangle 2")
6. Repeat for all 7 tasks

### File location
`data/external/task_correct_aoi_map.json`

### How to fill it in

For each task, update the `"correct_aoi"` field to the exact label you saw in Pro Lab:

```json
{
  "findDice": {
    "correct_aoi": "Dice",
    "distractor_aois": ["M1", "M2", "Rectangle 3", "Rectangle 4", ...]
  },
  "findYummy": {
    "correct_aoi": "Rectangle 2",
    "distractor_aois": ["Rectangle", "Rectangle 1", "Rectangle 3", ...]
  }
}
```

**The label must match exactly** what appears in the TSV column header after the dash:
- Column: `AOI hit [findYummy - Rectangle 2]`
- → correct_aoi: `"Rectangle 2"`

> **Tip:** To see all available AOI names for a task, open the Data export TSV in Excel or a text editor and search for `AOI hit [findDice`. All columns with that prefix list the available AOI labels.

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
