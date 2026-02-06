import os
import json
import gspread
import requests
import time
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

# --- 1. AUTHENTICATION ---
# Pulls the secret named 'CREDENTIALS' from your GitHub repository
creds_raw = os.getenv("CREDENTIALS")
if not creds_raw:
    raise ValueError("GOOGLE_CREDENTIALS secret not found. Check your GitHub Secrets!")

creds_info = json.loads(creds_raw)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
client = gspread.authorize(creds)

# --- 2. SHEET CONFIGURATION ---
# Replace "Your Sheet Name" with the EXACT name of your Google Sheet
# Ensure the sheet is SHARED with: sheet-writer@ivory-voyage-486522-h6.iam.gserviceaccount.com
SHEET_NAME = "Eccomerce Lead Gen Agent" 
sheet = client.open(SHEET_NAME).sheet1

# --- 3. SCRAPER ENGINE ---
def run_optimized_scraper():
    # To get 1,400 leads at 50 per page, we loop through pages 1 to 28
    for page_num in range(1, 29):
        print(f"Processing Page {page_num}...")
        url = f"https://builtwith.com/top-sites/United-States/eCommerce?PAGE={page_num}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Stopped at page {page_num}. Status: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            # Select table rows while skipping the header
            rows = soup.select('table tr')[1:] 

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 6:
                    # Mapping the columns from the BuiltWith table
                    website = cols[1].text.strip()    # Domain name (e.g., tiffany.com)
                    location = cols[2].text.strip()   # e.g., United States
                    sales_rev = cols[4].text.strip()  # e.g., $100m+
                    tech_spend = cols[5].text.strip() # e.g., $10000+

                    print(f"Found: {website}")
                    
                    # Append data to Google Sheet
                    sheet.append_row([website, location, sales_rev, tech_spend, f"Page {page_num}"])
                    
                    # Be gentle: Sleep 2 seconds per row to avoid Google API limits
                    time.sleep(2)

            # Wait 15 seconds before the next page to avoid BuiltWith IP ban
            print(f"Page {page_num} finished. Resting...")
            time.sleep(15)

        except Exception as e:
            print(f"Error on page {page_num}: {e}")
            break

if __name__ == "__main__":
    run_optimized_scraper()
