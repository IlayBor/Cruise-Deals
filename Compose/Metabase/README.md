# Metabase — Visualization

Runs **Metabase** as the BI layer for exploring and dashboarding the processed cruise deals.

## Services

| Container | Role |
|---|---|
| `metabase` | Metabase application (port `4000`) |
| `metabaseappdb` | Postgres 17 — stores Metabase's internal state (questions, dashboards, users) |

## Data Source

Metabase is manually connected (via its UI) to the data warehouse:

- **Host:** `cruise_deals_postgres`
- **Database:** `cruise_deals_db`
- **Schema:** `marts`
- **Table:** `fct_deals`

## Access

Navigate to [http://localhost:4000](http://localhost:4000) after running `docker compose up`.
