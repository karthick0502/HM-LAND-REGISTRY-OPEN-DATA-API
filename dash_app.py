import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from logger import logger

# Initialize Logger
logger = logger()

# Load data
try:
    # Load average price and transaction data
    df_avg_price = pd.read_csv("./output/average_price_by_property_type.csv")
    df_transactions = pd.read_csv("./output/transactions_above_1_million.csv")
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise FileNotFoundError(f"Required file not found: {e}")
except pd.errors.ParserError as e:
    logger.error(f"Error parsing CSV file: {e}")
    raise ValueError(f"CSV parsing error: {e}")
except Exception as e:
    logger.error(f"Unexpected error loading CSV files: {e}")
    raise RuntimeError(f"Unexpected error: {e}")

# Preprocess data to ensure JSON serialization compatibility
try:
    if 'date_of_transfer' in df_transactions.columns:
        df_transactions['date_of_transfer'] = pd.to_datetime(
            df_transactions['date_of_transfer'], errors='coerce'
        )
        if df_transactions['date_of_transfer'].isnull().any():
            logger.warning("Some 'date_of_transfer' values could not be parsed and were set to NaT.")
    
    # Group data for the second tab and handle any errors
    df_grouped = (
        df_transactions.groupby(
            df_transactions['date_of_transfer'].dt.to_period('M') if 'date_of_transfer' in df_transactions.columns else []
        )['price']
        .mean()
        .reset_index()
        .rename(columns={'price': 'average_price'})
    )
    df_grouped['date_of_transfer'] = df_grouped['date_of_transfer'].astype(str)  # Ensure JSON compatibility
except Exception as e:
    logger.error(f"Error preprocessing data: {e}")
    raise RuntimeError(f"Error during data preprocessing: {e}")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Property Dashboard"

# Layout
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Average Price by Property Type and County", children=[
            html.H1("Average Price and Transaction Count by Property Type and County", style={'text-align': 'center'}),
            dcc.Graph(
                id='bar-chart',
                figure=px.bar(
                    df_avg_price,
                    x='county',  # Group bars by county
                    y='avg_price',  # Height of bars represents average price
                    color='property_type',  # Different colors for each property type
                    text='transaction_count',  # Display transaction count as text on the bars
                    title='Average Price and Transaction Count by Property Type and County',
                    labels={
                        'county': 'County',
                        'transaction_count': 'Transaction Count',
                        'property_type': 'Property Type',
                        'avg_price': 'Average Price (£)'
                    },
                    category_orders={'county': df_avg_price['county'].unique().tolist()},
                    barmode='stack'  # Display bars stacked for each county
                ).update_traces(
                    texttemplate='%{text}',  # Display transaction count as plain text
                    textposition='outside'  # Position text outside the bars
                ).update_layout(
                    xaxis_tickangle=-45,  # Rotate county names for better readability
                    yaxis_title="Average Price (£)",  # Explicit Y-axis label for average price
                    legend_title="Property Type",  # Legend title for property types
                    transition_duration=500,
                    uniformtext_minsize=8,  # Minimum text size
                    uniformtext_mode='hide',  # Hide text if it doesn’t fit
                    template="plotly_white"  # Use a clean theme
                )
            )
        ]),
        dcc.Tab(label="High-Value Transactions", children=[
            html.H1("Property Price Trends (Above 1 Million)", style={'text-align': 'center'}),
            dcc.Graph(
                id='line-chart',
                figure=px.line(
                    df_grouped,
                    x='date_of_transfer',
                    y='average_price',
                    title='Property Price Trends (Above 1 Million)',
                    labels={'date_of_transfer': 'Date', 'average_price': 'Average Price (£)'}
                ).update_layout(
                    yaxis_title="Average Price (£)",  # Explicit Y-axis label for price
                    transition_duration=500
                )
            )
        ]),
    ])
])

# Function to run the dashboard
def run_dashboard():
    logger.info("Starting dashboard...")
    app.run_server(debug=False, host="0.0.0.0", port=8050)

# Run the app
if __name__ == "__main__":
    try:
        app.run_server(debug=False, host="0.0.0.0", port=8050)
    except Exception as e:
        logger.error(f"Error running Dash app: {e}")
        raise RuntimeError(f"Server run error: {e}")
