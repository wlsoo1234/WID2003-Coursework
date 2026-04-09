**Proposed study title**

**Predicting Cognitive Processing Style from Eye-Tracking During Visual
Search Tasks**

Sub title: **Eye Tracking for Classifying Fast vs Slow Problem Solvers**

This is practical because:

- students can all participate as subjects
- the task is easy to run in class
- eye-tracking features are straightforward
- the output can be used for a 2-class prediction model

**1. Study idea**

Students complete a short visual search task while their eye movements
are recorded.

The goal is to build a prediction model that classifies students into
**2 groups** based on their task performance. (fast vs slow problem
solvers)

**2-group classification target**

**A: High-performing vs low-performing**

Label students based on accuracy score:

- **Group 1:** High-performing
- **Group 2:** Low-performing

Example rule:

- top 50% accuracy = high-performing
- bottom 50% accuracy = low-performing

**B: Fast vs slow solvers**

Label students based on completion time:

- **Group 1:** Fast
- **Group 2:** Slow

Example rule:

- below median completion time = fast
- above median completion time = slow

**C: Focused vs distracted**

Label based on behavioral indicators such as off-task gaze or unstable
attention.
This is possible, but harder and less objective.

**2. Study objective**

To examine whether eye-tracking features during a visual search task can
predict whether a student belongs to the **high-performing** or
**low-performing** group / **fast vs slow solvers**.

**3. Research question**

**Can eye-tracking features be used to classify students into
high-performing and low-performing groups / fast vs slow solvers during
a short visual search task?**

**4. Hypothesis**

Students with better performance will show more efficient visual
attention patterns, such as:

- shorter time to relevant regions
- fewer unnecessary fixations
- more focused gaze distribution
- more organized scanpaths

**5. Task design**

**Multiple visual search questions** shown on a screen.

Other alternative examples:

- pattern matching
- odd-one-out
- Raven-like matrix reasoning
- visual search questions
- attention-based comparison tasks

Structure per trial:

- 1 question image on top
- 4 answer choices below
- student selects answer verbally or via keyboard/mouse

**Why this works?**

- easy to prepare
- easy to define Areas of Interest (AOIs)
- participant can understand task quickly
- produces both eye-tracking and performance data

**6. Experimental design**

**Design type**

**Within-class observational study**

All students are participants.

**Participants**

- CogSci students from same class and cohort
- Example: 80--100 students

**Stimuli**

Prepare around:

- **8 to 12 visual search task questions**
- Difficulty : easy -- moderate - hard
- each question displayed one at a time
- all participants will view same image

**AOIs**

For each question, define:

- **AOI 1:** Question/problem area
- **AOI 2--5:** Answer areas (i.e. A, B, C, D)

Optional:

- AOI for instruction area
- AOI for timer area if shown

**7. Variables**

**Independent/predictor variables**

Eye-tracking features

**Outcome variable**

Binary label:

- High-performing / fast solver
- Low-performing / slow solver

**Additional behavioral variables**

- accuracy
- response time

**8. Eye-tracking features to collect**

Metrics produced by Tobii Pro Lab.

**Basic gaze features**

- Total fixation duration
- Fixation count
- Average fixation duration
- Time to first fixation on correct answer AOI
- Total visit duration on correct answer AOI
- Visit count on each AOI
- Number of AOI transitions
- Proportion of gaze on problem area
- Proportion of gaze on answer options
- Response time

**Optional advanced features**

- Scanpath length
- Entropy of gaze distribution
- Revisits to previously viewed AOIs
- Ratio of problem-area viewing to answer-area viewing

**Recommended minimum feature set**

Use around 8--10 features: (can do feature engineering)

1. Total fixation duration
2. Fixation count
3. Average fixation duration
4. Time to first fixation on correct AOI
5. Visit count to correct AOI
6. Total duration on correct AOI
7. Number of AOI transitions
8. Response time
9. Proportion of gaze on problem AOI
10. Proportion of gaze on distractor AOIs

**9. Procedure**

**Part A: Preparation**

1. Prepare 8--12 visual search images.
2. Create AOIs for problem region and answer options.
3. Set up eye tracker and calibration.
4. Prepare response sheet or keyboard response input.
5. Explain task to students.

**Part B: Data collection**

1. Participant sits in front of tracker.
2. Perform calibration.
3. Show 1 practice trial.
4. Present test trials one by one.
5. Record gaze and response.
6. Repeat for each participant.

Giving chance for all to participate, group members can rotate roles:

- participant
- operator
- observer
- note taker
- data recorder

**10. Collaborative workflow**

**Group roles**

Divide members into small groups:

- **Option 1:** Eye tracker operator
- **Option 2:** Participant manager
- **Option 3:** Response/time recorder
- **Option 4:** Data cleaning and feature extraction team
- **Option 5:** AI modeling team

**11. Study pipeline**

**Phase 1: Study planning**

1. Define objective: classify high vs low performers / fast vs slow
   performers
2. Choose task: visual search images
3. Prepare 8--12 stimuli
4. Define AOIs
5. Prepare response recording form

**Phase 2: Data collection**

1. Recruit all participants
2. Obtain consent
3. Calibrate eye tracker
4. Run practice trial
5. Run experimental trials
6. Save gaze data and response data

**Phase 3: Label creation**

1. Compute accuracy for each student
2. Rank students by score
3. Split into two groups:

   - high-performing / fast
   - low-performing / slow

Possible rule (for performance levels):

- score above or equal to median = high
- score below median = low

Possible rule (for speed levels):

- speed of performance for each task (set a treshold for fast vs slow)

**Phase 4: Data preprocessing**

1. Remove poor-quality recordings
2. Exclude trials with tracking loss
3. Extract eye-tracking metrics per trial
4. Aggregate features per participant

   - mean fixation duration
   - total fixation count
   - mean response time
   - etc.
5. Standardize features (if needed)

**Phase 5: Dataset creation**

Build a table:

- each row = one student
- columns = extracted features
- final column = class label

**Phase 6: Exploratory analysis**

1. Compare groups visually
2. Check means and standard deviations
3. Plot boxplots or histograms
4. Identify features that differ between groups

**Phase 7: Prediction modeling**

1. Split data into train/test
2. Train simple classifiers
3. Evaluate performance
4. Compare models

**Phase 8: Interpretation**

1. Which features mattered most?
2. What gaze behaviors characterize high performers?
3. What does this suggest about cognition?

**12. Example dataset structure**

Each row is one participant.

  **Student**   **TFD\_Total**   **Fix\_Count**   **Avg\_Fix\_Dur**   **TFF\_CorrectAOI**   **Dur\_CorrectAOI**   **Visit\_CorrectAOI**   **AOI\_Transitions**   **ResponseTime**   **Distractor\_Gaze\_Ratio**   **Label**

---

  S01           12500            86               145                 820                   3400                  6                       14                     9.2                0.41                          High
  S02           15200            110              138                 1600                  2100                  9                       21                     13.8               0.58                          Low
  S03           11800            79               149                 700                   3600                  5                       12                     8.7                0.35                          High
  S04           16150            121              133                 1900                  1800                  10                      24                     14.6               0.62                          Low

**Meaning of selected columns (see Pro Lab Manual)**

- **TFD\_Total**: total fixation duration across all trials
- **Fix\_Count**: total number of fixations
- **Avg\_Fix\_Dur**: average fixation duration
- **TFF\_CorrectAOI**: time to first fixation on correct answer AOI
- **Dur\_CorrectAOI**: total time spent on correct answer
- **Visit\_CorrectAOI**: number of visits to correct answer
- **AOI\_Transitions**: total shifts between AOIs
- **ResponseTime**: average time per question
- **Distractor\_Gaze\_Ratio**: proportion of gaze spent on wrong
  answer options

**13. Labeling example**

Suppose 24 students participate.

If median accuracy = 7/10:

- accuracy 7 and above = High-performing
- accuracy below 7 = Low-performing

Alternative:

- top 12 = High
- bottom 12 = Low

keep the class sizes balanced.

**14. Suitable prediction models**

Use interpretable models to begin.

**Models options**

**1. Logistic Regression**

Good because:

- simple
- interpretable
- works well for small datasets

**2. Decision Tree**

Good because:

- easy to understand
- shows decision rules clearly

**3. Random Forest**

Good because:

- usually performs better than a single tree
- can show feature importance

**4. Support Vector Machine**

Good for small datasets, though less interpretable

**Recommended order**

Start with:

1. Logistic Regression
2. Decision Tree
3. Random Forest

**15. Model input and output**

**Input**

Eye-tracking features per participant

**Output**

Binary class:

- 1 = High-performing / fast
- 0 = Low-performing / slow

**16. Example modeling workflow**

**Step 1: Feature matrix**

X = eye-tracking features:

- fixation count
- average fixation duration
- time to first fixation on correct AOI
- distractor gaze ratio
- response time
- etc.

**Step 2: Target label**

y = performance group:

- High
- Low

**Step 3: Train-test split**

Example:

- 80% training
- 20% testing

If dataset is small, use:

- **5-fold cross-validation**

**Step 4: Train model**

Train logistic regression / decision tree / random forest

**Step 5: Evaluate**

Use:

- accuracy
- precision
- recall
- F1-score
- confusion matrix

**17. What features may predict the groups**

High-performing students may show:

- shorter time to correct AOI
- higher duration on relevant AOIs
- lower distractor gaze ratio
- fewer unnecessary AOI transitions
- shorter response times
- more efficient fixation patterns

Low-performing students may show:

- more scattered gaze
- longer search time
- more distractor viewing
- more revisits
- longer response time

**18. Interpretation**

This study helps students connect:

- **cognitive science**: attention, visual search, decision making
- **eye tracking**: fixations, transitions, AOIs
- **AI**: feature extraction, classification, prediction

Combines human cognition and machine learning in one classroom activity.

**19. Visual Search Task**

**Task**

Show 10 visual search questions.

**Features**

Extract following metrics:

- fixation count
- average fixation duration
- time to first fixation on correct answer
- response time
- distractor gaze ratio

**Label**

High vs low accuracy

**Models**

- Logistic Regression
- Decision Tree

**20. Example report structure**

Write report for the study using this structure:

1. Introduction
2. Objective
3. Participants
4. Task and stimuli
5. Eye-tracking setup
6. AOIs and measures
7. Label definition
8. Data preprocessing
9. Prediction model
10. Results
11. Discussion
12. Conclusion

**21. Summary of recommended study design**

**Study summary**

**Task:** visual search task
**Participants:** students from CogSci class
**Target classification:** high-performing vs low-performing / fast vs
slow solvers
**Data collected:** gaze features + accuracy + response time
**Unit of analysis:** participant-level aggregated features
**Models:** logistic regression, decision tree, random forest
