import os
import sys
import pymysql
from google_sheets_connector import get_sheet_data
from db_connector import get_db_connection

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SHEET_RANGE = "Sheet1!A1:Z1000"  # Adjust range to the size of your sheet

def sync_sheet_to_db():
    """
    Sync the entire Google Sheet with the MySQL database.
    The first row in the sheet is treated as column names.
    """
    sheet_data = get_sheet_data(sheet_id=os.getenv("GOOGLE_SHEET_ID"), range_name=SHEET_RANGE)
    
    if not sheet_data or len(sheet_data) < 2:
        print("No data found in the sheet, or the sheet is empty.")
        return

    # Extract column names from the first row (headers)
    column_names = sheet_data[0]

    # Establish a connection to the MySQL database
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database.")
        return
    cursor = conn.cursor()

    # Drop the existing table (if any) and create a new one with the column names
    table_name = "sheet1"
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create table query that includes `row_number` as the primary key
    create_table_query = f"""
    CREATE TABLE `{table_name}` (
        `row_number` INT PRIMARY KEY AUTO_INCREMENT,
        {', '.join([f'`{col}` TEXT' for col in column_names])}
    )
    """
    cursor.execute(create_table_query)

    # Insert data (starting from the second row since the first row is the header)
    for i, row_data in enumerate(sheet_data[1:], start=2):  # Start at 2 to match Google Sheet row numbers
    # Pad row_data with None (NULL in SQL) if it's shorter than the number of columns
      while len(row_data) < len(column_names):
          row_data.append(None)

      # Insert the data into the table
      values = [f"'{value}'" if value else "NULL" for value in row_data]
      insert_query = f"""
      INSERT INTO `{table_name}` (`row_number`, {', '.join([f'`{col}`' for col in column_names])})
      VALUES ({i}, {', '.join(values)})
      """
      cursor.execute(insert_query)


    conn.commit()
    cursor.close()
    conn.close()

    print("Google Sheet data successfully synced to MySQL")
    
def update_cell_in_db(row, column_name, new_value):
    """
    Update a specific cell in the MySQL table when the Google Sheet changes.
    :param row: The row number of the change.
    :param column_name: The column name of the cell.
    :param new_value: The new value to update in the database.
    """
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database.")
        return
    cursor = conn.cursor()

    # Update the specified cell in the MySQL table
    table_name = "sheet1"
    update_query = f"""
    UPDATE `{table_name}`
    SET `{column_name}` = %s
    WHERE `row_number` = %s
    """
    try:
        cursor.execute(update_query, (new_value, row))
        conn.commit()
        print(f"Row {row}, Column '{column_name}' updated with value: {new_value}")
    except pymysql.MySQLError as e:
        print(f"Error updating cell: {e}")
    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    sync_sheet_to_db()
