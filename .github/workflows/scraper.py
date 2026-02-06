import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials from the GitHub Secret environment variable
creds_raw = os.getenv("CREDENTIALS")
creds_info = json.loads(creds_raw)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
client = gspread.authorize(creds)

# Open your sheet (Make sure you shared it with the client_email from your JSON!)
sheet = client.open("Your Sheet Name").sheet1
