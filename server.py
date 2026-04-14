from flask import Flask, request, jsonify

app = Flask(__name__)

# Store latest signal
latest_signal = {}

print("🚀 SERVER VERSION: payload logging enabled")

# =========================
# WEBHOOK (TradingView → Render)
# =========================
@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal

    data = request.get_json(silent=True)

    print("📩 Webhook payload received:", data)

    if data:
        latest_signal = data
        return jsonify({"status": "ok"}), 200

    print("❌ Invalid webhook body:", request.data)
    return jsonify({"status": "bad request"}), 400


# =========================
# SIGNAL (MT4 EA → Render)
# =========================
@app.route('/signal', methods=['GET'])
def signal():
    global latest_signal

    sig = latest_signal
    latest_signal = {}  # clear after sending

    print("📤 Sending signal to MT4:", sig)

    return jsonify(sig)


# =========================
# ROOT (health check)
# =========================
@app.route('/')
def home():
    return "Trading Webhook Server Running", 200


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
