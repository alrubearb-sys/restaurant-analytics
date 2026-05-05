# streamlit_app.py
# Run: streamlit run app/streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path

DATA_PATH = Path("data/cleaned/restaurants_clean.csv")
MODEL_PATH = Path("models/best_model.joblib")

st.set_page_config(page_title="Restaurant Analytics", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None


def page_overview(df):
    st.title("Restaurant Performance Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Restaurants", f"{len(df):,}")
    col2.metric("Avg Rating", f"{df['stars'].mean():.2f}")
    col3.metric("Currently Open", f"{df['is_open'].sum():,}")
    col4.metric("Survival Rate", f"{df['is_open'].mean()*100:.1f}%")

    st.subheader("Rating Distribution")
    fig, ax = plt.subplots(figsize=(8, 3))
    df["stars"].value_counts().sort_index().plot(kind="bar", ax=ax, color="#4C72B0", edgecolor="white")
    ax.set_xlabel("Stars")
    ax.set_ylabel("Count")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("Top 15 Cities")
    top_cities = df.groupby("city").agg(
        restaurants=("business_id", "count"),
        avg_rating=("stars", "mean")
    ).sort_values("restaurants", ascending=False).head(15).reset_index()
    top_cities["avg_rating"] = top_cities["avg_rating"].round(2)
    st.dataframe(top_cities, use_container_width=True, hide_index=True)


def page_operational(df):
    st.title("Operational Insights")
    st.write("Filter by city to explore how ratings and price distribution vary by market.")

    st.sidebar.header("Filters")
    city_counts = df["city"].dropna().value_counts()
    city_options = ["All"] + [f"{c} ({city_counts[c]:,})" for c in city_counts.index]
    city_label = st.sidebar.selectbox("City", city_options)

    selected_city = None if city_label == "All" else city_label.rsplit(" (", 1)[0]
    if selected_city:
        df = df[df["city"] == selected_city]

    n = len(df)
    st.metric("Filtered Restaurants", f"{n:,}")

    if selected_city:
        if n < 30:
            st.warning(
                f"Small sample: {selected_city} has only {n} restaurants. "
                "Averages are not statistically reliable."
            )
        elif n < 100:
            st.info(
                f"Limited sample: {selected_city} has {n} restaurants. "
                "Interpret averages with caution."
            )

    st.subheader("Rating by Price Range")
    if "pricerange2" in df.columns:
        df_p = df[df["pricerange2"].notna()].copy()
        df_p["pricerange2"] = df_p["pricerange2"].astype(str)
        fig, ax = plt.subplots(figsize=(7, 3))
        sns.boxplot(data=df_p, x="pricerange2", y="stars",
                    order=["1.0", "2.0", "3.0", "4.0"], ax=ax)
        ax.set_xlabel("Price Range (1=cheap, 4=expensive)")
        ax.set_ylabel("Stars")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


def page_predictor(df):
    st.title("Experimental: Rating Predictor")
    st.warning(
        "**Exploratory model — not predictive in practice.** "
        "This logistic regression achieves AUC 0.65 on held-out data (random baseline = 0.50). "
        "Operational attributes alone explain little of the variance in ratings. "
        "Included here to illustrate the modelling step, not as a decision tool."
    )
    st.write("Input a restaurant's operational profile to see the model output.")

    artifact = load_model()
    if artifact is None:
        st.warning("Model not found. Run `python notebooks/03_model.py` first.")
        return

    model = artifact["model"]
    features = artifact["features"]

    col1, col2 = st.columns(2)
    with col1:
        price_range = st.selectbox(
            "Price Range",
            [1, 2, 3, 4],
            format_func=lambda x: {
                1: "1 — Budget (fast food, takeaway)",
                2: "2 — Mid-range (casual dining)",
                3: "3 — Upper-mid (upscale casual)",
                4: "4 — Premium (fine dining)",
            }[x],
        )
        delivery = st.selectbox("Offers Delivery?", ["Yes", "No"])
        takeout = st.selectbox("Offers Takeout?", ["Yes", "No"])
    with col2:
        reservations = st.selectbox("Takes Reservations?", ["Yes", "No"])
        outdoor = st.selectbox("Outdoor Seating?", ["Yes", "No"])
        review_count = st.number_input(
            "Number of Yelp reviews",
            min_value=1, value=50,
            help="Total reviews the restaurant has received on Yelp. More reviews generally means more established."
        )
        is_open = st.selectbox(
            "Still operating?",
            ["Yes", "No"],
            help="Whether the restaurant is currently open for business (not permanently closed)."
        )

    def yn(val):
        return 1 if val == "Yes" else 0

    input_data = pd.DataFrame([{
        "pricerange2": float(price_range),
        "delivery": yn(delivery),
        "takeout": yn(takeout),
        "reservations": yn(reservations),
        "outdoorseating": yn(outdoor),
        "review_count": float(review_count),
        "is_open": yn(is_open),
    }])[features]

    if st.button("Predict"):
        prob = model.predict_proba(input_data)[0][1]
        prediction = "HIGH RATING (>=4.0 stars)" if prob >= 0.5 else "LOW RATING (<4.0 stars)"
        color = "green" if prob >= 0.5 else "red"
        st.markdown(f"### Prediction: :{color}[{prediction}]")
        st.metric("Probability of High Rating", f"{prob*100:.1f}%")


def page_findings(df):
    st.title("Key Findings & Business Implications")
    st.write(
        f"Based on **{len(df):,} restaurants** across **{df['city'].nunique():,} cities**. "
        "Findings are descriptive — correlations, not causal claims."
    )
    st.divider()

    # Finding 1 — Delivery
    st.subheader("1. Delivery correlates with lower ratings")
    c1, c2, c3 = st.columns(3)
    c1.metric("With Delivery", "3.41 ★", delta=None)
    c2.metric("Without Delivery", "3.63 ★", delta=None)
    c3.metric("Gap", "−0.22 ★", delta="-0.22", delta_color="inverse")
    st.info(
        "**What this means:** Adding delivery is a volume play, not a quality signal. "
        "Restaurants offering delivery trade experience for convenience — "
        "operators expecting ratings to improve by adding delivery are likely to be disappointed. "
        "Focus on in-venue execution first."
    )
    st.divider()

    # Finding 2 — Outdoor seating
    st.subheader("2. Outdoor seating shows the strongest positive signal")
    c1, c2, c3 = st.columns(3)
    c1.metric("With Outdoor Seating", "3.67 ★")
    c2.metric("Without Outdoor Seating", "3.41 ★")
    c3.metric("Gap", "+0.26 ★", delta="+0.26")
    st.info(
        "**What this means:** Across 46,000+ restaurants with known seating data, "
        "outdoor seating consistently accompanies higher ratings. "
        "For operators choosing or renovating a venue, this is worth weighing — "
        "it may reflect ambiance, dining experience, or customer segment differences."
    )
    st.divider()

    # Finding 3 — Reservations
    st.subheader("3. Restaurants accepting reservations rate higher")
    c1, c2, c3 = st.columns(3)
    c1.metric("Takes Reservations", "3.65 ★")
    c2.metric("No Reservations", "3.43 ★")
    c3.metric("Gap", "+0.22 ★", delta="+0.22")
    st.info(
        "**What this means:** Reservations signal a sit-down, experience-focused operation. "
        "The pattern likely reflects that full-service restaurants attract customers "
        "with higher expectations — and meet them. Fast-casual and counter-service formats "
        "face a structural rating ceiling in this dataset."
    )
    st.divider()

    # Finding 4 — Price range
    st.subheader("4. Mid-range pricing outperforms both budget and premium")

    price_data = {"Price Range": ["1 - Budget", "2 - Mid", "3 - Upper-Mid", "4 - Premium"],
                  "Avg Rating": [3.38, 3.60, 3.60, 3.43],
                  "Restaurants": [24552, 29817, 2306, 306]}
    price_df = pd.DataFrame(price_data)

    fig, ax = plt.subplots(figsize=(7, 3))
    colors = ["#aec6cf", "#4C72B0", "#4C72B0", "#aec6cf"]
    ax.bar(price_df["Price Range"], price_df["Avg Rating"], color=colors, edgecolor="white")
    ax.set_ylim(3.2, 3.75)
    ax.set_ylabel("Avg Rating")
    ax.axhline(3.55, color="gray", linestyle="--", linewidth=0.8, label="Dataset avg (3.55)")
    ax.legend(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.info(
        "**What this means:** Mid-range and upper-mid restaurants both average 3.60★ and outperform "
        "the cheapest (3.38★) and most expensive (3.43★) tiers. "
        "The premium penalty is real — high prices raise expectations that are difficult to consistently meet at scale."
    )
    st.divider()

    # Summary table
    st.subheader("Summary: Operational attribute impact on average rating")
    summary = pd.DataFrame({
        "Attribute": ["Outdoor Seating", "Reservations", "Delivery", "Takeout"],
        "With": [3.67, 3.65, 3.41, 3.54],
        "Without": [3.41, 3.43, 3.63, 3.40],
        "Delta": ["+0.26", "+0.22", "−0.22", "+0.14"],
        "Direction": ["Positive", "Positive", "Negative", "Positive"],
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.caption(
        f"Dataset: Yelp Open Dataset · {len(df):,} restaurants · {df['city'].nunique():,} cities. "
        "Correlations only — no causal claims."
    )


def main():
    df = load_data()

    pages = {
        "Key Findings": page_findings,
        "Overview": page_overview,
        "Operational Insights": page_operational,
        "Experimental: Rating Predictor": page_predictor,
    }

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", list(pages.keys()))
    pages[page](df)


if __name__ == "__main__":
    main()
