import subprocess
import sys
import os
import streamlit as st
import pandas as pd
from logger import logger
import plotly.express as px

logger = logger()

# Define file paths
df_1_path = "./output/average_price_by_property_type.csv"
df_2_path = "./output/transactions_above_1_million.csv"

# Function to safely load CSV files
def load_csv_file(file_path):
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            st.error(f"File not found: {file_path}")
            return None
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {str(e)}")
        st.error(f"An error occurred while loading the file: {file_path}. Please check the logs for more details.")
        return None

# Load the CSV files
df_1 = load_csv_file(df_1_path)
df_2 = load_csv_file(df_2_path)

# Show a selection menu for navigation between graphs
page = st.radio("Select Graph", options=["Average Price by Property Type", "Property Price Trends (Above 1 Million)"])

# Bar Chart for Average Price by Property Type
if page == "Average Price by Property Type" and df_1 is not None:
    try:
        # Bar Chart for Average Price by Property Type
        fig_1 = px.bar(df_1, x='county', y='avg_price', color='property_type',
                       title='Average Property Prices by City',
                       labels={'city': 'City', 'average_price': 'Average Price'},
                       width=1000, height=800)  # Adjust size for better visibility
        st.plotly_chart(fig_1, use_container_width=True)
    except Exception as e:
        logger.error(f"Error processing data for Average Price by Property Type: {str(e)}")
        st.error("An error occurred while processing the data for Average Price by Property Type. Please check the logs.")
else:
    logger.warning(f"Skipping plotting for {df_1_path} due to loading failure.")

# Property Price Trends (Above 1 Million)
if page == "Property Price Trends (Above 1 Million)" and df_2 is not None:
    try:
        # Convert 'date_of_transfer' to datetime format
        df_2['date_of_transfer'] = pd.to_datetime(df_2['date_of_transfer'])

        # Group by month, convert the Period object to a string for JSON serialization
        df_2['month'] = df_2['date_of_transfer'].dt.to_period('M').astype(str)

        # Group by the newly created 'month' column
        df_2_grouped = df_2.groupby('month')['price'].mean().reset_index()

        # Line Chart for Property Price Trends (Above 1 Million)
        fig_2 = px.line(df_2_grouped, x='month', y='price',
                        title='Property Price Trends (Above 1 Million)',
                        labels={'month': 'Date', 'price': 'Average Price'},
                        width=1000, height=800)  # Adjust size for better visibility
        st.plotly_chart(fig_2, use_container_width=True)
    except Exception as e:
        logger.error(f"Error processing data for Property Price Trends: {str(e)}")
        st.error("An error occurred while processing the data for Property Price Trends. Please check the logs.")
else:
    logger.warning(f"Skipping plotting for {df_2_path} due to loading failure.")

