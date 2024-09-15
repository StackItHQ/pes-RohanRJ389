import unittest

import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.google_sheets_connector import get_sheet_data
from config.config import Config

class TestGoogleSheetsConnector(unittest.TestCase):
    def test_get_sheet_data(self):
        """
        Test fetching data from Google Sheets and print the content.
        """
        sheet_id = Config.GOOGLE_SHEET_ID
        range_name = 'Sheet1!A1:C10'  # Modify range according to your sheet

        # Fetch data
        data = get_sheet_data(sheet_id, range_name)
        
        # Print the data for verification
        print("Data from Google Sheet:")
        for row in data:
            print(row)
        
        # Optionally, you can include assertions to verify the content
        self.assertIsInstance(data, list, "Data should be a list")
        self.assertGreater(len(data), 0, "Data should not be empty")

if __name__ == "__main__":
    unittest.main()
