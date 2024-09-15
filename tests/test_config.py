# tests/test_config.py
import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import Config


def test_env_variables():
    print("GOOGLE_SHEET_ID:", Config.GOOGLE_SHEET_ID)
    print("GOOGLE_API_KEY:", Config.GOOGLE_API_KEY)
    print("MYSQL_HOST:", Config.MYSQL_HOST)
    print("MYSQL_USER:", Config.MYSQL_USER)
    print("MYSQL_PASSWORD:", Config.MYSQL_PASSWORD)
    print("MYSQL_DB:", Config.MYSQL_DB)


if __name__ == "__main__":
    test_env_variables()
