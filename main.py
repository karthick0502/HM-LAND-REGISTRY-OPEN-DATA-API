import os
from logger import logger
from API import download_file, process_file
# from etl import etl_process
from etl import etl_process
from reports import generate_reports

# Setting DB Insertion process during ETL
DB_INSERTION = True

# Constants
API_DATA = 'pp-monthly-update'  # You can change the file name if needed
DATA_URL = f'http://prod2.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/{API_DATA}.txt'
OUTPUT_CSV_FILE = f'property_transactions_{API_DATA}.csv'
TEMP_FILE = f'{API_DATA}.txt'
BATCH_SIZE = 50000  # Number of rows to process per batch
CHUNK_SIZE = 8192  # Size of chunks to read when downloading

#setup logger
logger = logger()

def main():
    try:
        # Step 1: Download and process the raw data file and save it as CSV
        download_file(DATA_URL, TEMP_FILE, CHUNK_SIZE)
        process_file(TEMP_FILE, OUTPUT_CSV_FILE, BATCH_SIZE)
        logger.info(f"Data processing completed. CSV saved as {OUTPUT_CSV_FILE}")
 
        # Step 2: Perform ETL process on the generated pre processed (cleaned) CSV file
        etl_process(file_name = OUTPUT_CSV_FILE, db_insertion=DB_INSERTION)

        # Step 3: Generate report as csv file to output folder
        generate_reports()
        
        # Step 4: Run the dashboard
        from dash_app import run_dashboard
        logger.info("Launching the dashboard...")
        run_dashboard()

    except Exception as e:
        logger.critical(f"Critical error in the main function: {e}")
        print("An error occurred. Check the logs for details.")

if __name__ == "__main__":
    main()
