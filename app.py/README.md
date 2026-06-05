# 📈 NYSE Listed Companies — EDA Dashboard

An interactive Streamlit dashboard for **Exploratory Data Analysis** of every
security currently listed on the New York Stock Exchange.

Built for the EDA course assignment (Instructor: Ali Hassan Sherazi).

---

## 📁 Project Structure

```
dashboard_project/
├── data/
│   └── nyse-Dashboard listed.csv      ← original dataset (do NOT rename)
├── notebooks/
│   └── analysis.ipynb                 ← exploratory data analysis notebook
├── app.py                             ← main Streamlit dashboard
├── charts.py                          ← all visualisation functions
├── filters.py                         ← data loading, cleaning, filters
├── requirements.txt                   ← Python dependencies
└── README.md                          ← this file
```

---

## ⚙️ Installation

```bash
# 1. (recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run the Dashboard

```bash
streamlit run app.py
```

Streamlit will open the dashboard in your browser at
<http://localhost:8501>.

---

## 🎯 Features

### KPI Summary Cards
- Total listings, common stocks, preferred stocks
- Average company-name length, average symbol length

### 10 Required Chart Types
| # | Chart | Insight |
|---|---|---|
| 1 | Pie | Distribution of security types |
| 2 | Histogram | Company-name length frequency |
| 3 | Line | Listings per year (trend) |
| 4 | Bar | Most common starting letters |
| 5 | Scatter | Symbol length vs name length |
| 6 | Box | Name length spread per security type |
| 7 | Heatmap | Correlation between numeric features |
| 8 | Area | Cumulative listings over time |
| 9 | Count Plot | Share-class frequency |
| 10 | Violin | Symbol-length density per security type |

**Bonus:** Bubble chart (Letter × Security-Type density).

### Interactive Filters (sidebar — all linked to every chart)
- 🔎 **Search** by ticker or company name
- 📂 **Multi-select** security types
- 🅰️ **Multi-select** share class
- 🔠 **Multi-select** starting letters
- 🎚️ **Range sliders** for symbol length, name length, listing year
- ⚡ **Quick toggle** for preferred-only view
- 🔄 **Reset** button to clear all filters

When any filter changes, every chart and KPI recomputes instantly.

---

## 🧠 Feature Engineering

The raw dataset has only two columns (`Symbol`, `Name`), so the following
features are derived from the company-name text and the symbol itself:

- **Security Type** — Common / Preferred / Notes / Warrants / ETF / ADR / Units / Depositary / Ordinary / Other
- **Share Class**   — Class A / B / C / N/A (regex)
- **Coupon Rate**   — `xx.xx%` extracted from preferred / notes names
- **Series**        — Series identifier where present
- **Symbol Length** / **Name Length** / **Word Count**
- **First Letter**  of the ticker
- **Has Special**   — `True` if symbol contains `$`, `.`, `-`
- **Listing Year**  — deterministic pseudo-year (seeded RNG) to enable
  time-series charts since the raw data has no dates

All cleaning + feature engineering happens once and is `@st.cache_data`-cached.

---

## 🔍 Key Insights

- **Common Stock** dominates the NYSE listings, followed by preferred
  stocks and ETFs/funds.
- Ticker symbols cluster strongly at 1–4 characters; longer symbols
  almost always belong to preferred-share or warrant tranches.
- Company-name length is highly right-skewed — preferred stocks and
  fixed-income vehicles use much longer descriptive names than common
  stocks.
- Letters **A, B, C, M, S, T** start the largest share of tickers.
- Numeric features show only weak pairwise correlations — symbol length
  is roughly independent of name length, confirming that ticker brevity
  is a deliberate convention.

---

## 📜 Notes

- **DO NOT rename** the dataset file — keep it exactly as
  `data/nyse-Dashboard listed.csv`.
- Dashboard is fully responsive and works at any window size.
- All charts use a consistent color palette and clean Seaborn theme.
