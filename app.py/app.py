"""
app.py — NYSE Listed Companies EDA Dashboard
============================================

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from filters import load_data, sidebar_filters, apply_filters
from charts  import (
    apply_theme,
    pie_security_type,
    histogram_name_length,
    line_listings_per_year,
    bar_top_letters,
    scatter_symlen_vs_namelen,
    box_namelen_by_security,
    heatmap_correlation,
    area_cumulative_listings,
    count_share_class,
    violin_symlen_by_security,
    bubble_letter_security,
)

# ----------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="NYSE Listed Companies — EDA Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ----------------------------------------------------------------------
# Custom styling
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
      .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
      .kpi-card {
          background: linear-gradient(135deg,#0F172A 0%,#1E293B 100%);
          color: #F8FAFC;
          padding: 1.1rem 1.3rem;
          border-radius: 14px;
          box-shadow: 0 4px 14px rgba(15,23,42,0.10);
      }
      .kpi-label { font-size: 0.78rem; opacity: 0.75;
                   text-transform: uppercase; letter-spacing: .05em; }
      .kpi-value { font-size: 1.7rem; font-weight: 700; margin-top: .25rem; }
      .section-title {
          font-size: 1.05rem; font-weight: 700;
          color: #0F172A; margin: 1.2rem 0 .4rem 0;
          padding-bottom: .35rem; border-bottom: 2px solid #E2E8F0;
      }
      .stApp { background-color: #F8FAFC; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Load data
# ----------------------------------------------------------------------
try:
    df_all = load_data()
except FileNotFoundError as e:
    st.error(
        "❌ Dataset not found. Expected file:\n\n"
        "`data/nyse-Dashboard listed.csv`\n\n"
        "Do NOT rename the dataset file."
    )
    st.stop()

# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.title("📈 NYSE Listed Companies — EDA Dashboard")
st.markdown(
    "Exploratory analysis of every security currently listed on the New York "
    "Stock Exchange. The raw file contains only **ticker** and **company name**, "
    "so derived features (security type, share class, coupon rate, symbol "
    "length, etc.) are engineered to power a full 10-chart EDA."
)

# ----------------------------------------------------------------------
# Filters & filtered data
# ----------------------------------------------------------------------
filters = sidebar_filters(df_all)
df      = apply_filters(df_all, filters)

# ----------------------------------------------------------------------
# KPI summary cards
# ----------------------------------------------------------------------
total      = len(df)
n_common   = int(df["Is Common"].sum())
n_pref     = int(df["Is Preferred"].sum())
avg_namelen= df["Name Length"].mean() if total else 0
avg_symlen = df["Symbol Length"].mean() if total else 0

c1, c2, c3, c4, c5 = st.columns(5)
def kpi(col, label, value):
    col.markdown(
        f"<div class='kpi-card'>"
        f"<div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value'>{value}</div></div>",
        unsafe_allow_html=True,
    )
kpi(c1, "Total Listings",     f"{total:,}")
kpi(c2, "Common Stocks",      f"{n_common:,}")
kpi(c3, "Preferred Stocks",   f"{n_pref:,}")
kpi(c4, "Avg Name Length",    f"{avg_namelen:.1f}")
kpi(c5, "Avg Symbol Length",  f"{avg_symlen:.2f}")

if total == 0:
    st.warning("No rows match the current filters. Adjust them in the sidebar.")
    st.stop()

# ----------------------------------------------------------------------
# Charts — laid out in logical sections
# ----------------------------------------------------------------------
st.markdown("<div class='section-title'>📊 Composition</div>", unsafe_allow_html=True)
a, b, c = st.columns(3)
with a: st.pyplot(pie_security_type(df),       use_container_width=True)
with b: st.pyplot(count_share_class(df),       use_container_width=True)
with c: st.pyplot(bar_top_letters(df),         use_container_width=True)

st.markdown("<div class='section-title'>📈 Trends Over Time</div>", unsafe_allow_html=True)
a, b = st.columns(2)
with a: st.pyplot(line_listings_per_year(df),  use_container_width=True)
with b: st.pyplot(area_cumulative_listings(df),use_container_width=True)

st.markdown("<div class='section-title'>🔬 Distributions & Relationships</div>", unsafe_allow_html=True)
a, b = st.columns(2)
with a: st.pyplot(histogram_name_length(df),   use_container_width=True)
with b: st.pyplot(scatter_symlen_vs_namelen(df), use_container_width=True)

a, b = st.columns(2)
with a: st.pyplot(box_namelen_by_security(df), use_container_width=True)
with b: st.pyplot(violin_symlen_by_security(df), use_container_width=True)

st.markdown("<div class='section-title'>🧠 Correlation & Density</div>", unsafe_allow_html=True)
a, b = st.columns([1, 1.4])
with a: st.pyplot(heatmap_correlation(df),     use_container_width=True)
with b: st.pyplot(bubble_letter_security(df),  use_container_width=True)

# ----------------------------------------------------------------------
# Data table + download
# ----------------------------------------------------------------------
st.markdown("<div class='section-title'>📄 Filtered Data</div>", unsafe_allow_html=True)
st.dataframe(
    df[["Symbol", "Name", "Security Type", "Share Class",
        "Coupon Rate", "Symbol Length", "Name Length",
        "Word Count", "Listing Year"]],
    use_container_width=True, height=360,
)

st.download_button(
    "⬇️  Download filtered data (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="nyse_filtered.csv",
    mime="text/csv",
)

st.caption(
    "Built with Python · Pandas · Matplotlib · Seaborn · Streamlit  ·  "
    "EDA project for Exploratory Data Analysis course."
)
