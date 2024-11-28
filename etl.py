import pandas as pd
import psycopg2
from logger import logger

# Setup logger
logger = logger()

def load_to_db():
    """
    Establish connection to the PostgreSQL database.
    Returns:
        conn: A psycopg2 connection object
    """
    try:
        conn = psycopg2.connect(
            dbname="price_paid_data",
            user="hm_land",
            password="12345",
            host="localhost",
            port="5432"
        )
        logger.info("Connected to PostgreSQL database successfully.")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL database: {e}")
        raise

def insert_into_property_transactions(cleaned_df):
    """
    Insert data from the cleaned DataFrame into the property_transactions table
    in the PostgreSQL database with foreign key references and address.
    :param cleaned_df: Transformed DataFrame containing the data to be inserted.
    """
    try:
        print('These are the columns are going to be add to main (property_transaction table)')
        logger.info(cleaned_df.columns)
        # Establish the database connection
        conn = load_to_db()
        cursor = conn.cursor()

        # Log the start of the insert operation
        logger.info("Starting data insertion into the database.")
        logger.info("Data inserting...")

        # Loop through the DataFrame and insert each row
        for _, row in cleaned_df.iterrows():
            try:
                # Insert into property_transactions table with references to other tables
                cursor.execute("""
                INSERT INTO property_transactions (
                    transaction_unique_id, price, date_of_transfer, postcode, 
                    property_type_id, old_new, tenure_id, paon, saon, street, locality, 
                    town_city, district, county, ppd_category_id, record_status_id, 
                    avg_price_by_property_type, address
                )
                VALUES (%s, %s, %s, %s, 
                        (SELECT property_type_id FROM property_types WHERE property_type_code = %s), 
                        %s, 
                        (SELECT tenure_id FROM tenures WHERE tenure_code = %s), 
                        %s, %s, %s, %s, %s, %s, %s, 
                        (SELECT ppd_category_id FROM ppd_categories WHERE ppd_category_code = %s),
                        (SELECT record_status_id FROM record_statuses WHERE record_status_code = %s),
                        %s, 
                        %s)
                ON CONFLICT (transaction_unique_id)
                DO NOTHING
            """, (
                    row['Transaction ID'], row['Price'], row['Date of Transfer'], row['Postcode'],
                    row['Property Type'], row['Old/New'],
                    row['Duration'], row['PAON'], row['SAON'], row['Street'], 
                    row['Locality'], row['Town/City'], row['District'], row['County'],
                    row['PPD Category'], row['Record Status'],
                    row['Avg_Price_by_Property_Type'],
                    row['Address']
                ))

                # log how many rows are affected
                if cursor.rowcount > 0:
                    logger.info(f"Inserted or Updated record with Transaction ID: {row['Transaction ID']}")

            except Exception as e:
                # Rollback in case of error
                logger.error(f"Error inserting record {row['Transaction ID']}: {e}")
                conn.rollback()

        # Commit the transaction after all records have been processed
        conn.commit()

        # Log the successful completion
        logger.info(f"Data insertion into the database completed")

    except Exception as e:
        logger.error(f"Error during Database insertion: {e}")
    
    finally:
        # Close the cursor and connection after all processing is done
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def transform_data(file_name, save_csv):
    """
    Perform data transformation tasks such as cleaning, standardizing,
    and calculating fields.
    :param file_name: Path to the raw CSV file
    :return: Transformed DataFrame
    """
    try:
        logger.info("Starting ETL process.")

        # Load raw CSV into DataFrame
        df = pd.read_csv(file_name)
        logger.info(f"Data loaded from {file_name}. Initial rows: {len(df)}.")

        # Clean data: Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_count - len(df)} duplicate rows.")

        # Remove rows with null values
        rows_with_null = df.isnull().sum().sum()
        if rows_with_null > 0:
            logger.info(f"Found {rows_with_null} missing values. Removing rows with null values.")
            initial_count = len(df)
            df = df.dropna()
            logger.info(f"Removed {initial_count - len(df)} rows containing null values.")

        # 1. Calculate average price by property type
        if 'Property Type' in df.columns and 'Price' in df.columns:
            df['Avg_Price_by_Property_Type'] = df.groupby('Property Type')['Price'].transform('mean').round(2)
            logger.info("Average price by property type calculated.")
        else:
            logger.warning("Property Type or Price column not found. Skipping average price calculation.")

        # 2. Reformat Transaction ID (remove curly braces)
        if 'Transaction ID' in df.columns:
            df['Transaction ID'] = df['Transaction ID'].str.replace(r'[{}]', '', regex=True)
            logger.info("Transaction ID reformatted.")
        else:
            logger.warning("Transaction ID column not found.")

        # 3. Remove quotes from specific columns (Postcode to Record Status)
        if 'Postcode' in df.columns and 'Record Status' in df.columns:
            quote_columns = df.loc[:, 'Postcode':'Record Status'].columns
            for col in quote_columns:
                df[col] = df[col].str.replace(r'"', '', regex=True)
            logger.info(f"Quotes removed from columns: {', '.join(quote_columns)}")

        # 4. Consolidate fields into Address column
        logger.info('Address column formatting...')
        address_components = ['PAON', 'SAON', 'Street', 'Locality', 'Town/City', 'District', 'County', 'Postcode']
        if 'Address' in df.columns:
            df['Address'] = df['Address'].str.replace(r'"', '', regex=True)
        df['Address'] = df[address_components].apply(
            lambda row: ', '.join(row.dropna().astype(str)), axis=1
        )
        logger.info("Address column reformatted and consolidated.")

        # Log the transformation summary
        logger.info(f"Transformed data: {len(df)} rows and {df.shape[1]} columns after cleaning.")

        # Save cleaned DataFrame to CSV if specified
        if save_csv:
            df.to_csv(f'cleaned_{file_name}', index=False)
            logger.info(f"Cleaned DataFrame saved to cleaned_{file_name}.")

        return df

    except Exception as e:
        logger.error(f"Error during data transformation: {e}")
        raise

def etl_process(file_name, db_insertion):
    """
    Main ETL process: Extract -> Transform -> Load
    :param file_name: Path to the raw CSV file
    """
    try:
        # Step 1: Extract and Transform
        df = transform_data(file_name, save_csv=True)

        # Step 2: insert into database
        if db_insertion:
            insert_into_property_transactions(cleaned_df=df)
        else:
            logger.warning("DB insertion skipped...")   
        logger.info("ETL process completed successfully.")

    except Exception as e:
        logger.critical(f"Critical error in ETL process: {e}")
        raise


# Entry point for execution
if __name__ == "__main__":
    db_insertion = False
    raw_csv_file = "property_transactions_pp-2023.csv"  # Replace with your input file path
    etl_process(raw_csv_file, db_insertion)
