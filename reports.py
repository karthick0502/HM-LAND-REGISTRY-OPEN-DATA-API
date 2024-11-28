import psycopg2
import pandas as pd
from logger import logger
from etl import load_to_db
from psycopg2 import OperationalError, DatabaseError

# Setup logger
logger = logger()

def run_query(conn, query):
    """Run a query and return the result as a DataFrame."""
    try:
        df = pd.read_sql_query(query, conn)
        logger.info("Report SQL Query executed successfully.")
        return df
    except DatabaseError as e:
        logger.error(f"Error executing report query: {e}")
        raise

def save_to_csv(df, filename):
    """Save the DataFrame to a CSV file."""
    try:
        df.to_csv(filename, index=False)
        logger.info(f"Report Data saved to {filename}.")
    except Exception as e:
        logger.error(f"Error saving Report data to CSV: {e}")
        raise

def generate_reports():
    logger.info('Generate report starting...')
    try:
        # SQL Query 1: Average Price and Transaction Count by Property Type and County
        query_1 = """
            SELECT 
                pt.county AS county,
                ptp.property_type_code AS property_type,
                COUNT(pt.transaction_id) AS transaction_count,
                AVG(pt.price) AS avg_price
            FROM 
                property_transactions pt
            JOIN 
                property_types ptp 
            ON 
                pt.property_type_id = ptp.property_type_id
            GROUP BY 
                pt.county, ptp.property_type_code
            ORDER BY 
                transaction_count DESC;
        """
        
        # SQL Query 2: Transactions above 1 Million
        query_2 = """
        SELECT 
            transaction_unique_id,
            price,
            date_of_transfer,
            town_city,
            county,
            postcode
        FROM 
            property_transactions
        WHERE 
            price > 1000000
        ORDER BY 
            price DESC;
        """
        
        # Create a database connection
        conn = load_to_db()

        # Run Query 1 and save the results to CSV
        df_1 = run_query(conn, query_1)
        save_to_csv(df_1, "./output/average_price_by_property_type.csv")
        logger.info(f'Report csv Generated for Query 1: Average Price by Property Type')

        # Run Query 2 and save the results to CSV
        df_2 = run_query(conn, query_2)
        save_to_csv(df_2, "./output/transactions_above_1_million.csv")
        logger.info(f'Report csv Generated for Query 2: Transactions above 1 Million')

        # Close the database connection
        conn.close()

    except Exception as e:
        logger.error(f"Error in while generate report execution: {e}")
        raise

if __name__ == "__main__":
    generate_reports()
