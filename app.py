import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Data generation ──────────────────────────────────────────────────────────

@st.cache_data
def load_data() -> pd.DataFrame:
    np.random.seed(42)
    n = 1000

    start = date(2023, 1, 1)
    dates = [start + timedelta(days=int(d)) for d in np.random.randint(0, 730, n)]

    categories = ["Electronics", "Clothing", "Food & Beverage", "Home & Garden", "Sports"]
    regions = ["North", "South", "East", "West"]

    base_revenue = {
        "Electronics": 450,
        "Clothing": 120,
        "Food & Beverage": 60,
        "Home & Garden": 200,
        "Sports": 180,
    }

    cat_col = np.random.choice(categories, n)
    revenue = np.array([
        base_revenue[c] * (1 + 0.4 * np.random.randn()) for c in cat_col
    ]).clip(5)

    df = pd.DataFrame({
        "date": pd.to_datetime(dates),
        "category": cat_col,
        "region": np.random.choice(regions, n),
        "revenue": revenue.round(2),
        "units": np.random.randint(1, 50, n),
    })
    df = df.sort_values("date").reset_index(drop=True)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["year"] = df["date"].dt.year
    return df


df_full = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Filters")

    min_date = df_full["date"].min().date()
    max_date = df_full["date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    all_categories = sorted(df_full["category"].unique())
    selected_categories = st.multiselect(
        "Category",
        options=all_categories,
        default=all_categories,
    )

    all_regions = sorted(df_full["region"].unique())
    selected_regions = st.multiselect(
        "Region",
        options=all_regions,
        default=all_regions,
    )

    st.markdown("---")
    st.caption("Data: Synthetic sales dataset (2023-2024)")

# ── Filter data ───────────────────────────────────────────────────────────────

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_d, end_d = date_range
else:
    start_d, end_d = min_date, max_date

df = df_full[
    (df_full["date"].dt.date >= start_d)
    & (df_full["date"].dt.date <= end_d)
    & (df_full["category"].isin(selected_categories if selected_categories else all_categories))
    & (df_full["region"].isin(selected_regions if selected_regions else all_regions))
].copy()

# ── KPI calculations ──────────────────────────────────────────────────────────

total_revenue = df["revenue"].sum()
total_units = df["units"].sum()
avg_order = df["revenue"].mean() if len(df) else 0

# Growth rate: compare first half vs second half of the filtered window
mid = start_d + (end_d - start_d) / 2
rev_first = df[df["date"].dt.date <= mid]["revenue"].sum()
rev_second = df[df["date"].dt.date > mid]["revenue"].sum()
growth = ((rev_second - rev_first) / rev_first * 100) if rev_first > 0 else 0.0

# ── Header ────────────────────────────────────────────────────────────────────

st.title("Sales Performance Dashboard")
st.caption(f"Showing {len(df):,} transactions · {start_d} → {end_d}")

# ── KPI row ───────────────────────────────────────────────────────────────────

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    label="Total Revenue",
    value=f"${total_revenue:,.0f}",
    delta=f"{growth:+.1f}% vs prior period",
)
k2.metric(
    label="Total Units Sold",
    value=f"{total_units:,}",
)
k3.metric(
    label="Avg. Order Value",
    value=f"${avg_order:,.2f}",
)
k4.metric(
    label="Period Growth Rate",
    value=f"{growth:+.1f}%",
    delta="vs first half of period",
)

st.markdown("---")

# ── Charts row 1: Trend + Distribution ───────────────────────────────────────

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Revenue Trend Over Time")
    if df.empty:
        st.info("No data for the selected filters.")
    else:
        trend = (
            df.groupby(["month", "category"])["revenue"]
            .sum()
            .reset_index()
            .sort_values("month")
        )
        fig_line = px.line(
            trend,
            x="month",
            y="revenue",
            color="category",
            markers=True,
            labels={"revenue": "Revenue ($)", "month": "Month", "category": "Category"},
        )
        fig_line.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=40, b=0),
            hovermode="x unified",
        )
        fig_line.update_traces(line=dict(width=2))
        st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    st.subheader("Revenue by Category")
    if df.empty:
        st.info("No data for the selected filters.")
    else:
        pie_data = df.groupby("category")["revenue"].sum().reset_index()
        fig_pie = px.pie(
            pie_data,
            names="category",
            values="revenue",
            hole=0.45,
        )
        fig_pie.update_traces(textposition="outside", textinfo="percent+label")
        fig_pie.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ── Charts row 2: Bar comparison ─────────────────────────────────────────────

st.subheader("Category × Region Revenue Breakdown")

if df.empty:
    st.info("No data for the selected filters.")
else:
    bar_data = (
        df.groupby(["category", "region"])["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    fig_bar = px.bar(
        bar_data,
        x="category",
        y="revenue",
        color="region",
        barmode="group",
        labels={"revenue": "Revenue ($)", "category": "Category", "region": "Region"},
        text_auto=".2s",
    )
    fig_bar.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis_tickangle=0,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Monthly summary table ─────────────────────────────────────────────────────

st.subheader("Monthly Summary")

if df.empty:
    st.info("No data for the selected filters.")
else:
    summary = (
        df.groupby("month")
        .agg(
            Revenue=("revenue", "sum"),
            Orders=("revenue", "count"),
            Units=("units", "sum"),
            Avg_Order=("revenue", "mean"),
        )
        .reset_index()
        .rename(columns={"month": "Month", "Avg_Order": "Avg Order ($)"})
        .sort_values("Month", ascending=False)
    )
    summary["Revenue"] = summary["Revenue"].map("${:,.0f}".format)
    summary["Avg Order ($)"] = summary["Avg Order ($)"].map("${:,.2f}".format)
    st.dataframe(summary, use_container_width=True, hide_index=True)
