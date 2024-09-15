import os, sys
import pymysql
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.google_sheets_connector import get_sheet_data
from core.db_connector import get_db_connection
from core.data_validator import validate_date, validate_status

# You can adjust this based on your sheet data range
SHEET_RANGE = "Sheet1!A1:D100"  # Change this to match the actual data range

def sync_google_sheet_to_mysql():
    """
    Fetch data from Google Sheets and update the MySQL task_list table.
    """
    # Fetch the data from the Google Sheet
    sheet_data = get_sheet_data(sheet_id=os.getenv("GOOGLE_SHEET_ID"), range_name=SHEET_RANGE)

    if not sheet_data or len(sheet_data) < 2:
        print("No data found in the sheet, or sheet is empty.")
        return

    # Establish a connection to the MySQL database
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()

    # Skip the header row (assumes first row is the header)
    for row in sheet_data[1:]:
        sl_no = int(row[0])  # Sl. No
        task = row[1]        # Task

        # Validate and convert status and deadline
        status = validate_status(row[2])  # Status (convert to boolean)
        deadline = validate_date(row[3])  # Deadline (convert to MySQL date format)

        if status is None or deadline is None:
            print(f"Skipping row {row[0]} due to invalid data.")
            continue

        # Insert or update the task in the MySQL table
        query = """
        INSERT INTO task_list (Sl_No, Task, Status, Deadline)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE Task=%s, Status=%s, Deadline=%s
        """
        try:
            cursor.execute(query, (sl_no, task, status, deadline, task, status, deadline))
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")

    # Commit the transaction
    conn.commit()
    
    # Close the cursor and the connection
    cursor.close()
    conn.close()

    print("Google Sheet data successfully synced to the MySQL database.")

if __name__ == "__main__":
    sync_google_sheet_to_mysql()
