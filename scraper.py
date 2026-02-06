import os
import json
import gspread
import requests
import time
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

# --- 1. SETUP ---
creds_raw = os.getenv("CREDENTIALS")
creds_info = json.loads(creds_raw)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
client = gspread.authorize(creds)

# Ensure "Your Sheet Name" matches your actual Google Sheet title!
sheet = client.open("Eccomerce Lead Gen Agent").sheet1

# --- 2. THE TOP SITES COLLECTOR ---
def scrape_top_sites():
    # Loop through the pages to hit your 1,400 goal
    # Each page usually has 50 results, so 28 pages = 1,400 leads
    for page in range(1, 29):
        print(f"Scraping Top Sites Page {page}...")
        url = f"https://builtwith.com/top-sites/United-States/eCommerce?PAGE={page}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Rate limited or blocked at page {page}. Status: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # BuiltWith Top Sites are organized in a <table>
            rows = soup.select('table.table tbody tr')

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    site_name = cols[0].text.strip()
                    sales_rev = cols[1].text.strip()
                    tech_spend = cols[2].text.strip()
                    
                    print(f"Adding: {site_name}")
                    sheet.append_row([site_name, sales_rev, tech_spend, f"Page {page}"])
                    
                    # Pause to stay under Google's API limits
                    time.sleep(1.5)

            # Pause between pages to avoid BuiltWith's anti-bot detection
            print("Page complete. Waiting 10 seconds...")
            time.sleep(10)

        except Exception as e:
            print(f"Error occurred: {e}")
            break

if __name__ == "__main__":
    scrape_top_sites()
