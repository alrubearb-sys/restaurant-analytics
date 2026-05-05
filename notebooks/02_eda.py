# 02_eda.py
# Exploratory analysis: ratings distribution, cuisine types, operational attributes

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

CLEAN_DIR = Path("data/cleaned")
FIG_DIR = Path("outputs/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")


def load_data() -> pd.DataFrame:
    return pd.read_csv(CLEAN_DIR / "restaurants_clean.csv")


def plot_rating_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    df["stars"].value_counts().sort_index().plot(kind="bar", ax=ax, color="#4C72B0")
    ax.set_title("Rating Distribution")
    ax.set_xlabel("Stars")
    ax.set_ylabel("Number of Restaurants")
    plt.tight_layout()
    fig.savefig(FIG_DIR / "rating_distribution.png", dpi=150)
    plt.close()
    print("  Saved rating_distribution.png")


def plot_top_cities(df: pd.DataFrame, n: int = 15):
    top = df["city"].value_counts().head(n)
    fig, ax = plt.subplots(figsize=(10, 5))
    top.plot(kind="barh", ax=ax, color="#4C72B0")
    ax.invert_yaxis()
    ax.set_title(f"Top {n} Cities by Restaurant Count")
    ax.set_xlabel("Count")
    plt.tight_layout()
    fig.savefig(FIG_DIR / "top_cities.png", dpi=150)
    plt.close()
    print("  Saved top_cities.png")


def plot_price_vs_rating(df: pd.DataFrame):
    col = "pricerange2"
    if col not in df.columns:
        print("  pricerange2 column not found, skipping.")
        return
    df_plot = df[df[col].notna()].copy()
    df_plot[col] = df_plot[col].astype(float).astype(int).astype(str)
    order = [v for v in ["1", "2", "3", "4"] if v in df_plot[col].unique()]
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(data=df_plot, x=col, y="stars", ax=ax, order=order)
    ax.set_title("Rating by Price Range")
    ax.set_xlabel("Price Range (1=cheap, 4=expensive)")
    ax.set_ylabel("Stars")
    plt.tight_layout()
    fig.savefig(FIG_DIR / "price_vs_rating.png", dpi=150)
    plt.close()
    print("  Saved price_vs_rating.png")


def plot_operational_impact(df: pd.DataFrame):
    features = ["delivery", "takeout", "reservations", "outdoorseating"]
    fig, axes = plt.subplots(1, len(features), figsize=(14, 4), sharey=True)
    for ax, feat in zip(axes, features):
        if feat not in df.columns:
            continue
        df_f = df[df[feat].notna()].copy()
        df_f[feat] = df_f[feat].astype(str)
        sns.boxplot(data=df_f, x=feat, y="stars", ax=ax)
        ax.set_title(feat.capitalize())
        ax.set_xlabel("")
    fig.suptitle("Rating by Operational Attribute")
    plt.tight_layout()
    fig.savefig(FIG_DIR / "operational_impact.png", dpi=150)
    plt.close()
    print("  Saved operational_impact.png")


def main():
    print("Loading cleaned data...")
    df = load_data()
    print(f"  Rows: {len(df):,}")

    print("\nKey stats:")
    print(f"  Avg rating: {df['stars'].mean():.2f}")
    print(f"  Open restaurants: {df['is_open'].sum():,} ({df['is_open'].mean()*100:.1f}%)")
    print(f"  Cities: {df['city'].nunique()}")

    print("\nGenerating plots...")
    plot_rating_distribution(df)
    plot_top_cities(df)
    plot_price_vs_rating(df)
    plot_operational_impact(df)
    print("\nEDA complete.")


if __name__ == "__main__":
    main()
