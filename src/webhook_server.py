import logging
from flask import Flask, request, jsonify
from sheets_sync import *

app = Flask(__name__)

# Setup logger for database changes
db_logger = logging.getLogger("db_changes_logger")
db_logger.setLevel(logging.INFO)  # Set the level to INFO or DEBUG based on your preference

# Create a file handler to log database changes
file_handler = logging.FileHandler("logs/db_changes.log")
file_handler.setLevel(logging.INFO)


# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the db_logger
db_logger.addHandler(file_handler)


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    try:
        data = request.json
        row = data["row"]
        column_name = data["column_name"]
        new_value = data.get("new_value", "")  # Safely handle missing new_value
        old_value = data.get("old_value", "")
        action = data["action"]
        row_data = data.get("row_data")  # List of all data in the row

        if row == 1:
            if old_value and not new_value:
                # Column removed
                db_logger.info(f"Column '{old_value}' removed from database")
                remove_column_from_db(old_value)
            elif old_value and new_value:
                # Column renamed
                db_logger.info(f"Column '{old_value}' renamed to '{new_value}' in database")
                rename_column_in_db(old_value, new_value)
            elif not old_value and new_value:
                # New column added
                db_logger.info(f"New column '{new_value}' added to database")
                add_column_to_db(new_value)
        elif action == "delete":
            db_logger.info(f"Row {row} deleted from database")
            delete_row_from_db(row)
        elif action == "update":
            if check_row_exists(row):
                db_logger.info(f"Cell in row {row}, column '{column_name}' updated to '{new_value}'")
                update_cell_in_db(row, column_name, new_value)
            else:
                try:
                    db_logger.info(f"New row added to database: {row_data}")
                    add_row_to_db(row, row_data)
                except:
                    db_logger.error("Add failed")
        else:
            print(f"Unknown action: {action}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # Initial sync of the Google Sheet to the MySQL database
    sync_sheet_to_db()
    app.run(debug=True)
