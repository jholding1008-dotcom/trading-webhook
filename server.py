from flask import Flask, request, jsonify

app = Flask(__name__)

SECRET_KEY = "CHANGE_ME"

signals = {
    "xau_1m": None,
    "btc_1m": None,
    "nas_1m": None,
    "xau_5m": None,
    "btc_5m": None,
    "ustec_5m": None,
}


@app.route("/")
def home():
    return "Trading webhook server running"


def save_signal(key):
    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    signals[key] = data
    print(f"Received {key} signal:", data)

    return jsonify({
        "status": "success",
        "route": key,
        "signal": data
    })


def get_signal(key):
    secret = request.args.get("secret")

    if secret != SECRET_KEY:
        return jsonify({"status": "error", "message": "Invalid secret"}), 403

    if signals[key] is None:
        return "NO_SIGNAL"

    signal = signals[key]
    signals[key] = None

    return jsonify(signal)


# ======================
# VANTAGE 1 MIN ROUTES
# ======================

@app.route("/webhook_xau_1m", methods=["POST"])
def webhook_xau_1m():
    return save_signal("xau_1m")


@app.route("/latest_xau_1m", methods=["GET"])
def latest_xau_1m():
    return get_signal("xau_1m")


@app.route("/webhook_btc_1m", methods=["POST"])
def webhook_btc_1m():
    return save_signal("btc_1m")


@app.route("/latest_btc_1m", methods=["GET"])
def latest_btc_1m():
    return get_signal("btc_1m")


@app.route("/webhook_nas_1m", methods=["POST"])
def webhook_nas_1m():
    return save_signal("nas_1m")


@app.route("/latest_nas_1m", methods=["GET"])
def latest_nas_1m():
    return get_signal("nas_1m")


# ======================
# IC MARKETS 5 MIN ROUTES
# ======================

@app.route("/webhook_xau_5m", methods=["POST"])
def webhook_xau_5m():
    return save_signal("xau_5m")


@app.route("/latest_xau_5m", methods=["GET"])
def latest_xau_5m():
    return get_signal("xau_5m")


@app.route("/webhook_btc_5m", methods=["POST"])
def webhook_btc_5m():
    return save_signal("btc_5m")


@app.route("/latest_btc_5m", methods=["GET"])
def latest_btc_5m():
    return get_signal("btc_5m")


@app.route("/webhook_ustec_5m", methods=["POST"])
def webhook_ustec_5m():
    return save_signal("ustec_5m")


@app.route("/latest_ustec_5m", methods=["GET"])
def latest_ustec_5m():
    return get_signal("ustec_5m")


# ======================
# OLD ROUTES - OPTIONAL BACKUP
# ======================

@app.route("/webhook_vantage", methods=["POST"])
def webhook_vantage():
    return save_signal("xau_1m")


@app.route("/latest", methods=["GET"])
def latest():
    return get_signal("xau_1m")


@app.route("/webhook_ic", methods=["POST"])
def webhook_ic():
    return save_signal("xau_5m")


@app.route("/latest_ic", methods=["GET"])
def latest_ic():
    return get_signal("xau_5m")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
