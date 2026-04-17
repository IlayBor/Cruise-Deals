# Airflow DAGs

## `cruise_deals_dag.py`

The single DAG that drives the entire pipeline. Runs on a **daily schedule** and executes two tasks in sequence.

### Task 1 — `scrape_and_load`

A Python task that:

1. Logs into [vacationstogo.com](https://www.vacationstogo.com) with a session cookie
2. Iterates over cruise regions (Caribbean, Mediterranean, etc.)
3. Scrapes deal tables using `BeautifulSoup`
4. Parses each row into structured fields (ship, dates, price, port, etc.)
5. Loads all records into `public.deals` in PostgreSQL via `SQLAlchemy` (truncate + insert)

### Task 2 — `dbt_transform`

Uses **Astronomer Cosmos** to run the full dbt project in-process inside Airflow. This triggers the `staging` and `marts` model layers and materializes the cleaned data into PostgreSQL.

### Dependencies

```
scrape_and_load >> dbt_transform
```

### Runtime Requirements

These Python packages must be installed in the Airflow environment (handled by the custom Docker image):

- `requests`, `beautifulsoup4`, `pandas`
- `sqlalchemy`, `psycopg2`
- `astronomer-cosmos`, `dbt-postgres`
