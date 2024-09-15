import unittest
import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import Config
from config.settings import (
    GOOGLE_SHEET_ID,
    GOOGLE_API_KEY,
    SYNC_INTERVAL,
)


class TestSettings(unittest.TestCase):

    def test_google_sheets_settings(self):
        self.assertEqual(
            GOOGLE_SHEET_ID, Config.GOOGLE_SHEET_ID, "GOOGLE_SHEET_ID is incorrect"
        )
        self.assertEqual(
            GOOGLE_API_KEY, Config.GOOGLE_API_KEY, "GOOGLE_API_KEY is incorrect"
        )

    def test_sync_interval(self):
        self.assertEqual(SYNC_INTERVAL, 60, "SYNC_INTERVAL is not set correctly")


if __name__ == "__main__":
    unittest.main()
