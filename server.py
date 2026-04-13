from flask import Flask, request, jsonify

app = Flask(__name__)

latest_signal = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal
    latest_signal = request.json
    return jsonify({"status": "ok"})

@app.route('/signal', methods=['GET'])
def signal():
    global latest_signal
    temp = latest_signal
    latest_signal = {}
    return jsonify(temp)

if __name__ == "__main__":
    print("Server running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)