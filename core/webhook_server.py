from flask import Flask, request, jsonify
from sheets_sync import (
    sync_sheet_to_db,
    update_cell_in_db,
    add_row_to_db,
    delete_row_from_db,
    check_row_exists,
    rename_column_in_db,
)

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    print("Webhook triggered")
    print(request.json)
    try:
        data = request.json
        row = data["row"]
        column_name = data["column_name"]
        old_value = data["old_value"]
        new_value = data["new_value"]
        action = data["action"]
        row_data = data.get("row_data")  # List of all data in the row

        if row == 1:
            rename_column_in_db(old_value, new_value)
        elif action == "delete":
            delete_row_from_db(row)
        elif action == "update":
            if check_row_exists(row):
                update_cell_in_db(row, column_name, new_value)
            else:
                try:
                    add_row_to_db(row, row_data)
                except:
                    print("Add failed")
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
