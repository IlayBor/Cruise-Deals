# PostgreSQL — Data Warehouse

Runs a **PostgreSQL 16** instance that serves as the central data warehouse for the project.

## Connection Details

| Parameter | Value |
|---|---|
| Host (Docker network) | `cruise_deals_postgres` |
| Host (from host machine) | `localhost:5436` |
| Database | `cruise_deals_db` |

## Schema Layout

| Schema | Populated by | Contents |
|---|---|---|
| `public` | Airflow scraper | Raw `deals` table (truncated and reloaded daily) |
| `staging` | dbt | `stg_scrape__deals` view — cleaned and typed data |
| `marts` | dbt | `fct_deals` table — final fact table for Metabase |
