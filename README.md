# Restaurant Analytics — What Makes a Restaurant Succeed?

**Live dashboard:** https://restaurant-analytics-d9ytpbxjufavbentta2wad.streamlit.app/

End-to-end analysis of 67,578 restaurants from the Yelp Open Dataset to identify the operational and structural factors that separate high-rated restaurants from low-rated ones.

## Key Findings

| Finding | Data |
|---|---|
| Delivery correlates with lower ratings | 3.41★ with delivery vs 3.63★ without (−0.22★) |
| Outdoor seating shows the strongest positive signal | 3.67★ with vs 3.41★ without (+0.26★) |
| Reservations accompany higher ratings | 3.65★ vs 3.43★ (+0.22★) |
| Mid-range pricing outperforms budget and premium | $$ and $$$ both at 3.60★ vs $ at 3.38★ |
| 46.7% of restaurants achieve ≥4.0★ | Across 1,009 cities |

## Business Questions
1. What operational attributes (price, delivery, reservations) correlate with higher ratings?
2. Which cities have the highest restaurant concentration and average ratings?
3. Can operational profile alone predict whether a restaurant achieves a high rating?

## Dataset
- Source: [Yelp Open Dataset](https://www.yelp.com/dataset)
- Scope: 67,578 restaurant and food businesses across 1,009 cities
- Raw data: 150,346 businesses filtered to restaurants/food category

## Tech Stack
- **Python** — data cleaning, EDA, feature engineering (pandas, NumPy, Matplotlib, Seaborn, scikit-learn)
- **SQL (SQLite)** — business query layer (12 queries)
- **Streamlit** — interactive dashboard with live rating predictor

## Dashboard Pages
- **Key Findings** — 4 data-backed business implications in plain language
- **Overview** — KPI cards, rating distribution, top cities
- **Operational Insights** — filter by city, price range vs rating
- **Experimental: Rating Predictor** — logistic regression (AUC 0.65, exploratory only)

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
└── requirements.txt
```

## How to Run Locally
```bash
pip install -r requirements.txt
python notebooks/01_cleaning.py
python notebooks/02_eda.py
python notebooks/03_model.py
streamlit run app/streamlit_app.py
```
