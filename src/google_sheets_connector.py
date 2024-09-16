# core/google_sheets_connector.py
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from googleapiclient.discovery import build
from google.oauth2 import service_account
from config.config import Config

# Path to your credentials file
CREDENTIALS_FILE = "config/credentials.json"

def get_sheets_service():
    """
    Create and return a Google Sheets service object.
    """
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )
    service = build("sheets", "v4", credentials=creds)
    return service

def get_sheet_data(sheet_id, range_name):
    """
    Fetch data from a Google Sheet.
    """
    service = get_sheets_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get("values", [])
    return values
