# Airflow — Docker Setup

Runs a full **Apache Airflow 3.x** cluster using the **CeleryExecutor** for parallel task execution.

## Services

| Container | Role |
|---|---|
| `airflow-apiserver` | REST API + Airflow UI (port `8090`) |
| `airflow-scheduler` | Parses schedules and triggers task instances |
| `airflow-dag-processor` | Parses DAG files in a separate process |
| `airflow-worker` | Executes tasks (Celery worker) |
| `airflow-triggerer` | Handles deferrable operators |
| `redis` | Celery message broker between scheduler and worker |
| `postgres` | Airflow's internal metadata database |

## Custom Image

The `Airflow-Image/Dockerfile` extends `apache/airflow:3.1.6` with:
- `git` (system package)
- All Python deps from `requirements.txt`:
  - `dbt-postgres`, `astronomer-cosmos` — for dbt-in-Airflow execution
  - `pandas`, `sqlalchemy`, `beautifulsoup4` — for the scraper task

## Volume Mounts

The following host paths are bind-mounted into the worker and scheduler:

| Host path (from repo root) | Container path |
|---|---|
| `Airflow-Dags/` | `/opt/airflow/dags` |
| `dbt_project/` | `/opt/airflow/dbt_project` |
| `Compose/Airflow/Extras/logs/` | `/opt/airflow/logs` |
| `Compose/Airflow/Extras/config/` | `/opt/airflow/config` |
| `Compose/Airflow/Extras/plugins/` | `/opt/airflow/plugins` |

## Configuration

Key settings in `.env`:

```env
AIRFLOW_UID=50000
AIRFLOW_PROJ_DIR=../../         # Resolves volume mounts from repo root
_AIRFLOW_WWW_USER_USERNAME=...
_AIRFLOW_WWW_USER_PASSWORD=...
AIRFLOW_CONN_POSTGRES_DBT=...   # SQLAlchemy URI for dbt → data warehouse connection
```
