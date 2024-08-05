import streamlit as st
import pandas as pd
import plotly.express as px

# Load the EV sales dataset
@st.cache_data
def load_data():
    data = pd.read_csv('IEA Global EV Data 2024.csv')
    return data

# Load the data
data = load_data()

# Dashboard title
st.title('Global EV Value Dashboard (2010 - 2024)')

# Display total value
total_value = data['value'].sum()
st.metric(label="Total EV Value", value=int(total_value))

# Filter by year
years = data['year'].unique()
selected_year = st.selectbox('Select Year:', sorted(years))

# Filter data for the selected year
year_data = data[data['year'] == selected_year]

# Value by Region (or Category, or Unit, depending on your interest)
value_by_region = year_data.groupby('region')['value'].sum().reset_index()

# Bar chart for value by region
fig_country = px.bar(value_by_region, x='region', y='value', title=f'EV Value by Region in {selected_year}')
st.plotly_chart(fig_country)

# Value trends over the years
value_trend = data.groupby('year')['value'].sum().reset_index()

# Line chart for value trends
fig_trend = px.line(value_trend, x='year', y='value', title='EV Value Trends Over Years')
st.plotly_chart(fig_trend)

# Additional metrics
st.subheader('Additional Insights')
st.write(f"Total value in {selected_year}: {year_data['value'].sum()}")
top_region = value_by_region.loc[value_by_region['value'].idxmax(), 'region']
st.write(f"Top-selling region: {top_region}")

# Show the data table
if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(data)

# Run the app with `streamlit run your_script_name.py`
