## core_logic

**Libraries** ->

import os

import pandas as pd

### Constants

SUBJECTS = ["English", "Hindi", "Mathematics", "Science", "Computer/AI"]   (5 subjects)

THEORY_MAX = 80

PRAC_MAX   = 20

SUBJECT_MAX = 100   (= THEORY_MAX + PRAC_MAX)

PASS_MARK = 33

max_total = 500   (SUBJECT_MAX * 5)

### Grade Thresholds

GRADE_THRESHOLDS = {

  "A1": 90, "A2": 80, "B1": 70, "B2": 60,

  "C1": 50, "C2": 40, "D":  0,

}

### Remarks Map

REMARKS_MAP = {

  "A1": "Outstanding performance. Keep it up!",

  "A2": "Excellent work. Aim for the next band.",

  "B1": "Very good. Push harder in weaker subjects.",

  "B2": "Good effort. Solidify concepts for top grade.",

  "C1": "Fair. Focus on consistent practice.",

  "C2": "Average. Needs structured revision.",

  "D":  "Needs improvement.",

}

FAIL override -> "Result: FAIL. Attend remedial classes."

### Functions

**get_grade(pct)** -> loop GRADE_THRESHOLDS, first threshold where pct >= thr wins; default "D"

**load_data(filename)** -> raises FileNotFoundError if missing (msg: "Run `python generate_csv.py` first"). Reads CSV, strips col names, coerces subject cols to int (NaN→0), Roll Number & Class astype int.

**processing_records(df)** -> df.copy(); for each subject:

  - obtained = df[s].clip(0, 100)
  - theory    = (obtained * 0.8).round().int.clip(upper=80)
  - practical = obtained - theory   (so total still equals obtained)

  Adds cols: grand_total, max_total (=500), average (mean, 2dp), percentage (grand_total/500*100, 2dp), grade, status, remarks, overall_rank, `{subject}_rank`.

  PASS rule: row.min() >= 33 across SUBJECTS  →  else FAIL.

  Rank method: `rank(ascending=False, method="min")` cast to int.

**search_student(df, query)** -> q = str(query).strip().lower()

  mask = name.str.lower().contains(q) | (Roll Number as string == q)

**calculate_results(row)** -> returns dict:

  {
    name, roll, class, section,
    subjects: [{name, theory, practical, total, max=100, grade}, x5],
    total, max_total=500, average, percentage, grade, status, remarks
  }

**compute_ranks(df)** -> {"overall": {roll: rank}, "subjects": {subject_name: {roll: rank}, ...}}

### Notes

- Subject col names must match SUBJECTS exactly (case-sensitive).
- Practical is whatever is left after theory split (not a separate input).
- `processing_records` is idempotent on the original CSV; never called twice on a processed df.
