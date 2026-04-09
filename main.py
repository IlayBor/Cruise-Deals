import requests
from bs4 import BeautifulSoup

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

for deal_table in deals_tables:
    region_name = deal_table.find_previous_sibling("table", class_="ticker region").get_text(strip=True)

    rows = deal_table.find_all("tr")
    for row in rows:
        fd = row.find("td", class_="fd").get_text(strip=True)
        n = row.find("td", class_="n").get_text(strip=True)
        d = row.find("td", class_="d").get_text(strip=True)
        e = row.find("td", class_="e").get_text(strip=True)
        ls = row.find("td", class_="ls").get_text(strip=True)
        r = row.find("td", class_="r").get_text(strip=True)
        r = row.find("td", class_="r").get_text(strip=True)
        br = row.find("td", class_="br").get_text(strip=True)
        our = row.find("td", class_="our").get_text(strip=True)
        p = row.find("td", class_="p").get_text(strip=True)

        st = row.find("td", class_="st").get_text(strip=True)
        st_suite = row.find("td", class_="st suite").get_text(strip=True)
        st_onboard_credit = row.find("td", class_="st onboard-credit").get_text(strip=True)
        st_resident_rate = row.find("td", class_="st resident-rate").get_text(strip=True)
        st_oceanview = row.find("td", class_="st oceanview").get_text(strip=True)
        st_reduced_again = row.find("td", class_="st reduced-again").get_text(strip=True)
        st_sold_out = row.find("td", class_="st sold-out").get_text(strip=True)
        st_new_offer = row.find("td", class_="st new-offer").get_text(strip=True)
        st_balcony = row.find("td", class_="st balcony").get_text(strip=True)
        