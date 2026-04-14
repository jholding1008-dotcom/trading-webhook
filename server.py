import logging
import os
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
    force=True
)

logger = logging.getLogger(__name__)

latest_signal = {}

logger.info("SERVER VERSION: payload logging enabled")


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


@app.route('/signal', methods=['GET'])
def signal():
    global latest_signal

    sig = latest_signal
    latest_signal = {}

    logger.info("Sending signal to MT4: %s", sig)

    return jsonify(sig)


@app.route('/', methods=['GET'])
def home():
    logger.info("Health check hit")
    return "Trading Webhook Server Running", 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    logger.info("Starting server on port %s", port)
    app.run(host='0.0.0.0', port=port)
