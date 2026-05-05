# Project Roadmap — Restaurant Analytics

## Objective
Analyze 150k+ real restaurants from the Yelp Open Dataset to answer:
**What operational and structural factors separate high-rated restaurants from low-rated ones?**

Deliverable: end-to-end Python + SQL + Streamlit project deployable as a live app.

---

## Status Legend
- [ ] Not started
- [~] In progress
- [x] Done

---

## Phase 1 — Setup & Data Acquisition
- [x] Download Yelp Open Dataset from yelp.com/dataset (free, requires registration)
- [x] Place `yelp_academic_dataset_business.json` in `data/raw/`
- [x] Install dependencies: `pip install pandas numpy matplotlib seaborn scikit-learn joblib streamlit`
- [x] Rename folder from `project3_sales` → `project3_restaurant_analytics`

**Checkpoint:** `data/raw/yelp_academic_dataset_business.json` exists and is readable. ✓

---

## Phase 2 — Data Cleaning (Python)
**Script:** `notebooks/01_cleaning.py`

- [x] Load raw JSON (line-by-line for memory efficiency)
- [x] Filter to restaurant/food businesses (~50-60k records expected)
- [x] Standardize column names to snake_case
- [x] Extract operational attributes from nested dict (`attributes` column)
- [x] Engineer `rating_tier` column (low / medium / high / top)
- [x] Export `data/cleaned/restaurants_clean.csv`

**Checkpoint:** 150,346 raw → 67,578 restaurants. 15 columns. ✓

---

## Phase 3 — Exploratory Analysis (Python)
**Script:** `notebooks/02_eda.py`

- [x] Rating distribution plot
- [x] Top 15 cities by restaurant count
- [x] Price range vs. rating boxplot
- [x] Operational attributes impact on rating (delivery, takeout, reservations, outdoor)
- [x] Save all figures to `outputs/figures/`

**Checkpoint:** 4 figures en `outputs/figures/`. Avg rating 3.55★, 1,009 ciudades, 69.1% abiertos. ✓

---

## Phase 4 — SQL Analysis Layer
**Script:** `sql/queries.sql`

- [x] Import cleaned CSV into SQLite (`restaurant.db`)
- [x] Run all 12 queries and verify results
- [x] Document key findings as comments next to each query

Queries cover: overall summary, rating distribution, city rankings, survival rate, price range impact, delivery/reservations effect, operational matrix, high-rating profile.

**Checkpoint:** 12/12 queries sin errores. Hallazgo clave: delivery correlaciona negativamente con rating (3.41 vs 3.63). ✓

---

## Phase 5 — Predictive Model (Python)
**Script:** `notebooks/03_model.py`

- [x] Define binary target: `high_rating` = 1 if stars >= 4.0
- [x] Features: price range, delivery, takeout, reservations, outdoor seating, review count, is_open
- [x] Train Logistic Regression and Random Forest
- [x] Evaluate with classification report + ROC-AUC
- [x] Save best model to `models/best_model.joblib`
- [x] Document feature importances (what matters most)

**Checkpoint:** Logistic Regression AUC=0.650 (ganó vs Random Forest 0.608). Modelo guardado. ✓

---

## Phase 6 — Streamlit Dashboard
**Script:** `app/streamlit_app.py`

- [ ] Page 1 — Overview: KPI cards, rating distribution, top cities
- [ ] Page 2 — Operational Insights: filters by city, attribute comparisons, survival rate
- [ ] Page 3 — Rating Predictor: form input → model prediction with probability
- [ ] Test locally: `streamlit run app/streamlit_app.py`
- [ ] Fix layout/display issues

**Checkpoint:** App runs locally, all 3 pages load without errors.

---

## Phase 7 — Deployment & Documentation
- [ ] Deploy to Streamlit Community Cloud (free, requires GitHub repo)
  - Push project to GitHub
  - Connect repo at share.streamlit.io
  - Set main file path: `app/streamlit_app.py`
- [ ] Write README.md with: project summary, key findings, tech stack, live app link
- [ ] Add `requirements.txt` for Streamlit Cloud
- [ ] Add screenshots of each dashboard page to README

**Checkpoint:** Live URL accessible from public internet.

---

## Phase 8 — Portfolio Integration
- [ ] Update CV bullet with live app URL and key metric
- [ ] Update LinkedIn Featured section with project link
- [ ] Write LinkedIn post (already drafted in reference — adapt with real findings)
- [ ] Verify GitHub README renders correctly

---

## Key Findings to Surface (targets — validate against real data)
- Does delivery/takeout correlate with higher or lower ratings?
- Do more expensive restaurants rate higher on average?
- What is the survival rate gap between high-rated and low-rated restaurants?
- What does the operational profile of a top-rated restaurant look like?

---

## File Structure
```
project3_restaurant_analytics/
├── data/
│   ├── raw/                        ← Yelp JSON files (not committed to git)
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
├── outputs/
│   └── figures/
├── requirements.txt
├── README.md
└── ROADMAP.md
```

---

## Requirements
```
pandas
numpy
matplotlib
seaborn
scikit-learn
joblib
streamlit
```

---

## Estimated Time per Phase
| Phase | Estimated Time |
|---|---|
| 1. Setup & Data | 1h |
| 2. Cleaning | 2h |
| 3. EDA | 2h |
| 4. SQL | 1h |
| 5. Model | 2-3h |
| 6. Streamlit | 3-4h |
| 7. Deploy & Docs | 2h |
| 8. Portfolio | 1h |
| **Total** | **~15h** |
