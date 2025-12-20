import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

st.set_page_config(page_title="World Happiness 2021", layout="wide")
st.title("😊 World Happiness 2021 Dashboard")

# ------------------------
# Load Data
# ------------------------
df = pd.read_csv("world-happiness-report-2021.csv")

# ------------------------
# Data Preprocessing
# ------------------------

df_new = df.copy()
df_new.rename(columns = {"Country name":"Country"}, inplace = True)
df_new.rename(columns = {"Regional indicator":"Region"}, inplace = True)

# ------------------------
# Sidebar Filters
# ------------------------
st.sidebar.header("Filter Options")

regions = ["All"] + sorted(df_new['Region'].unique())
selected_region = st.sidebar.selectbox("Select Region", regions, index = 0)

countries = ["All"] + sorted(df_new['Country'].unique())
selected_country = st.sidebar.selectbox("Select Country", countries, index=0)

# ------------------------
# Apply Filters
# ------------------------
filtered_df_new = df_new.copy()

if selected_region != "All":
    filtered_df_new = filtered_df_new[filtered_df_new['Region'] == selected_region]
if selected_country != "All":
    filtered_df_new = filtered_df_new[filtered_df_new['Country'] == selected_country]

# ------------------------
# KPI Metrics
# ------------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)
# average ladder socre
# col1.metric("Total Countires", f"${filtered_df_new["Country"].sum():,.2f}")
col1.metric("Total Countries", filtered_df_new["Country"].nunique())
col2.metric("Happiness score", f"{filtered_df_new["Ladder score"].mean():.2f}")
col3.metric("GDP", f"{filtered_df_new["Logged GDP per capita"].mean():.2f}")
col4.metric("Life Expectancy", f"{filtered_df_new["Healthy life expectancy"].mean():.2f}")
col5.metric("Freedom to Choose", f"{filtered_df_new["Freedom to make life choices"].mean():.2f}")
col6.metric("Corruption Perception", f"{filtered_df_new["Perceptions of corruption"].mean():.2f}")

st.markdown("---")

# ------------------------
# Descriptive Analysis
# ------------------------
st.subheader("📊 Descriptive Statistics")
st.dataframe(filtered_df_new[["Logged GDP per capita", "Social support", "Healthy life expectancy", 
                              "Freedom to make life choices", "Generosity", "Perceptions of corruption"]].describe().T)

# ------------------------
# Correlation Heatmap
# ------------------------

st.subheader("📈 Correlation Heatmap")
corr = filtered_df_new[["Logged GDP per capita", "Social support", "Healthy life expectancy", 
                              "Freedom to make life choices", "Generosity", "Perceptions of corruption"]].corr()
fig_heat = px.imshow(corr, text_auto = True, color_continuous_scale = "Blues", title = "Correlation Heatmap")
st.plotly_chart(fig_heat)

# ------------------------
# Top Countries
# ------------------------
st.subheader("Top Happiness Countries")
happiness_countires = filtered_df_new.groupby("Country")["Ladder score"].sum().reset_index()
fig_bar = px.bar(happiness_countires, x = "Country", y= "Ladder score", 
                 color = "Country", text = "Ladder score", 
                 title = "World Happiness Scores", labels = {"Ladder score": "Happiness Score"})
fig_bar.update_layout(showlegend = False)
st.plotly_chart(fig_bar)

# ------------------------
# Pie Chart for Region
# ------------------------
st.subheader("Happiness Happiness Scores by Regions")
score_avg = filtered_df_new.groupby("Region")["Ladder score"].mean().reset_index().sort_values("Ladder score", ascending=False)
# Gradient colors: dark to light
colors = px.colors.sequential.Blues[:len(score_avg)]
fig_pie = px.pie(score_avg, names="Region", values="Ladder score", color = "Ladder score", color_discrete_sequence = colors, title="Average Happiness Scores by Region", hover_data=["Ladder score"])
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_pie)

# ------------------------
# Scatter: Major Happiness Matrics Vs Happiness Scores
# ------------------------
st.subheader("Major Happiness Matrics vs Happiness Scores")

fig_scatter = px.scatter(filtered_df_new, x = 'Logged GDP per capita', y='Ladder score', 
                         color='Country', size='Ladder score', hover_data=['Ladder score'], 
                         title="GDP vs Happiness Scores")
st.plotly_chart(fig_scatter)

fig_line = px.line(filtered_df_new, x = 'Healthy life expectancy', y = 'Ladder score', 
                   color = 'Country', markers = True, 
                   title="Life Expectancy vs Happiness Scores")
st.plotly_chart(fig_line)

fig_scatter = px.scatter(filtered_df_new, x = 'Social support', y='Ladder score', 
                         color='Country', size='Ladder score', hover_data=['Ladder score'], 
                         title="Social Support vs Happiness Scores")
st.plotly_chart(fig_scatter)


