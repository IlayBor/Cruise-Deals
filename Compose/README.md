# Compose

Docker Compose configuration for the entire Cruise Deals stack. All services run on a shared Docker bridge network (`cruise-deals-network`) so they can resolve each other by hostname.

## Services Overview

| Service | Description | Exposed Port |
|---|---|---|
| Airflow cluster | Orchestration (scheduler, worker, API server, etc.) | `8090` |
| `cruise_deals_postgres` | Data warehouse (raw + transformed data) | `5436` |
| Metabase | BI dashboard | `4000` |
| `metabaseappdb` | Metabase's internal state DB | — |

## Structure

```
Compose/
├── docker-compose.yml   # Root file — merges all sub-composes, defines shared network
├── Airflow/             # Airflow 3.x CeleryExecutor cluster
├── Postgres/            # Data warehouse PostgreSQL instance
└── Metabase/            # Metabase + its backing Postgres
```

## Usage

```bash
# Start the full stack from this directory
docker compose up -d

# Tear down
docker compose down
```

> All volume mounts resolve from the repo root. The `AIRFLOW_PROJ_DIR=../../` env var in `Airflow/.env` controls this.

## Sub-compose files

Each subdirectory has its own `docker-compose.yml` and README with service-specific details.
