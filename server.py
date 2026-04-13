from flask import Flask, request, jsonify
import os

app = Flask(__name__)

latest_signal = {}

# =========================
# RECEIVE TRADINGVIEW ALERT
# =========================
@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal
    
    data = request.json
    print("Received signal:", data)

    latest_signal = data

    return jsonify({"status": "ok"})


# =========================
# SEND SIGNAL TO MT4
# =========================
@app.route('/signal', methods=['GET'])
def signal():
    global latest_signal
    
    temp = latest_signal
    latest_signal = {}  # clear after sending
    
    return jsonify(temp)


# =========================
# RUN SERVER (RENDER FIX)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Server running on port {port}")
    app.run(host="0.0.0.0", port=port)