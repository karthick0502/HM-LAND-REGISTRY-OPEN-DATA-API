import requests
import os
import pandas as pd
from logger import logger

#setup logger
logger = logger()



def download_file(url, file_name, chunk_size):
    """
    Download the file from the URL if not already downloaded.
    :param url: URL of the file
    :param file_name: Local file name to save
    """
    try:
        if os.path.exists(file_name):
            logger.info(f"{file_name} already exists. Skipping download.")
            return
        
        logger.info('Starting file download...')
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
        logger.info(f"File downloaded and saved as {file_name}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading file: {e}")
        raise

def process_file(file_name, output_csv, batch_size):
    """
    Process the downloaded file and save it in batches to a CSV file using Pandas.
    :param file_name: Input text file name
    :param output_csv: Output CSV file name
    :param batch_size: Number of lines to process per batch
    """
    try:
        logger.info("Starting file processing...")
        default_columns = ["Transaction ID", "Price", "Date of Transfer", "Postcode", "Property Type", 
                           "Old/New", "Duration", "PAON", "SAON", "Street", "Locality", "Town/City", 
                           "District", "County", "PPD Category", "Record Status"]
        
        if os.path.exists(output_csv):
            logger.info(f"{output_csv} already exists. Appending to it.")
        
        batch = []  # Initialize an empty batch
        skip_count = 0
        process_count = 0
        
        with open(file_name, 'r', encoding='utf-8') as file:
            for index, line in enumerate(file, start=1):
                fields = line.strip().split(',')
                
                # Check for column count mismatch
                if len(fields) != len(default_columns):
                    # print(f"Row {index}-{fields[0]} has column mismatch. Expected {len(default_columns)} columns, found {len(fields)} columns.")
                    skip_count += 1
                    continue  # Skip this row
                
                batch.append(fields)

                # When the batch size is reached, save it as a DataFrame and write to CSV
                if len(batch) == batch_size:                    
                    df = pd.DataFrame(batch, columns=default_columns)
                    write_to_csv(df, output_csv, header=not os.path.exists(output_csv))
                    process_count += len(df)
                    batch = []  # Reset the batch
                    logger.info(f"Processed {index} records...")

            # Process any remaining records
            if batch:
                df = pd.DataFrame(batch, columns=default_columns)
                write_to_csv(df, output_csv, header=not os.path.exists(output_csv))
                process_count += len(df)
                logger.info(f"Processed all records. Total: {index} records.")

        logger.warning(f"Overall skipped rows: {skip_count}")
        logger.warning(f"Total processed rows: {process_count}")

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise

def write_to_csv(dataframe, file_name, header=False):
    """
    Write a Pandas DataFrame to a CSV file.
    :param dataframe: Pandas DataFrame to write
    :param file_name: Output CSV file name
    :param header: Whether to write the header row
    """
    try:
        dataframe.to_csv(file_name, mode='a', index=False, header=header, encoding='utf-8')
        logger.info(f"Wrote {len(dataframe)} records to {file_name}")
    except Exception as e:
        logger.error(f"Error writing to CSV: {e}")
        raise