### Step-by-Step Guide to setting up Postgres and pgadmin4 Image from Docker Hub

#### 1. **Pull the PostgreSQL Docker Image**

Start by pulling the PostgreSQL image from Docker Hub:

```bash
docker pull postgres
```

This will download the latest PostgreSQL image from Docker Hub.

#### 2. **Create a New Volume for Data Persistence**

Now, create a new volume for storing the database data (to ensure that your data persists even if the container is removed):

```bash
docker volume create hm_land_data
```

This will create a volume named `hm_land_data`. You can check the volumes by running:

```bash
docker volume ls
```

You should now see a volume with the name `hm_land_data`.

#### 3. **Run PostgreSQL in a New Docker Container**

Next, run a new PostgreSQL container, attaching it to the volume you just created for persistent storage:

```bash
docker run --name HM_LAND_DB -e POSTGRES_USER=hm_land -e POSTGRES_PASSWORD=12345 -p 5432:5432 -v hm_land_data:/var/lib/postgresql/data -d postgres
```

This command does the following:

- Starts a PostgreSQL container named `HM_LAND_DB`.
- Sets the environment variables for `POSTGRES_USER` and `POSTGRES_PASSWORD` (username and password for the database).
- Maps the container's PostgreSQL port (`5432`) to the same port on your local machine so you can connect to it.
- Mounts the `hm_land_data` volume to the container's data directory (`/var/lib/postgresql/data`) for data persistence.
- Runs the container in the background (`-d`).

You can check the status of your container by running:

```bash
docker ps
```

This should show your `HM_LAND_DB` container running.

#### 4. **Connect to the PostgreSQL Database**

Once the container is running, you can connect to the PostgreSQL database using `psql` inside the container:

```bash
docker exec -it HM_LAND_DB psql -U hm_land
```

This will start a `psql` session where you can run SQL queries.

#### 5. **Create a New Database**

Now that you're inside the PostgreSQL session, create a new database to store your schema:

```sql
CREATE DATABASE price_paid_data;
```

Switch to the new database:

```sql
\c price_paid_data
```

Quit the database
```sql
\q
```

#### 6. **Upload and Execute the Schema SQL Script**

Now, copy your schema SQL file (which contains the table definitions and insertions) into the container. First, ensure your `db_schema.sql` file is ready in your local directory. Then, use the `docker cp` command to copy it into the container:

```bash
docker cp db_schema.sql HM_LAND_DB:/db_schema.sql
```

Now, execute the SQL script inside the container to create the tables and insert sample records:

```bash
docker exec -it HM_LAND_DB psql -U hm_land -d price_paid_data -f /db_schema.sql
```

This command will run your schema into the database.

```
docker cp db_insert.sql HM_LAND_DB:/db_insert.sql
docker exec -it HM_LAND_DB psql -U hm_land -d price_paid_data -f /db_insert.sql
```

This command will run your insert query and insert record to the tables.

```bash
docker exec -it HM_LAND_DB psql -U hm_land -d price_paid_data
```
You should be able to interact with your database directly inside the container by using above command.


#### 7. **Verify the Data**

Once the script has executed successfully, you can verify the tables and data by running queries inside `psql`:

```sql
SELECT * FROM property_types;
SELECT * FROM tenures;
SELECT * FROM ppd_categories;
SELECT * FROM record_statuses;
SELECT * FROM property_transactions;
```

These queries will show you the data from your tables.


Ensure database permissions that the hm_land user has proper permissions on the price_paid_data database.
```sql
GRANT ALL PRIVILEGES ON DATABASE price_paid_data TO hm_land;
```

#### 8. **Stopping and Restarting the Container**

If you stop your container and want to restart it later, you can use the following commands:

- To stop the container:

  ```bash
  docker stop HM_LAND_DB
  ```

- To start the container again:

  ```bash
  docker start HM_LAND_DB
  ```

Since you're using a volume (`hm_land_data`), your data will persist even after stopping or restarting the container.

#### 9. **Removing the Container and Data (Optional)**

If you ever want to start fresh again, you can remove the container and volume as follows:

- To remove the container:

  ```bash
  docker rm HM_LAND_DB
  ```

- To remove the volume:

  ```bash
  docker volume rm hm_land_data
  ```

This will remove both the container and the volume, so all data will be lost.



### 2. **Option A: Running PgAdmin via Docker**
#### Steps:
1. **Pull PgAdmin Docker Image**:
   ```bash
   docker pull dpage/pgadmin4
   ```

2. **Run PgAdmin in a Docker Container**:
   ```bash
   docker run --name pgadmin4 -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin -d dpage/pgadmin4
   ```

3. **Access PgAdmin**:
   - Open your browser and navigate to `http://localhost:5050`.
   - Log in with:
     - Email: `admin@example.com`
     - Password: `admin`.

4. **Connect to PostgreSQL**:
   - Add a new server in PgAdmin.
   - Use the following details:
     - Host: `host.docker.internal` (to connect to the PostgreSQL container from another container on Windows)
     - Port: `5432`
     - Username: `hm_land`
     - Password: `12345`


## **Additional Tips**:

### 3. **Option B: Installing PgAdmin on Windows**
#### Steps:
1. **Download and Install PgAdmin**:
   - Visit the official PgAdmin website: [PgAdmin Downloads](https://www.pgadmin.org/download/).
   - Choose the Windows installer and follow the installation steps.

2. **Set Up Connection**:
   - Open PgAdmin after installation.
   - Create a new server connection:
     - Host: `localhost`
     - Port: `5433` (your PostgreSQL container's port)
     - Database: `hm_land_db`
     - Username: `hm_land`
     - Password: `12345`
