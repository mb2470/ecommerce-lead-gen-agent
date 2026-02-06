import os
import json
import gspread
import requests
import time
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

# 1. Setup Authentication (Working)
creds_raw = os.getenv("CREDENTIALS")
creds_info = json.loads(creds_raw)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
client = gspread.authorize(creds)

# 2. Open your sheet
# REPLACE "Your Sheet Name" with your actual sheet title!
sheet = client.open("Eccomerce Lead Gen Agent").sheet1

# 3. Scraping Configuration
URL = "https://builtwith.com/ecommerce" 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def run_scraper():
    print("Fetching data...")
    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Blocked or failed. Status: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # This selects the company links from the BuiltWith list
    # Note: BuiltWith changes layouts often; you may need to adjust the selector
    companies = soup.select('td a') 

    for company in companies:
        name = company.text.strip()
        link = company.get('href', 'N/A')

        if name and len(name) > 1:
            print(f"Saving: {name}")
            # Append to Google Sheet: Name, URL, Status
            sheet.append_row([name, link, "Lead Found"])
            
            # Slow down to avoid being blocked by Google or the website
            time.sleep(6) 

if __name__ == "__main__":
    run_scraper()
