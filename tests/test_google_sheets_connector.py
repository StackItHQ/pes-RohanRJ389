# tests/test_google_sheets_connector.py

# core/google_sheets_connector.py
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from googleapiclient.discovery import build
from google.oauth2 import service_account
from config.config import Config

# Path to your credentials file
CREDENTIALS_FILE = "path/to/credentials.json"


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


import unittest
from unittest.mock import patch, MagicMock
from core.google_sheets_connector import get_sheets_service, get_sheet_data


class TestGoogleSheetsConnector(unittest.TestCase):

    @patch("core.google_sheets_connector.build")
    @patch(
        "core.google_sheets_connector.service_account.Credentials.from_service_account_file"
    )
    def test_get_sheets_service(self, mock_creds, mock_build):
        """
        Test the creation of Google Sheets service object.
        """
        # Arrange
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Act
        service = get_sheets_service()

        # Assert
        self.assertEqual(service, mock_service)
        mock_build.assert_called_once_with(
            "sheets", "v4", credentials=mock_creds.return_value
        )

    @patch("core.google_sheets_connector.get_sheets_service")
    def test_get_sheet_data(self, mock_get_sheets_service):
        """
        Test fetching data from Google Sheets.
        """
        # Arrange
        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_values = MagicMock()

        # Mock the API response
        mock_values.get.return_value.execute.return_value = {
            "values": [["Header1", "Header2"], ["Row1Data1", "Row1Data2"]]
        }
        mock_service.spreadsheets.return_value = mock_sheets
        mock_sheets.values.return_value = mock_values
        mock_get_sheets_service.return_value = mock_service

        # Act
        data = get_sheet_data("fake_sheet_id", "Sheet1!A1:B2")

        # Assert
        self.assertEqual(data, [["Header1", "Header2"], ["Row1Data1", "Row1Data2"]])
        mock_get_sheets_service.assert_called_once()
        mock_sheets.values().get.assert_called_once_with(
            spreadsheetId="fake_sheet_id", range="Sheet1!A1:B2"
        )


if __name__ == "__main__":
    unittest.main()
