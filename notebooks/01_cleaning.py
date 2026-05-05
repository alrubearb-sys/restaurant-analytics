# 01_cleaning.py
# Load Yelp JSON files, filter to restaurants, clean and export to CSV

import json
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/cleaned")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

RESTAURANT_CATEGORIES = ["Restaurants", "Food", "Bars", "Cafes", "Nightlife"]


def load_businesses(filepath: Path) -> pd.DataFrame:
    records = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    return pd.DataFrame(records)


def filter_restaurants(df: pd.DataFrame) -> pd.DataFrame:
    mask = df["categories"].str.contains(
        "|".join(RESTAURANT_CATEGORIES), case=False, na=False
    )
    return df[mask].copy()


def clean_businesses(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "business_id", "name", "city", "state", "stars",
        "review_count", "is_open", "categories", "attributes", "hours"
    ]
    df = df[cols].copy()
    df.columns = [c.lower() for c in df.columns]
    df["stars"] = pd.to_numeric(df["stars"], errors="coerce")
    df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")
    df["is_open"] = df["is_open"].astype(int)
    df["rating_tier"] = pd.cut(
        df["stars"],
        bins=[0, 2.5, 3.5, 4.0, 5.0],
        labels=["low", "medium", "high", "top"]
    )
    return df


def extract_attributes(df: pd.DataFrame) -> pd.DataFrame:
    attr_keys = ["RestaurantsPriceRange2", "RestaurantsDelivery",
                 "RestaurantsTakeOut", "RestaurantsReservations",
                 "OutdoorSeating", "WiFi"]
    for key in attr_keys:
        col = key.replace("Restaurants", "").lower()
        df[col] = df["attributes"].apply(
            lambda x: x.get(key) if isinstance(x, dict) else None
        )
    return df.drop(columns=["attributes", "hours"])


def main():
    print("Loading business data...")
    df_raw = load_businesses(RAW_DIR / "yelp_academic_dataset_business.json")
    print(f"  Total businesses: {len(df_raw):,}")

    df_rest = filter_restaurants(df_raw)
    print(f"  Restaurants filtered: {len(df_rest):,}")

    df_clean = clean_businesses(df_rest)
    df_clean = extract_attributes(df_clean)

    out_path = CLEAN_DIR / "restaurants_clean.csv"
    df_clean.to_csv(out_path, index=False)
    print(f"  Saved to {out_path}")
    print(f"  Columns: {list(df_clean.columns)}")
    print(f"  Missing values:\n{df_clean.isnull().sum()[df_clean.isnull().sum() > 0]}")


if __name__ == "__main__":
    main()
