import unittest
import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import Config
from config.settings import DB_CONNECTION_STRING, GOOGLE_SHEET_ID, GOOGLE_API_KEY, SYNC_INTERVAL

class TestSettings(unittest.TestCase):
    
    def test_db_connection_string(self):
        expected_connection_string = (
            f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}"
            f"@{Config.MYSQL_HOST}/{Config.MYSQL_DB}"
        )
        self.assertEqual(DB_CONNECTION_STRING, expected_connection_string, "DB_CONNECTION_STRING is incorrect")

    def test_google_sheets_settings(self):
        self.assertEqual(GOOGLE_SHEET_ID, Config.GOOGLE_SHEET_ID, "GOOGLE_SHEET_ID is incorrect")
        self.assertEqual(GOOGLE_API_KEY, Config.GOOGLE_API_KEY, "GOOGLE_API_KEY is incorrect")

    def test_sync_interval(self):
        self.assertEqual(SYNC_INTERVAL, 60, "SYNC_INTERVAL is not set correctly")

if __name__ == "__main__":
    unittest.main()
