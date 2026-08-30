import os
import pandas as pd

SUBJECTS    = ["English", "Hindi", "Mathematics", "Science", "Computer/AI"]
THEORY_MAX  = 80       
PRAC_MAX    = 20
SUBJECT_MAX = THEORY_MAX + PRAC_MAX   # 100
PASS_MARK   = 33

GRADE_THRESHOLDS = [
    ("A1", 90), ("A2", 80), ("B1", 70), ("B2", 60),
    ("C1", 50), ("C2", 40), ("D",  0),
]

REMARKS_MAP = {
    "A1": "Outstanding performance. Keep it up!",
    "A2": "Excellent work. Aim for the next band.",
    "B1": "Very good. Push harder in weaker subjects.",
    "B2": "Good effort. Solidify concepts for top grade.",
    "C1": "Fair. Focus on consistent practice.",
    "C2": "Average. Needs structured revision.",
    "D":  "Needs improvement.",
}


# ------------------------- GRADE HELPER -----------------------
def get_grade(pct):
    for grade, thr in GRADE_THRESHOLDS:
        if pct >= thr:
            return grade
    return "D"


# ------------------------- LOAD -------------------------
def load_data(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"CSV file not found: {filename}\n"
            f"Run `python generate_csv.py` first.")
    df = pd.read_csv(filename)
    df.columns = df.columns.str.strip()
    for s in SUBJECTS:
        df[s] = pd.to_numeric(df[s], errors="coerce").fillna(0).astype(int)
    df["Roll Number"] = df["Roll Number"].astype(int)
    df["Class"]       = df["Class"].astype(int)
    return df


# ------------------------- PROCESS --------------------- 
def processing_records(df):
    df = df.copy()

    # --- Theory / Practical split (80 % / 20 % of each subject) ---
    for s in SUBJECTS:
        obtained = df[s].clip(lower=0, upper=SUBJECT_MAX)
        df[f"{s}_theory"]    = (obtained * 0.8).round().astype(int).clip(upper=THEORY_MAX)
        df[f"{s}_practical"] = obtained - df[f"{s}_theory"]

    # --- Totals & Percentage ---
    df["grand_total"] = df[SUBJECTS].sum(axis=1)
    df["max_total"]   = SUBJECT_MAX * len(SUBJECTS)
    df["average"]     = df[SUBJECTS].mean(axis=1).round(2)
    df["percentage"]  = (df["grand_total"] / df["max_total"] * 100).round(2)

    # --- Grades ---
    df["grade"] = df["percentage"].apply(get_grade)

    # --- Pass / Fail (any subject below PASS_MARK -> FAIL) ---
    df["status"] = (
        df[SUBJECTS].apply(lambda row: "PASS" if row.min() >= PASS_MARK else "FAIL", axis=1)
    )

    # --- Remarks ---
    df["remarks"] = df["grade"].map(REMARKS_MAP)
    df.loc[df["status"] == "FAIL", "remarks"] = "Result: FAIL. Attend remedial classes."

    # --- Rankings ---
    df["overall_rank"] = (
        df["grand_total"].rank(ascending=False, method="min").astype(int)
    )
    for s in SUBJECTS:
        df[f"{s}_rank"] = (
            df[s].rank(ascending=False, method="min").astype(int)
        )

    return df


# ------------------------- SEARCH -----------------------
def search_student(df, query):
    """Case-insensitive name match OR exact roll match. Returns filtered DataFrame."""
    q = str(query).strip().lower()
    mask = (
        df["Student Name"].str.lower().str.contains(q, na=False)
        | (df["Roll Number"].astype(str) == q)
    )
    return df[mask]


# ------------------------- SINGLE-STUDENT DICT -----------
def calculate_results(row):
    subjects = []
    for s in SUBJECTS:
        pct = row[s] / SUBJECT_MAX * 100
        subjects.append({
            "name":      s,
            "theory":    int(row[f"{s}_theory"]),
            "practical": int(row[f"{s}_practical"]),
            "total":     int(row[s]),
            "max":       SUBJECT_MAX,
            "grade":     get_grade(pct),
        })

    return {
        "name":      row["Student Name"],
        "roll":      int(row["Roll Number"]),
        "class":     int(row["Class"]),
        "section":   row["Section"],
        "subjects":  subjects,
        "total":     int(row["grand_total"]),
        "max_total": SUBJECT_MAX * len(SUBJECTS),
        "average":   round(float(row["average"]), 2),
        "percentage": round(float(row["percentage"]), 2),
        "grade":     row["grade"],
        "status":    row["status"],
        "remarks":   row["remarks"],
    }


# ------------------------- RANKS ------------------------
def compute_ranks(df):
    """Extract rank dicts from the already-processed DataFrame.
    Returns {"overall": {roll: rank}, "subjects": {"English": {roll: rank}, ...}}"""
    overall = dict(zip(df["Roll Number"], df["overall_rank"]))
    subjects = {
        s: dict(zip(df["Roll Number"], df[f"{s}_rank"]))
        for s in SUBJECTS
    }
    return {"overall": overall, "subjects": subjects}
