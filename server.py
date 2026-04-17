from flask import Flask, request, jsonify

app = Flask(__name__)

# Stores latest signal for each broker
latest_signals = {
    "vantage": {},
    "ic": {}
}

@app.route("/", methods=["GET"])
def home():
    return "Webhook server is running", 200


# ==================================================
# VANTAGE CHANNEL
# ==================================================
@app.route("/webhook_vantage", methods=["POST"])
def webhook_vantage():
    data = request.get_json(silent=True) or {}

    latest_signals["vantage"] = data

    print("Stored VANTAGE signal:", data)

    return jsonify({
        "status": "ok",
        "channel": "vantage",
        "stored": data
    })


@app.route("/signal_vantage", methods=["GET"])
def signal_vantage():
    # Return current signal WITHOUT clearing it
    signal = latest_signals["vantage"]

    print("Delivered VANTAGE signal:", signal)

    return jsonify(signal)


# ==================================================
# IC MARKETS CHANNEL
# ==================================================
@app.route("/webhook_ic", methods=["POST"])
def webhook_ic():
    data = request.get_json(silent=True) or {}

    latest_signals["ic"] = data

    print("Stored IC signal:", data)

    return jsonify({
        "status": "ok",
        "channel": "ic",
        "stored": data
    })


@app.route("/signal_ic", methods=["GET"])
def signal_ic():
    # Return current signal WITHOUT clearing it
    signal = latest_signals["ic"]

    print("Delivered IC signal:", signal)

    return jsonify(signal)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
