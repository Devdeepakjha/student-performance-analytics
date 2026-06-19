import pandas as pd
import numpy as np


def analyze_csv(filepath: str) -> dict:
    """
    Reads student marks CSV and returns a rich analytics dictionary.
    """

    # Read CSV or Excel file
    if filepath.lower().endswith(".csv"):
        df = pd.read_csv(filepath)

    elif filepath.lower().endswith(
        (".xlsx", ".xls")
    ):
        df = pd.read_excel(filepath)

    else:
        raise ValueError(
            "Unsupported file format"
        )

    df.columns = df.columns.str.strip()

    # --- Identify columns ---
    roll_col = _find_col(df, ["roll", "roll_number", "rollno", "id"])
    name_col = _find_col(df, ["name", "student_name", "student"])

    # Subject columns = numeric columns that are NOT roll/total/percentage/pass columns
    exclude = {"total", "percentage", "pass", "fail", "grade", "result", "prediction"}
    subject_cols = [
        c for c in df.columns
        if c.lower() not in exclude
        and c != roll_col
        and c != name_col
        and pd.api.types.is_numeric_dtype(df[c])
    ]

    if not subject_cols:
        raise ValueError(
            "No numeric subject columns found. Ensure subject marks are numeric."
        )

    max_per_subject = 100  # assumed; adjust if needed
    total_max = max_per_subject * len(subject_cols)

    # --- Computed columns ---
    df["Total"] = df[subject_cols].sum(axis=1)
    df["Percentage"] = (df["Total"] / total_max * 100).round(2)
    df["Pass"] = df[subject_cols].apply(lambda row: (row >= 35).all(), axis=1)
    df["Grade"] = df["Percentage"].apply(_assign_grade)

    # --- Students list (for search) ---
    students = []
    for _, row in df.iterrows():
        s = {
            "roll_number": str(row[roll_col]) if roll_col else str(_),
            "name": str(row[name_col]) if name_col else f"Student {_}",
            "total": float(row["Total"]),
            "percentage": float(row["Percentage"]),
            "pass": bool(row["Pass"]),
            "grade": row["Grade"],
        }
        for sub in subject_cols:
            s[sub] = float(row[sub])
        students.append(s)

    # --- Class stats ---
    pass_count = int(df["Pass"].sum())
    fail_count = len(df) - pass_count

    # --- Topper ---
    topper_idx = df["Total"].idxmax()
    topper = {
        "name": str(df.loc[topper_idx, name_col]) if name_col else f"Row {topper_idx}",
        "roll_number": str(df.loc[topper_idx, roll_col]) if roll_col else str(topper_idx),
        "total": float(df.loc[topper_idx, "Total"]),
        "percentage": float(df.loc[topper_idx, "Percentage"]),
    }

    # --- Top 5 ---
    top5_df = df.nlargest(5, "Total")
    top5 = []
    for rank, (_, row) in enumerate(top5_df.iterrows(), 1):
        top5.append({
            "rank": rank,
            "name": str(row[name_col]) if name_col else f"Row {_}",
            "roll_number": str(row[roll_col]) if roll_col else str(_),
            "total": float(row["Total"]),
            "percentage": float(row["Percentage"]),
            "grade": row["Grade"],
        })

    # --- Subject averages ---
    subject_averages = {sub: round(float(df[sub].mean()), 2) for sub in subject_cols}

    # --- Grade distribution ---
    grade_dist = df["Grade"].value_counts().to_dict()

    # --- Chart data (for JS charts) ---
    percentage_bins = [0, 35, 50, 60, 75, 90, 100]
    bin_labels = ["0-35", "35-50", "50-60", "60-75", "75-90", "90-100"]
    hist_counts, _ = np.histogram(df["Percentage"].values, bins=percentage_bins)
    percentage_distribution = {
        "labels": bin_labels,
        "data": hist_counts.tolist(),
    }

    return {
        "total_students": len(df),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "pass_percentage": round(pass_count / len(df) * 100, 1),
        "class_average": round(float(df["Percentage"].mean()), 2),
        "highest_score": float(df["Percentage"].max()),
        "lowest_score": float(df["Percentage"].min()),
        "topper": topper,
        "top5": top5,
        "subject_averages": subject_averages,
        "subjects": subject_cols,
        "grade_distribution": grade_dist,
        "percentage_distribution": percentage_distribution,
        "students": students,
    }


def _find_col(df: pd.DataFrame, candidates: list) -> str | None:
    for col in df.columns:
        if col.strip().lower().replace(" ", "_") in candidates:
            return col
    return None


def _assign_grade(pct: float) -> str:
    if pct >= 90:
        return "A+"
    elif pct >= 80:
        return "A"
    elif pct >= 70:
        return "B+"
    elif pct >= 60:
        return "B"
    elif pct >= 50:
        return "C"
    elif pct >= 35:
        return "D"
    else:
        return "F"