from flask import Flask, request, jsonify
from sheets_sync import update_cell_in_db, sync_sheet_to_db

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    print("Webhook triggered")
    print(request.json)
    try:
        data = request.json
        row = data['row']   # Row number from the webhook
        column_name = data['column_name']  # Name of the column
        new_value = data['new_value']  # The new value of the cell

        # Update the database
        update_cell_in_db(row, column_name, new_value)
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print(f"Error handling webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # Initial sync of the Google Sheet to the MySQL database
    sync_sheet_to_db()
    app.run(debug=True)
