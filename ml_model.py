import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings("ignore")


def predict_performance(filepath: str) -> dict:
    """
    Predicts each student's performance trend: Improving / Stable / At Risk.

    Strategy:
      - Uses subject marks as features.
      - Derives a synthetic trend label based on variance + percentage:
          • High % + low variance  → Stable
          • High %                 → Improving
          • Low % or failing subs  → At Risk
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

    roll_col = _find_col(df, ["roll", "roll_number", "rollno", "id"])
    name_col = _find_col(df, ["name", "student_name", "student"])
    exclude = {"total", "percentage", "pass", "fail", "grade", "result", "prediction"}
    subject_cols = [
        c for c in df.columns
        if c.lower() not in exclude
        and c != roll_col
        and c != name_col
        and pd.api.types.is_numeric_dtype(df[c])
    ]

    if len(subject_cols) < 2:
        return {"error": "Need at least 2 subjects for trend prediction."}

    X = df[subject_cols].copy().fillna(0)
    total_max = 100 * len(subject_cols)
    percentages = X.sum(axis=1) / total_max * 100
    variances = X.std(axis=1)
    failed_subjects = (X < 35).sum(axis=1)

    # Synthetic label logic
    labels = []
    for pct, var, fails in zip(percentages, variances, failed_subjects):
        if fails > 0 or pct < 40:
            labels.append("At Risk")
        elif pct >= 70 and var <= 15:
            labels.append("Stable")
        elif pct >= 55:
            labels.append("Improving")
        else:
            labels.append("At Risk")

    df["_trend_label"] = labels

    le = LabelEncoder()
    y = le.fit_transform(labels)

    # Only train/predict if we have enough varied data
    unique_labels = len(set(labels))
    if unique_labels < 2 or len(df) < 5:
        # Fallback: just return rule-based labels
        predictions = _build_predictions(df, labels, subject_cols, roll_col, name_col)
        return {
            "predictions": predictions,
            "model_used": "Rule-based (insufficient data for ML)",
            "feature_importances": {},
        }

    # Train Random Forest
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if len(df) > 10 else None
        )
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X)
        predicted_labels = le.inverse_transform(y_pred)

        # Feature importances
        importances = {
            sub: round(float(imp), 4)
            for sub, imp in zip(subject_cols, clf.feature_importances_)
        }
        # Sort descending
        importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))

        predictions = _build_predictions(
            df, predicted_labels, subject_cols, roll_col, name_col
        )

        return {
            "predictions": predictions,
            "model_used": "Random Forest Classifier",
            "feature_importances": importances,
            "trend_summary": {
                "Improving": int(sum(1 for p in predicted_labels if p == "Improving")),
                "Stable": int(sum(1 for p in predicted_labels if p == "Stable")),
                "At Risk": int(sum(1 for p in predicted_labels if p == "At Risk")),
            },
        }
    except Exception as e:
        return {"error": f"ML prediction failed: {str(e)}"}


def _build_predictions(df, labels, subject_cols, roll_col, name_col):
    predictions = []
    for i, (_, row) in enumerate(df.iterrows()):
        trend = labels[i]
        predictions.append({
            "roll_number": str(row[roll_col]) if roll_col else str(i + 1),
            "name": str(row[name_col]) if name_col else f"Student {i + 1}",
            "trend": trend,
            "trend_icon": _trend_icon(trend),
            "trend_color": _trend_color(trend),
        })
    return predictions


def _trend_icon(trend: str) -> str:
    return {"Improving": "↑", "Stable": "→", "At Risk": "↓"}.get(trend, "?")


def _trend_color(trend: str) -> str:
    return {
        "Improving": "#22c55e",
        "Stable": "#3b82f6",
        "At Risk": "#ef4444",
    }.get(trend, "#6b7280")


def _find_col(df, candidates):
    for col in df.columns:
        if col.strip().lower().replace(" ", "_") in candidates:
            return col
    return None