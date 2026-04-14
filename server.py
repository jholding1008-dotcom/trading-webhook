import logging
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

# Force logs to stdout so Render captures them
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
    force=True
)

logger = logging.getLogger(__name__)

latest_signal = {}

logger.info("SERVER VERSION: payload logging enabled")

# =========================
# WEBHOOK (TradingView → Render)
# =========================
@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal

    data = request.get_json(silent=True)

    logger.info("Webhook payload received: %s", data)
    logger.info("Raw webhook body: %s", request.get_data(as_text=True))

    if data:
        latest_signal = data
        return jsonify({"status": "ok"}), 200

    logger.warning("Invalid webhook body")
    return jsonify({"status": "bad request"}), 400


# =========================
# SIGNAL (MT4 EA → Render)
# =========================
@app.route('/signal', methods=['GET'])
def signal():
    global latest_signal

    sig = latest_signal
    latest_signal = {}

    logger.info("Sending signal to MT4: %s", sig)

    return jsonify(sig)


# =========================
# ROOT
# =========================
@app.route('/')
def home():
    logger.info("Health check hit")
    return "Trading Webhook Server Running", 200
