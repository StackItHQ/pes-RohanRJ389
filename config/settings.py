from config.config import Config

# Define database connection string
DB_CONNECTION_STRING = (
    f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}"
    f"@{Config.MYSQL_HOST}/{Config.MYSQL_DB}"
)

# Google Sheets API settings
GOOGLE_SHEET_ID = Config.GOOGLE_SHEET_ID
GOOGLE_API_KEY = Config.GOOGLE_API_KEY

# Other settings related to synchronization
SYNC_INTERVAL = 60  # Sync interval in seconds, can be adjusted based on needs
