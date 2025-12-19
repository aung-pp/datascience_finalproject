import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")
st.title("🛒 Supermarket Sales Interactive Dashboard")

# ------------------------
# Load Data
# ------------------------
df = pd.read_csv("../supermarket_sales.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month_name()
df['Month_Num'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
df['Hour'] = pd.to_datetime(df['Time']).dt.hour
df['Day'] = df['Date'].dt.day_name()

# ------------------------
# Sidebar Filters
# ------------------------
st.sidebar.header("Filter Options")

months = ["All"] + sorted(df['Month'].unique(), key=lambda x: pd.to_datetime(x, format='%B').month)
selected_month = st.sidebar.selectbox("Select Month", months, index=0)

years = ["All"] + sorted(df['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=0)

product_lines = ["All"] + df['Product line'].unique().tolist()
selected_product = st.sidebar.selectbox("Select Product Line", product_lines, index=0)

cities = ["All"] + df['City'].unique().tolist()
selected_city = st.sidebar.selectbox("Select City", cities, index=0)

payments = ["All"] + df['Payment'].unique().tolist()
selected_payment = st.sidebar.selectbox("Select Payment Type", payments, index=0)

# ------------------------
# Apply Filters
# ------------------------
filtered_df = df.copy()

if selected_month != "All":
    filtered_df = filtered_df[filtered_df['Month'] == selected_month]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]
if selected_product != "All":
    filtered_df = filtered_df[filtered_df['Product line'] == selected_product]
if selected_city != "All":
    filtered_df = filtered_df[filtered_df['City'] == selected_city]
if selected_payment != "All":
    filtered_df = filtered_df[filtered_df['Payment'] == selected_payment]

# ------------------------
# KPI Metrics
# ------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Sales", f"${filtered_df['Total'].sum():,.2f}")
col2.metric("Gross Margin %", f"{filtered_df['gross margin percentage'].mean():.2f}%")
col3.metric("Gross Income", f"${filtered_df['gross income'].sum():,.2f}")
col4.metric("Average Rating", f"{filtered_df['Rating'].mean():.2f}")
col5.metric("Average Unit Price", f"${filtered_df['Unit price'].mean():.2f}")

st.markdown("---")

# ------------------------
# Descriptive Analysis
# ------------------------
st.subheader("📊 Descriptive Statistics")
st.dataframe(filtered_df[['Total','gross margin percentage','gross income','Rating','Unit price']].describe().T)

# ------------------------
# Correlation Heatmap
# ------------------------

col1, col2 = st.columns(2)
with col1:
    st.subheader("📈 Correlation Heatmap")
    corr = filtered_df[['Total','gross margin percentage','gross income','Rating','Unit price']].corr()
    fig_heat = px.imshow(corr, text_auto=True, color_continuous_scale='Blues', title="Correlation Heatmap")
    st.plotly_chart(fig_heat)
with col2:
    # ------------------------
    # Heatmap: Day vs Hour Sales
    # ------------------------
    st.subheader("Sales Heatmap: Day vs Hour")
    heatmap_data = filtered_df.groupby(['Day','Hour'])['Total'].sum().reset_index()
    days_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    heatmap_data['Day'] = pd.Categorical(heatmap_data['Day'], categories=days_order, ordered=True)
    heatmap_data = heatmap_data.sort_values(['Day','Hour'])
    heatmap_pivot = heatmap_data.pivot(index='Day', columns='Hour', values='Total')
    fig_heatmap = px.imshow(heatmap_pivot, color_continuous_scale='Blues', text_auto=True, labels=dict(x="Hour", y="Day", color="Total Sales"), aspect="auto")
    st.plotly_chart(fig_heatmap)

# ------------------------
# Monthly Sales Line Chart
# ------------------------
st.subheader("Monthly Sales by Product Line")
monthly_sales = filtered_df.groupby(['Month_Num','Month','Product line'])['Total'].sum().reset_index()
line_data = monthly_sales.pivot(index='Month', columns='Product line', values='Total').fillna(0)
fig_line = px.line(monthly_sales, x='Month', y='Total', color='Product line', markers=True, title="Monthly Sales Trend by Product Line")
fig_line.update_layout(xaxis=dict(categoryorder='array', categoryarray=monthly_sales['Month'].unique()))
st.plotly_chart(fig_line)

# ------------------------
# Total Sales Bar Chart by Product Line
# ------------------------
st.subheader("Total Sales by Product Line")
sales_product = filtered_df.groupby("Product line")["Total"].sum().reset_index()
fig_bar = px.bar(sales_product, x="Product line", y="Total", color="Product line", text="Total", title="Total Sales by Product Line")
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar)

# ------------------------
# Pie Chart for Average Rating by Product Line
# ------------------------
st.subheader("Average Rating by Product Line")
rating_avg = filtered_df.groupby("Product line")["Rating"].mean().reset_index().sort_values("Rating", ascending=False)
# Gradient colors: dark to light
colors = px.colors.sequential.Blues[:len(rating_avg)]
fig_pie = px.pie(rating_avg, names="Product line", values="Rating", color="Product line", color_discrete_sequence=colors, title="Average Rating by Product Line", hover_data=["Rating"])
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_pie)

# ------------------------
# Additional Scatter: Unit Price vs Rating
# ------------------------
st.subheader("Unit Price vs Rating by Product Line")
fig_scatter = px.scatter(filtered_df, x='Unit price', y='Rating', color='Product line', size='Quantity', hover_data=['Total'], title="Unit Price vs Rating")
st.plotly_chart(fig_scatter)

# ------------------------
# Monthly Sales by City
# ------------------------
st.subheader("Monthly Trends by Product Line")
monthly_sales = df.groupby(['Month_Num','Month','Product line'])['Total'].sum().reset_index()

col1, col2 = st.columns(2)

with col1:
    fig_line2 = px.line(
        df.groupby(['Month','Product line'])['Rating'].mean().reset_index(),
        x='Month', y='Rating', color='Product line', markers=True, title="Average Rating Trend"
    )
    st.plotly_chart(fig_line2)

with col2:
    fig_line3 = px.line(
        df.groupby(['Month','Product line'])['Unit price'].mean().reset_index(),
        x='Month', y='Unit price', color='Product line', markers=True, title="Average Unit Price Trend"
    )
    st.plotly_chart(fig_line3)

# ------------------------
# Show Filtered Data
# ------------------------
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df)
