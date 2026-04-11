# WID2003 — Cognitive Science Practical Project
## Predicting Cognitive Processing Style from Eye-Tracking During Visual Search Tasks

**Course:** WID2003 Cognitive Science
**Faculty:** Faculty of Computer Science and Information Technology (FSKTM)
**University:** Universiti Malaya

---

## Overview

This project integrates three areas of cognitive science into a single end-to-end analysis:

| Domain | What we use it for |
|---|---|
| **Cognitive Science** | Understanding how attention and visual search work |
| **Eye-Tracking** | Measuring gaze behaviour objectively (Tobii Pro Lab) |
| **Machine Learning** | Classifying participants as high vs. low performers |

Participants completed **8 visual search tasks** while their eye movements were recorded. The goal is to build a classifier that predicts whether a student is a **high-performing** or **low-performing** problem solver based solely on their gaze patterns — without needing to know their answer.

---

## Research Question

> Can eye-tracking features captured during visual search tasks predict whether a student belongs to the high-performing or low-performing group?

**Hypothesis:** High-performing students will show more efficient visual attention — shorter time to the target area, higher dwell time on the correct region, and fewer unnecessary fixations on distractors.

---

## Visual Search Tasks

All 8 tasks are shown as full-screen images. Participants are timed and observed.

| Task | Description | Type |
|---|---|---|
| `findDice` | Find the dice hidden among food items | Find object |
| `findYummy` | Find the hidden word "YUMMY" in a pizza restaurant scene | Find word |
| `frogInBathroom` | Spot the frog hidden inside a bathroom scene | Find object |
| `headphoneInBathroom` | Spot the headphones hidden in a bathroom | Find object |
| `frog` | Identify the frog that is different from all others | Spot the odd one |
| `whoCheats` | Identify which student is cheating in the classroom | Identify who |
| `whoThief` | Identify the thief in a crowd scene | Identify who |
| `spotNeedleInst` | Spot the needle hidden in the scene | Find object |

Each task has a set of labelled **Areas of Interest (AOIs)** defined in Tobii Pro Lab:
- `answer` — the correct target region
- `M1`, `M2`, ... — distractor regions

---

## Project Structure

```
WID2003/
├── data/
│   ├── raw/                  ← Original Tobii Pro Lab exports (TSV files)
│   ├── processed/            ← Cleaned data and features (auto-generated)
│   ├── stimuli/              ← Task images (.png) and AOI files (.aois)
│   └── external/
│       ├── task_correct_aoi_map.json  ← AOI-to-answer mapping (verified)
│       └── answer_key.json            ← Confirmed correct answers per task
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_feature_extraction.ipynb
│   ├── 03_label_creation.ipynb
│   ├── 04_dataset_creation.ipynb
│   ├── 05_exploratory_analysis.ipynb
│   ├── 06_prediction_models.ipynb
│   └── 07_interpretation.ipynb
├── outputs/
│   ├── figures/              ← All plots (auto-generated)
│   ├── models/               ← Trained model and metadata (auto-generated)
│   └── reports/              ← CSV summaries (auto-generated)
├── src/
│   ├── __init__.py
│   └── config.py             ← All column names, paths, and constants
├── data_collection_manual.md ← Operator guide for running the study
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Create a virtual environment

```bash
python -m venv wid2003_venv
source wid2003_venv/bin/activate        # Linux / macOS
wid2003_venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch Jupyter

```bash
jupyter notebook
```

Open the `notebooks/` folder and run the notebooks in order (01 → 07).

---

## Pipeline Execution Order

Run the notebooks **in this exact sequence**. Each notebook depends on the outputs of the previous one.

```
01_data_preprocessing
        ↓
02_feature_extraction
        ↓
03_label_creation
        ↓
04_dataset_creation
       ↙ ↘
05_exploratory   06_prediction_models
                        ↓
                 07_interpretation
```

| Step | Notebook | Time estimate |
|---|---|---|
| 1 | `01_data_preprocessing` | ~2 min (loads 31 MB file) |
| 2 | `02_feature_extraction` | ~5 min |
| 3 | `03_label_creation` | < 1 min |
| 4 | `04_dataset_creation` | < 1 min |
| 5 | `05_exploratory_analysis` | ~2 min |
| 6 | `06_prediction_models` | ~5–10 min (cross-validation) |
| 7 | `07_interpretation` | ~3 min (SHAP computation) |

---

## Data Files

| File | Description |
|---|---|
| `data/raw/VisualTask_Metrics.tsv` | Pre-aggregated eye-tracking metrics per AOI per participant (Tobii Pro Lab export) |
| `data/raw/VisualTask_Data_export.tsv` | Raw gaze point data at full sampling rate (~30 MB) |
| `data/raw/student_responses.csv` | Manual response accuracy per participant per task (1 = correct, 0 = incorrect) |
| `data/external/task_correct_aoi_map.json` | Maps each task to its correct AOI (`answer`/`answer1`) and distractors (`M1`–`M15`, `aoi1`–`aoi9`) |
| `data/external/answer_key.json` | Confirms the correct AOI and task type for each stimulus |

---

## Key Concepts

### Areas of Interest (AOIs)
Rectangular regions drawn on the stimulus image in Tobii Pro Lab. In this study, each task has:
- **`answer`** (or **`answer1`** for `frogInBathroom`) — the region containing the target (what the participant is looking for)
- **`M1`–`M15`** — distractor regions (wrong areas)
- **`aoi1`–`aoi9`** — distractor regions used in `findYummy`

### Eye-Tracking Features
Metrics recorded per AOI per participant:

| Feature | Cognitive meaning |
|---|---|
| Time to first fixation on `answer` | How quickly the participant detected the target |
| Total fixation duration on `answer` | How long they focused on the correct region |
| Number of visits to `answer` | How many times they returned to the target |
| Distractor dwell ratio | Proportion of time spent on wrong regions |
| Scanpath length | Total distance the eye traveled |
| Pupil diameter change | Proxy for cognitive load over time |

### Classification Labels
Participants are split into two groups using a **median split** on their accuracy score:
- **High-performing (1):** Accuracy at or above the group median
- **Low-performing (0):** Accuracy below the group median

---

## Group Roles

During data collection, group members rotate through these roles:

| Role | Responsibility |
|---|---|
| Eye-tracker operator | Runs recordings in Tobii Pro Lab, manages calibration |
| Participant manager | Welcomes participants, explains the task |
| Response recorder | Notes each participant's response (found / not found) |
| Data recorder | Enters responses into `student_responses.csv` |
| Observer | Monitors data quality, notes any tracking issues |

---

## Notebook Guide

See the individual README for each notebook inside the `notebooks/` folder for learning objectives, expected outputs, and discussion questions.

---

## References

- Holmqvist, K. et al. (2011). *Eye Tracking: A Comprehensive Guide to Methods and Measures*. Oxford University Press.
- Rayner, K. (1998). Eye movements in reading and information processing: 20 years of research. *Psychological Bulletin, 124*(3), 372–422.
- Tobii Pro Lab User Manual: [https://www.tobii.com/](https://www.tobii.com/)
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR, 12*, 2825–2830.
- Lundberg, S. & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *NeurIPS*.
