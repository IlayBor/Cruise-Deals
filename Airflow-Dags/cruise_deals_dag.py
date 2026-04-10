from airflow.decorators import dag, task
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import logging

from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping


def get_html_page():
    LOGIN_URL = "https://www.vacationstogo.com/login.cfm?t=y"
    DEALS_URL = "https://www.vacationstogo.com/ticker.cfm?t=y&sp=y"
    EMAIL = "ilaybor2004@gmail.com"

    logging.info("Starting to fetch the HTML page...")
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/131.0.0.0 Safari/537.36",
    })
    session.post(LOGIN_URL, data={"LogEmail": EMAIL}, allow_redirects=False)

    response = session.get(DEALS_URL)
    response.raise_for_status()

    logging.info("Finished fetching the HTML page.")
    return response.text

def scrape_deals(html_content):
    logging.info("Starting to scrape deals...")
    soup = BeautifulSoup(html_content, 'html.parser')

    deals_tables = soup.find_all("table", class_="ticker deals")
    total_rows = []
    for deal_table in deals_tables:
        region_name = deal_table.find_previous_sibling("table", class_="ticker region").get_text(strip=True)

        rows = deal_table.find_all("tr")
        row_keys = ["fd", "n", "d", "e", "ls", "r", "br", "our", "p", "st"]

        for row in rows:
            row_data = {}
            for key in row_keys:
                td = row.find("td", class_=key)
                row_data[key] = td.get_text(strip=True) if td else None
            row_data["region"] = region_name
            total_rows.append(row_data)

    df = pd.DataFrame(total_rows)
    logging.info(f"Scraped {len(df)} deals.")
    return df

def load_df_to_postgres(df, table_name="deals"):
    logging.info("Starting to load deals into PostgreSQL...")
    engine = create_engine("postgresql://ilaybor:24342434@cruise_deals_postgres:5432/cruise_deals_db")
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    logging.info("Finished loading deals into PostgreSQL.")

profile_config = ProfileConfig(
    profile_name="dbt_project",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgres_dbt",
        profile_args={"schema": "public"},
    ),
)

@dag(
    dag_id="cruise_deals",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["cruise", "deals", "scraping"],
)
def cruise_deals_dag():

    @task()
    def scrape_and_load():
        html_content = get_html_page()
        deals_df = scrape_deals(html_content)
        load_df_to_postgres(deals_df, "deals")

    dbt_transform = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=ProjectConfig("/opt/airflow/dbt_project"),
        profile_config=profile_config,
        operator_args={"install_deps": True},
    )

    scrape_and_load() >> dbt_transform


cruise_deals_dag()
