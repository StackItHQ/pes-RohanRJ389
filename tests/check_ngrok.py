from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is your Flask app running via Ngrok!"

if __name__ == '__main__':
    app.run(port=5000)
