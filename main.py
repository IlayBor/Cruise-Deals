import requests
from bs4 import BeautifulSoup
import pandas as pd
LOGIN_URL = "https://www.vacationstogo.com/login.cfm?t=y"
DEALS_URL = "https://www.vacationstogo.com/ticker.cfm?t=y&sp=y"
EMAIL = "ilaybor2004@gmail.com"

# --- Step 1: Login & fetch ---
# session = requests.Session()
# session.headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                   "AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/131.0.0.0 Safari/537.36",
# })
# session.post(LOGIN_URL, data={"LogEmail": EMAIL}, allow_redirects=False)

# response = session.get(DEALS_URL)
# response.raise_for_status()
# print(f"Fetched {len(response.text):,} characters from {DEALS_URL}")

# with open("deals.html", "w", encoding="utf-8") as f:
#     f.write(response.text)
# print("Saved response to deals.html")

# --- Step 2: Parse with BeautifulSoup ---
soup = BeautifulSoup(open("deals.html"), 'html.parser')

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
print(df.head())