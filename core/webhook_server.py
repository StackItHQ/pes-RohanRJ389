from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Print the entire JSON data
    print("Webhook triggered")
    print("Received data: ", data)
    
    # Extracting the specific changes from the received data
    if data:
        change_info = data.get('valueRanges', None)
        if change_info:
            for range_data in change_info:
                print(f"Range updated: {range_data.get('range')}")
                print(f"Updated values: {range_data.get('values')}")
        else:
            print("No 'valueRanges' found in the data")
    else:
        print("No data received")

    return jsonify({"status": "Webhook received"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
