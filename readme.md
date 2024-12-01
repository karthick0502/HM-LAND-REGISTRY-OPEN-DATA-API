# Project Documentation

## 1. **Database Design**

The database design consists of several tables to store property transaction data, with relationships between them ensuring data integrity and supporting the required queries for analysis.

### Tables:
1. **property_types**:
   - **Columns**:
     - `property_type_id`: Unique identifier for property types (Primary Key).
     - `property_type_code`: A short code to identify property types (e.g., "D" for Detached).
     - `property_type_description`: A textual description of the property type (e.g., "Detached House").
   
2. **tenures**:
   - **Columns**:
     - `tenure_id`: Unique identifier for property tenure (Primary Key).
     - `tenure_code`: A short code for tenure type (e.g., "F" for Freehold).
     - `tenure_description`: A description of the tenure (e.g., "Freehold").
   
3. **ppd_categories**:
   - **Columns**:
     - `ppd_category_id`: Unique identifier for the PPD category (Primary Key).
     - `ppd_category_code`: A code representing the category (e.g., "A" for Sale).
     - `ppd_category_description`: Description of the PPD category (e.g., "Sale").
   
4. **record_statuses**:
   - **Columns**:
     - `record_status_id`: Unique identifier for the record status (Primary Key).
     - `record_status_code`: A code representing the status of the record (e.g., "N" for New).
     - `record_status_description`: Description of the record status (e.g., "New").
   
5. **property_transactions** (Main Table):
   - **Columns**:
     - `transaction_id`: Unique identifier for each transaction (Primary Key).
     - `transaction_unique_id`: A unique string identifier for each transaction.
     - `price`: The price of the property in the transaction.
     - `date_of_transfer`: The date when the property was transferred.
     - `postcode`: The postcode of the property.
     - `property_type_id`: Foreign key referencing the `property_types` table.
     - `old_new`: Indicates if the property is old or new (optional).
     - `tenure_id`: Foreign key referencing the `tenures` table.
     - `paon`, `saon`, `street`, `locality`, `town_city`, `district`, `county`: Address details of the property.
     - `ppd_category_id`: Foreign key referencing the `ppd_categories` table.
     - `record_status_id`: Foreign key referencing the `record_statuses` table.
     - `avg_price_by_property_type`: Average price by property type.
     - `address`: Full address of the property (optional).

### Relationships:
- The `property_transactions` table is the central table, which holds references to other tables via foreign keys.
- **`property_types`**: Defines the types of properties involved in transactions.
- **`tenures`**: Specifies the tenure type (e.g., freehold or leasehold).
- **`ppd_categories`**: Defines the type of property (e.g., sale, new build).
- **`record_statuses`**: Indicates the status of a transaction record (e.g., new, updated).


## 2. **Data Transformations**

Several data transformations were applied to the raw property transactions data:

- **Date Handling**:
  - The `date_of_transfer` column was converted to a `datetime` format to ensure compatibility with analysis tools and visualizations.
  - Transactions were grouped by month to calculate the average price for property types in a given county, allowing time-based insights.

- **Grouping**:
  - Data was grouped by `county` and `property_type` to calculate the total number of transactions and the average price for each combination. This aggregation was used to generate the first report and visualizations.

- **Filtering**:
  - High-value property transactions (those above £1 million) were filtered from the `property_transactions` table for the second report.


## 3. **Report and Visualization Generation**

### Reports:
1. **Average Price and Transaction Count by Property Type and County**:
   - A SQL query was written to join the `property_transactions` and `property_types` tables, grouping by `county` and `property_type_code`. 
   - The report calculates the total number of transactions (`COUNT`) and the average price (`AVG`) for each combination of county and property type.
   - The result is sorted by the transaction count in descending order, highlighting regions with the most activity.

2. **High-Value Transactions - Property Price Trends (Above 1 Million)**:
   - Another SQL query was used to filter property transactions with a price greater than £1 million. This query returns the transaction details, including the unique transaction ID, price, date of transfer, and address information.
   - These high-value transactions are sorted by price in descending order to identify the most expensive properties.

### Visualizations:
- **Bar Chart**: A stacked bar chart was created using Plotly's `px.bar` to visualize the average prices and transaction counts by property type and county. Each bar represents a county, with segments showing the distribution of transaction counts by property type.
- **Line Chart**: A line chart was created using `px.line` to visualize the price trends of properties over time (filtered for those above £1 million). The x-axis represents the time period, and the y-axis shows the average price.

Both visualizations were integrated into a Dash app, with interactive features to allow users to explore the data dynamically.


## 5. **Docker Setup for Database**

To facilitate the development and testing environment, Docker containers were used to run the PostgreSQL database and pgAdmin 4 for managing the database.

- **PostgreSQL Container**: A PostgreSQL container was used to host the database. The data was populated in the `property_transactions` database and related tables.
- **pgAdmin 4 Container**: pgAdmin 4 was used as the web interface to manage the PostgreSQL database, providing an easy way to monitor and query the database.

For detailed instructions on setting up the database containers and managing the environment, please refer to the `docker-db-setup.md` file in the project repository. This file provides step-by-step instructions on pulling the necessary Docker images and configuring the containers.



## **Project Overview**

This project involves building a comprehensive data pipeline, transforming raw property transaction data, and visualizing key insights. The workflow spans from data ingestion to data cleaning, transformation, storage, and finally, generating dynamic reports and visualizations. The project uses **PostgreSQL**, **Docker containers**, and **Dash** for interactive web-based visualizations. 

### **Data Workflow**

#### **Step 1: Data Download and Storage**
1. **Download the Raw Data**:  
   The raw property transaction data is first downloaded from a given source (e.g., a CSV file). This file is stored locally before any data processing begins.

2. **Data Cleaning and Transformation**:  
   After saving the raw data into a CSV file, we proceed with cleaning and transforming the dataset. The following operations are applied to ensure the data is accurate and consistent:
   
   - **Remove Duplicates**:  
     The dataset is checked for duplicates and cleaned to ensure that only unique records are retained. The number of duplicates removed is logged for transparency.
   - **Handle Missing Values**:  
     Rows with missing values are identified and removed to maintain dataset integrity. The number of rows containing null values is logged.
   - **Calculate Average Price by Property Type**:  
     The average price per property type is calculated and stored in a new column `Avg_Price_by_Property_Type`. 
   - **Reformat Transaction ID**:  
     The `Transaction ID` is reformatted by removing curly braces.
   - **Remove Quotes from Specific Columns**:  
     Quotes are removed from specific columns like `Postcode` and `Record Status` to ensure uniformity.  
   - **Consolidate Address Information**:  
     An `Address` column is created by consolidating multiple fields such as `PAON`, `SAON`, `Street`, `Locality`, etc. This is done to make the address more readable and to help with data integrity. 

3. **Save Cleaned Data**:  
   After the transformation steps are completed, the cleaned data is saved back into a new CSV file. This file is ready to be imported into the database.

#### **Step 2: Upserting Data into Database**
1. **Upsert Logic (Handling Duplicates and Updates)**:  
   One of the key features of this project is the **upsert mechanism**, which ensures that any existing records in the database are updated if needed or inserted if they do not exist. This is achieved through a process called **upserting**, which combines insert and update operations to maintain the integrity of the data while avoiding duplicates.  
   
   **Upsert Example**:  
   In the `property_transactions` table, if a transaction with the same `transaction_unique_id` already exists, the record is updated. Otherwise, a new record is inserted. This is done for every dataset imported into the database.

2. **Error Handling and Logging**:  
   Every operation in this project is accompanied by error handling and logging to ensure smooth operation and traceability. We use a logging mechanism to record the success, failure, or any other issues encountered during the data processing and insertion stages.

   - **Logging Levels**:
     - **INFO**: For successful operations (e.g., removal of duplicates, completion of transformations).
     - **WARNING**: For potential issues (e.g., missing columns).
     - **ERROR**: For critical failures (e.g., database connection errors, upsert failures).

#### **Step 3: Report Generation and Visualization**
1. **SQL Queries**:  
   The core reports are generated using SQL queries that aggregate and filter data from the database. The following queries are used:
   - **Average Price and Transaction Count by Property Type and County**:  
     This query calculates the total number of transactions and the average price per property type and county.
     
   - **High-Value Transactions (Above £1 Million)**:  
     This query identifies and lists transactions where the price exceeds £1 million.

2. **Data Fetching**:  
   The data from the database is fetched using Python and then passed into visualization libraries.

3. **Data Visualization**:
   - **Bar Chart**: A bar chart is generated to visualize transaction counts and average prices by property type for each county.
   - **Line Chart**: A line chart is used to show price trends for high-value transactions.

4. **Dash Application**:  
   The visualizations are integrated into a Dash application, which serves as an interactive dashboard. Users can filter data, view charts, and explore the underlying trends.


## **How to Run the Project**

### 1. **Set Up Docker**  
   - **Install Docker**: Make sure Docker is installed on your machine.
   - **Database Setup**: Use the `docker-db-setup.md` file to set up **PostgreSQL** and **pgAdmin4** Docker containers. This guide will walk you through pulling the necessary Docker images and running the containers for the database setup.
## **Important note: Create a folder called 'output' where your main.py file exists**
### 2. **Run `main.py` - Complete Workflow from Start to End**

   - **Overview**: The `main.py` file orchestrates the entire project flow. When you run this script, it executes the entire pipeline from downloading the raw data, transforming it, inserting it into the database, generating reports, and finally displaying the interactive dashboard. 
   - **Steps Performed**:
     - **Download Raw Data**: Initiates the download of the property transaction data through the **API** and stores it in CSV format.
     - **Clean Data**: After the data is downloaded, it is cleaned and transformed (e.g., handling missing values, removing duplicates, calculating average prices).
     - **Insert into Database**: The cleaned data is then upserted into the PostgreSQL database using the **ETL** process. This ensures that duplicate records are avoided and existing records are updated.
     - **Generate Reports**: The script queries the database to fetch the required reports and generates CSV output files for further use.
     - **Dashboard**: The final step is generating the visualizations using **Dash** and displaying them on a dashboard.

---

### 3. **API (`api.py`) - Download Raw Data in Batches**

   - **Functionality**: The `api.py` file handles downloading the raw property transaction data. Since the files can be very large, the data is downloaded in **batches** of 50,000 records at a time.
   - **How It Works**:
     - The file connects to the data source via an API or URL and downloads records in chunks (50,000 at a time).
     - Each batch is appended to the CSV file (`raw_property_data.csv`) in a sequential manner, ensuring that no data is missed.
     - **Batch Download Example**:
       - Downloading 50,000 records at a time and appending to the file ensures large datasets are manageable and won’t cause memory issues.

   - **When to Run**: Run `api.py` first to initiate the downloading process. Once the file is fully downloaded, move on to the next steps.

---

### 4. **ETL Process (`etl.py`) - Clean and Transform Data**

   - **Functionality**: The `etl.py` script handles the data cleaning, transformation, and insertion into the PostgreSQL database.
   - **How It Works**:
     - **Data Cleaning**: It removes duplicates, handles missing values, and performs necessary transformations (such as calculating average prices).
     - **Data Transformation**: Additional transformations are applied, such as removing quotes from certain columns and consolidating address fields.
     - **Upsert to Database**: After cleaning, the script connects to the PostgreSQL database and **upserts** the cleaned data. This ensures that new records are inserted, while existing records are updated if necessary.
     - **Error Handling and Logging**: The script also handles errors during data processing and logs the steps for transparency and troubleshooting.

   - **When to Run**: Run `etl.py` after `api.py` finishes downloading the data. This ensures that the CSV file is ready to be processed and inserted into the database.

---

### 5. **Report Generation (`reports.py`) - Generate Output Reports**

   - **Functionality**: The `reports.py` script is responsible for generating the reports from the database and saving them as CSV files.
   - **How It Works**:
     - The script connects to the PostgreSQL database and runs SQL queries to fetch the necessary data for reports (e.g., average price by property type, high-value transactions).
     - Once the queries are executed, the results are saved as CSV files in the output folder.
     - These CSV files are used later for the dashboard visualizations.

   - **When to Run**: Run `reports.py` after `etl.py` has finished inserting the cleaned data into the database.


### 6. **Dashboard (`dash_app.py`) - Create Interactive Visualizations**

   - **Functionality**: The `dash_app.py` script is responsible for creating the interactive dashboard using **Dash**.
   - **How It Works**:
     - The script loads the generated report CSV files (from `reports.py`), and processes them to create visualizations.
     - It then uses **Plotly** and **Dash** to generate two interactive charts:
       - A bar chart showing the average price by property type.
       - A line or bar chart showing high-value transactions.
     - These visualizations are displayed on a web dashboard for users to interact with.
   
   - **When to Run**: Run `dash_app.py` after `reports.py` finishes generating the report CSV files. The dashboard will use these files to create the visualizations.

### **How to Run the Project in Order**

1. **Run `main.py`**: This script runs the entire end-to-end process. Before running it, make sure that your database engine is up and running, the schema is defined, and sample data has been inserted into all the necessary tables.
2. **Run `etl.py`**: Clean and transform the data, then upsert it into the PostgreSQL database.
3. **Run `reports.py`**: Generate the reports based on the data in the database and save them as CSV files.
4. **Run `dash_app.py`**: Display the generated reports as interactive visualizations in a web dashboard.
5. **Logger Configuration**:  
   - Ensure the `logger.py` file is included in your project. This file is responsible for logging all events throughout the process.  
   - All log information will be recorded in the `data_processing.log` file. This includes detailed logs of data processing, cleaning, transformation, upserts, and any errors encountered during execution.


