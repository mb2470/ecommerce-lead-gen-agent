import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# This name must match the 'env' section in your main.yml
creds_raw = os.getenv("CREDENTIALS")
creds_info = json.loads(creds_raw)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
client = gspread.authorize(creds)

# 1. CHANGE THIS to your actual Google Sheet name
# 2. Make sure you SHARED the sheet with the client_email from your JSON!
sheet = client.open("Eccomerce Lead Gen Agent").sheet1

sheet.append_row(["Final Test", "It is working!", "2026-02-05"])
print("Success! Check your Google Sheet.")
