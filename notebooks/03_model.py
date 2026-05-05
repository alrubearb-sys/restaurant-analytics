# 03_model.py
# Binary classification: predict whether a restaurant will have high rating (>=4.0)
# Features: price range, delivery, takeout, reservations, outdoor seating, review count

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score
import joblib

CLEAN_DIR = Path("data/cleaned")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

FEATURES = ["pricerange2", "delivery", "takeout", "reservations",
            "outdoorseating", "review_count", "is_open"]
TARGET = "high_rating"


def load_and_prepare(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    df = df.copy()
    df[TARGET] = (df["stars"] >= 4.0).astype(int)

    bool_cols = ["delivery", "takeout", "reservations", "outdoorseating"]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].map({"True": 1, "False": 0, True: 1, False: 0})

    if "pricerange2" in df.columns:
        df["pricerange2"] = pd.to_numeric(df["pricerange2"], errors="coerce")

    df = df[FEATURES + [TARGET]].dropna()
    return df[FEATURES], df[TARGET]


def train_and_evaluate(X: pd.DataFrame, y: pd.Series):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=500, random_state=42),
        "random_forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_prob)
        print(f"\n--- {name} ---")
        print(classification_report(y_test, y_pred))
        print(f"ROC-AUC: {auc:.3f}")
        results[name] = {"model": model, "auc": auc}

    best_name = max(results, key=lambda k: results[k]["auc"])
    best_model = results[best_name]["model"]
    print(f"\nBest model: {best_name} (AUC={results[best_name]['auc']:.3f})")

    out_path = MODEL_DIR / "best_model.joblib"
    joblib.dump({"model": best_model, "features": FEATURES}, out_path)
    print(f"Model saved to {out_path}")

    if hasattr(best_model, "feature_importances_"):
        importances = pd.Series(best_model.feature_importances_, index=FEATURES)
        print("\nFeature importances:")
        print(importances.sort_values(ascending=False).to_string())

    return best_model


def main():
    print("Loading data...")
    df = pd.read_csv(CLEAN_DIR / "restaurants_clean.csv")
    print(f"  Rows: {len(df):,}")

    X, y = load_and_prepare(df)
    print(f"  Training samples: {len(X):,}")
    print(f"  Class balance: {y.mean()*100:.1f}% high-rated")

    train_and_evaluate(X, y)


if __name__ == "__main__":
    main()
