# Restaurant Analytics — What Makes a Restaurant Succeed?

## Overview
End-to-end analysis of 150k+ restaurants from the Yelp Open Dataset to identify the operational and structural factors that separate high-rated restaurants from low-rated ones.

**Business questions:**
1. What operational attributes (price, delivery, reservations) correlate with higher ratings?
2. Which cities have the highest restaurant survival rates?
3. Can we predict whether a restaurant will achieve a high rating based on its operational profile?

## Dataset
- Source: [Yelp Open Dataset](https://www.yelp.com/dataset)
- Scope: restaurant and food businesses across multiple US/Canada cities
- Key fields: stars, review_count, is_open, price range, delivery, takeout, reservations, outdoor seating

## Tech Stack
- **Python** — data cleaning, EDA, feature engineering, classification model
- **SQL (SQLite)** — business query layer (12 queries)
- **Streamlit** — interactive dashboard with live rating predictor

## Project Structure
```
project3_restaurant_analytics/
├── data/
│   ├── raw/                    ← Yelp JSON (not tracked in git)
│   └── cleaned/
│       └── restaurants_clean.csv
├── notebooks/
│   ├── 01_cleaning.py
│   ├── 02_eda.py
│   └── 03_model.py
├── sql/
│   └── queries.sql
├── app/
│   └── streamlit_app.py
├── models/
│   └── best_model.joblib
├── outputs/figures/
├── requirements.txt
└── ROADMAP.md
```

## How to Run

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Place Yelp dataset file in `data/raw/`**
```
data/raw/yelp_academic_dataset_business.json
```

**3. Run pipeline**
```bash
python notebooks/01_cleaning.py
python notebooks/02_eda.py
python notebooks/03_model.py
```

**4. Launch dashboard**
```bash
streamlit run app/streamlit_app.py
```

## Dashboard
Three pages:
- **Overview** — KPI cards, rating distribution, top cities
- **Operational Insights** — how price, delivery, and reservations affect ratings
- **Rating Predictor** — input a restaurant's attributes and get a prediction

Live app: *[link after deployment]*

## Key Findings
*To be updated with real data after running the pipeline.*

## CV Bullet
*To be updated with real metrics after running the pipeline.*
