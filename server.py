from flask import Flask, request, jsonify

app = Flask(__name__)

# Stores latest signal for each broker
latest_signals = {
    "vantage": {},
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
