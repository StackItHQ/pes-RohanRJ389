from flask import Flask, request, jsonify
from sheets_sync import update_cell_in_db, sync_sheet_to_db, delete_row_from_db

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    print("Webhook triggered")
    print(request.json)
    try:
        data = request.json
        row = data["row"]
        column_name = data["column_name"]
        new_value = data["new_value"]
        action = data["action"]

        if action == "delete":
            delete_row_from_db(row)
        elif action == "update":
            update_cell_in_db(row, column_name, new_value)
        else:
            print(f"Unknown action: {action}")
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # Initial sync of the Google Sheet to the MySQL database
    sync_sheet_to_db()
    app.run(debug=True)
