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
    sheet_data = get_sheet_data(
        sheet_id=os.getenv("GOOGLE_SHEET_ID"), range_name=SHEET_RANGE
    )

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
    for i, row_data in enumerate(
        sheet_data[1:], start=2
    ):  # Start at 2 to match Google Sheet row numbers
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


if __name__ == "__main__":
    sync_sheet_to_db()


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


def delete_row_from_db(row):
    """
    Delete a specific row in the MySQL table.
    :param row: The row number to delete.
    """
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database.")
        return
    cursor = conn.cursor()

    table_name = "sheet1"
    delete_query = f"""
    DELETE FROM `{table_name}`
    WHERE `row_number` = %s
    """
    try:
        cursor.execute(delete_query, (row,))
        conn.commit()
        print(f"Row {row} deleted.")
    except pymysql.MySQLError as e:
        print(f"Error deleting row: {e}")
    finally:
        cursor.close()
        conn.close()


def check_row_exists(row):
    """
    Check if a specific row exists in the MySQL table.
    :param row: The row number to check.
    :return: True if the row exists, otherwise False.
    """
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database.")
        return False
    cursor = conn.cursor()

    table_name = "sheet1"
    check_query = f"""
    SELECT COUNT(*) FROM `{table_name}`
    WHERE `row_number` = %s
    """
    cursor.execute(check_query, (row,))
    exists = cursor.fetchone()[0] > 0

    cursor.close()
    conn.close()

    return exists


def add_row_to_db(row, row_data):
    """
    Add a new row to the MySQL table.
    :param row: The row number to add.
    :param row_data: The data to insert into the new row.
    """
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database.")
        return
    cursor = conn.cursor()

    table_name = "sheet1"

    # Fetch the column names from the database
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
    columns = [col[0] for col in cursor.fetchall() if col[0] != "row_number"]

    if len(row_data) != len(columns):
        print(f"Data length mismatch: expected {len(columns)}, got {len(row_data)}")
        cursor.close()
        conn.close()
        return

    # Prepare the query with actual column names
    column_names = ", ".join([f"`{col}`" for col in columns])
    placeholders = ", ".join(["%s"] * len(row_data))
    insert_query = f"""
    INSERT INTO `{table_name}` (`row_number`, {column_names})
    VALUES (%s, {placeholders})
    """

    try:
        cursor.execute(insert_query, [row] + row_data)
        conn.commit()

        print(f"Row {row} added.")
    except pymysql.MySQLError as e:
        print(f"Error adding row: {e}")

    finally:
        cursor.close()
        conn.close()


def rename_column_in_db(old_column_name, new_column_name):
    """
    Rename a column in the MySQL table if it exists.
    :param old_column_name: The current column name.
    :param new_column_name: The new column name.
    """
    conn = get_db_connection()

    if not conn:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()

    table_name = "sheet1"

    try:
        # Check if the column exists
        check_column_query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME = '{old_column_name}'
        """
        cursor.execute(check_column_query)
        result = cursor.fetchone()

        if not result:
            print(f"Column '{old_column_name}' does not exist in table '{table_name}'.")
            return

        # Proceed to rename the column
        rename_query = f"""
        ALTER TABLE `{table_name}`
        CHANGE COLUMN `{old_column_name}` `{new_column_name}` TEXT
        """
        cursor.execute(rename_query)
        conn.commit()
        print(f"Column '{old_column_name}' renamed to '{new_column_name}'.")

    except pymysql.MySQLError as e:
        print(f"Error renaming column: {e}")

    finally:
        cursor.close()
        conn.close()


def add_column_to_db(column_name):
    # Add a new column to the existing table
    try:
        connection = get_db_connection()  # Get your database connection
        cursor = connection.cursor()
        query = f"ALTER TABLE sheet1 ADD COLUMN `{column_name}` TEXT"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Column '{column_name}' added successfully.")

    except Exception as e:

        print(f"Error adding column: {e}")


def remove_column_from_db(column_name):
    # Remove a column from the existing table
    try:
        connection = get_db_connection()  # Get your database connection
        cursor = connection.cursor()
        query = f"ALTER TABLE sheet1 DROP COLUMN `{column_name}`"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

        print(f"Column '{column_name}' removed successfully.")

    except Exception as e:
        print(f"Error removing column: {e}")
