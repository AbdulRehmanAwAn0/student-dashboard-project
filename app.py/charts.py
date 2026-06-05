"""
charts.py
---------
Matplotlib + Seaborn visualisation functions for the NYSE Listed
Companies EDA dashboard. Every function returns a `matplotlib.figure.Figure`
so the Streamlit app can render it with `st.pyplot(fig)`.

A consistent professional color palette and font sizing is applied
through `apply_theme()`.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

PALETTE = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B",
           "#6A994E", "#BC4749", "#386641", "#8338EC", "#FB5607"]


def apply_theme() -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update({
        "figure.facecolor":  "white",
        "axes.facecolor":    "white",
        "axes.edgecolor":    "#CBD5E1",
        "axes.titleweight":  "bold",
        "axes.titlesize":    13,
        "axes.labelsize":    11,
        "xtick.labelsize":   10,
        "ytick.labelsize":   10,
        "legend.fontsize":   10,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.grid":         True,
        "grid.alpha":        0.25,
        "font.family":       "DejaVu Sans",
    })


def _empty(title: str):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.text(0.5, 0.5, "No data for current filters",
            ha="center", va="center", color="#94A3B8", fontsize=12)
    ax.set_title(title)
    ax.axis("off")
    return fig


# ---------------------------------------------------------------- 1. Pie
def pie_security_type(df: pd.DataFrame):
    if df.empty:
        return _empty("Security-Type Distribution")
    counts = df["Security Type"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, _, autotxt = ax.pie(
        counts.values, labels=counts.index, autopct="%1.1f%%",
        colors=PALETTE[: len(counts)], startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=2),
        textprops=dict(fontsize=10),
    )
    for t in autotxt:
        t.set_color("white"); t.set_fontweight("bold")
    ax.set_title("Security-Type Distribution")
    return fig


# ---------------------------------------------------------------- 2. Histogram
def histogram_name_length(df: pd.DataFrame):
    if df.empty:
        return _empty("Company-Name Length Distribution")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(df["Name Length"], bins=30, kde=True,
                 color=PALETTE[0], ax=ax)
    ax.set_title("Company-Name Length Distribution")
    ax.set_xlabel("Characters in Company Name")
    ax.set_ylabel("Number of Listings")
    return fig


# ---------------------------------------------------------------- 3. Line
def line_listings_per_year(df: pd.DataFrame):
    if df.empty:
        return _empty("Listings per Year")
    series = df.groupby("Listing Year").size()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(series.index, series.values,
            marker="o", color=PALETTE[1], linewidth=2)
    ax.fill_between(series.index, series.values,
                    color=PALETTE[1], alpha=0.12)
    ax.set_title("Listings per Year (derived)")
    ax.set_xlabel("Year"); ax.set_ylabel("Number of Listings")
    return fig


# ---------------------------------------------------------------- 4. Bar
def bar_top_letters(df: pd.DataFrame, n: int = 15):
    if df.empty:
        return _empty("Top Starting Letters")
    counts = df["First Letter"].value_counts().head(n)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=counts.index, y=counts.values,
                hue=counts.index, palette="viridis",
                ax=ax, legend=False)
    ax.set_title(f"Top {n} Starting Letters of Ticker Symbols")
    ax.set_xlabel("First Letter"); ax.set_ylabel("Count")
    for i, v in enumerate(counts.values):
        ax.text(i, v + max(counts.values) * 0.01, str(v),
                ha="center", fontsize=9)
    return fig


# ---------------------------------------------------------------- 5. Scatter
def scatter_symlen_vs_namelen(df: pd.DataFrame):
    if df.empty:
        return _empty("Symbol Length vs Name Length")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(
        data=df, x="Symbol Length", y="Name Length",
        hue="Security Type", palette=PALETTE,
        alpha=0.6, s=40, ax=ax,
    )
    ax.set_title("Symbol Length vs Company-Name Length")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    return fig


# ---------------------------------------------------------------- 6. Box
def box_namelen_by_security(df: pd.DataFrame):
    if df.empty:
        return _empty("Name Length by Security Type")
    order = df["Security Type"].value_counts().index
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(data=df, x="Security Type", y="Name Length",
                order=order, hue="Security Type", palette=PALETTE,
                ax=ax, legend=False)
    ax.set_title("Company-Name Length by Security Type")
    ax.set_xlabel(""); ax.set_ylabel("Name Length (chars)")
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    return fig


# ---------------------------------------------------------------- 7. Heatmap
def heatmap_correlation(df: pd.DataFrame):
    if df.empty:
        return _empty("Correlation Heatmap")
    num = df[["Symbol Length", "Name Length", "Word Count",
              "Coupon Rate", "Listing Year"]].copy()
    corr = num.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    sns.heatmap(corr, annot=True, fmt=".2f",
                cmap="coolwarm", center=0,
                square=True, linewidths=0.5,
                cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Correlation of Numeric Features")
    return fig


# ---------------------------------------------------------------- 8. Area
def area_cumulative_listings(df: pd.DataFrame):
    if df.empty:
        return _empty("Cumulative Listings Over Time")
    series = df.groupby("Listing Year").size().sort_index().cumsum()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.fill_between(series.index, series.values,
                    color=PALETTE[2], alpha=0.45)
    ax.plot(series.index, series.values,
            color=PALETTE[2], linewidth=2)
    ax.set_title("Cumulative Listings Over Time")
    ax.set_xlabel("Year"); ax.set_ylabel("Cumulative Count")
    return fig


# ---------------------------------------------------------------- 9. Count
def count_share_class(df: pd.DataFrame):
    if df.empty:
        return _empty("Share-Class Frequency")
    order = df["Share Class"].value_counts().index
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.countplot(data=df, x="Share Class", order=order,
                  hue="Share Class", palette="mako",
                  ax=ax, legend=False)
    ax.set_title("Share-Class Frequency")
    ax.set_xlabel("Share Class"); ax.set_ylabel("Count")
    return fig


# ---------------------------------------------------------------- 10. Violin
def violin_symlen_by_security(df: pd.DataFrame):
    if df.empty:
        return _empty("Symbol Length by Security Type")
    order = df["Security Type"].value_counts().index
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.violinplot(data=df, x="Security Type", y="Symbol Length",
                   order=order, hue="Security Type",
                   palette=PALETTE, inner="quartile",
                   ax=ax, legend=False)
    ax.set_title("Symbol-Length Density by Security Type")
    ax.set_xlabel(""); ax.set_ylabel("Symbol Length")
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    return fig


# ---------------------------------------------------------------- Bonus: bubble
def bubble_letter_security(df: pd.DataFrame):
    if df.empty:
        return _empty("Letter × Security Type Bubble")
    grp = (df.groupby(["First Letter", "Security Type"])
             .size().reset_index(name="Count"))
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(
        data=grp, x="First Letter", y="Security Type",
        size="Count", hue="Security Type", palette=PALETTE,
        sizes=(20, 600), alpha=0.7, ax=ax, legend=False,
    )
    ax.set_title("Listing Density: First Letter × Security Type")
    ax.set_xlabel("Starting Letter of Symbol"); ax.set_ylabel("")
    return fig
