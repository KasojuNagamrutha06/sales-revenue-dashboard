import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="chocolate Sales Dashboard", layout="wide")

st.title("🍫 Sales & Revenue Dashboard")

# Load data
df = pd.read_csv("Chocolate Sales.csv")

# Data cleaning
df["Amount"] = df["Amount"].replace('[\$,]', '', regex=True).astype(float)
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# Create Month-Year column
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# Sidebar filters
st.sidebar.header("🔍 Filters")

country = st.sidebar.multiselect(
    "Country", df["Country"].unique(), default=df["Country"].unique()
)

product = st.sidebar.multiselect(
    "Product", df["Product"].unique(), default=df["Product"].unique()
)

filtered_df = df[(df["Country"].isin(country)) & (df["Product"].isin(product))]

# KPIs
total_revenue = filtered_df["Amount"].sum()
total_sales = filtered_df["Boxes Shipped"].sum()

# Monthly aggregation
monthly = filtered_df.groupby("Month").agg({
    "Amount": "sum",
    "Boxes Shipped": "sum"
}).reset_index()

monthly = monthly.sort_values("Month")

# Growth calculations
monthly["Revenue Growth %"] = monthly["Amount"].pct_change() * 100
monthly["Sales Growth %"] = monthly["Boxes Shipped"].pct_change() * 100

# Latest growth
rev_growth = monthly["Revenue Growth %"].iloc[-1] if len(monthly) > 1 else 0
sales_growth = monthly["Sales Growth %"].iloc[-1] if len(monthly) > 1 else 0

# Best month
best_month = monthly.loc[monthly["Amount"].idxmax(), "Month"]

# KPI Display
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Total Sales", int(total_sales))
col3.metric("📈 Revenue Growth", f"{rev_growth:.2f}%")
col4.metric("📊 Sales Growth", f"{sales_growth:.2f}%")

st.info(f"🏆 Best Revenue Month: {best_month}")

# Charts

# Revenue Trend
fig1 = px.line(monthly, x="Month", y="Amount", title="📈 Monthly Revenue Trend", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Sales Trend
fig2 = px.line(monthly, x="Month", y="Boxes Shipped", title="📦 Monthly Sales Trend", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# Growth Trend
fig3 = px.line(monthly, x="Month", y="Revenue Growth %",
               title="📊 Revenue Growth % Trend", markers=True)
st.plotly_chart(fig3, use_container_width=True)

# Product Performance
fig4 = px.bar(filtered_df, x="Product", y="Amount",
              color="Product", title="🍫 Product Revenue")
st.plotly_chart(fig4, use_container_width=True)

# Country Performance
fig5 = px.pie(filtered_df, names="Country", values="Amount",
              title="🌍 Revenue by Country")
st.plotly_chart(fig5, use_container_width=True)

# Top 5 products
top_products = filtered_df.groupby("Product")["Amount"].sum().sort_values(ascending=False).head(5)
st.subheader("🏆 Top 5 Products")
st.bar_chart(top_products)

# Table
st.subheader("📋 Data")
st.dataframe(filtered_df)