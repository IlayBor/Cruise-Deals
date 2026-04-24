# Cruise Deals Pipeline

An end-to-end ELT data pipeline that scrapes daily cruise deals, stores and transforms the data, and surfaces it through a BI dashboard — all running locally via Docker.

## Architecture

<img width="1875" height="498" alt="image" src="https://github.com/user-attachments/assets/a646af7d-d3ad-48fc-88bb-7cd36d114b39" />

### How it works

1. **Scrape** — Airflow triggers a Python task that logs into vacationstogo.com, scrapes cruise deal listings by region using `requests` + `BeautifulSoup`, and parses them into a structured DataFrame.
2. **Load** — The raw DataFrame is truncated and bulk-inserted into `public.deals` in PostgreSQL via SQLAlchemy.
3. **Transform** — Astronomer Cosmos runs the dbt project inside Airflow. Two model layers clean prices, parse dates, calculate discounts, and materialize a final fact table.
4. **Visualize** — Metabase connects to the `marts.fct_deals` table and displays the processed deals.

## Example

This is my day-to-day report to hunt for deals

<img width="2534" height="1104" alt="image" src="https://github.com/user-attachments/assets/861c6c0e-bd3e-4f58-8829-098e8c9594ec" />

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | Apache Airflow 3.x (CeleryExecutor + Redis) |
| Scraping | Python, `requests`, `BeautifulSoup4`, `pandas` |
| Data Warehouse | PostgreSQL 16 |
| Transformations | dbt-core, dbt-postgres, Astronomer Cosmos |
| Visualization | Metabase |
| Infrastructure | Docker, Docker Compose |

## Project Structure

```
Cruise-Deals/
├── Airflow-Dags/       # Pipeline DAG (scrape → load → dbt)
├── Compose/            # Docker infrastructure for all services
│   ├── Airflow/        # Airflow cluster + custom image
│   ├── Postgres/       # Data warehouse
│   └── Metabase/       # BI tool + its backing DB
└── dbt_project/        # SQL transformation models (staging + marts)
```

## Getting Started

```bash
# From the Compose/ directory
docker compose up -d
```

Airflow UI: http://localhost:8090  
Metabase: http://localhost:4000

## Connecting Metabase to PostgreSQL

After deployment, Metabase requires a one-time manual setup to connect to the PostgreSQL data warehouse. On first launch, go through the Metabase onboarding wizard and enter the following connection details when prompted to add a database:

| Field    | Value                   |
|----------|-------------------------|
| Type     | PostgreSQL              |
| Host     | `cruise_deals_postgres` |
| Port     | `5436`                  |
| Database | `cruise_deals_db`       |
| Username | `ilaybor`               |
| Password | `24342434`              |
| Schema   | `marts`                 |

> **Note:** Use `cruise_deals_postgres` as the host — this is the Docker service hostname, not `localhost`. Metabase connects to PostgreSQL from within the Docker network, so the service name is used for internal routing.
