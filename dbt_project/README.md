# dbt Project

Handles all SQL transformations on the raw scraped cruise deals data. Runs inside Airflow via **Astronomer Cosmos**.

## Model Layers

### Staging — `models/staging/stg_scrape__deals.sql`

Reads from `public.deals` (raw data) and produces a clean view in the `staging` schema.

Transformations applied:
- Strip `$` and `,` from price columns, cast to numeric
- Parse sailing dates with year-rollover logic (handles Dec → Jan crossings)
- Calculate `end_date` from start date + duration
- Split `city, state` strings into separate columns
- Extract cruise line and ship name from a combined field
- Compute `percentage_off` discount from original vs. current price

### Marts — `models/marts/fct_deals.sql`

A thin fact table (`marts.fct_deals`) that selects all columns from the staging view and materializes them as a permanent table. This is the table Metabase queries.

## Materialization

| Layer | Schema | Materialized as |
|---|---|---|
| Staging | `staging` | View |
| Marts | `marts` | Table |

## Schema Naming

The `macros/generate_schema_name.sql` macro overrides dbt's default behavior to use exact schema names (`staging`, `marts`) instead of environment-prefixed names.

## Running Manually

```bash
# From the dbt_project/ directory
dbt run
dbt test
```

> In production, dbt is triggered automatically by the Airflow DAG via Astronomer Cosmos after each scrape.
