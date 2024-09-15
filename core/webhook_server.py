# core/webhook_server.py
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook triggered")
    print(request.json)  # To print the data being sent from Google Sheets
    return "Webhook received", 200



if __name__ == "__main__":
    app.run(port=5000)
