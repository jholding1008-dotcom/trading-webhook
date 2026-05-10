from flask import Flask, request, jsonify

app = Flask(__name__)

latest_signal = None
latest_ic_signal = None
SECRET_KEY = "CHANGE_ME"

@app.route("/")
def home():
    return "Webhook server running"

@app.route("/webhook_vantage", methods=["POST"])
def webhook_vantage():
    global latest_signal

    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    latest_signal = data

    print("Received TradingView signal:", latest_signal)

    return jsonify({
        "status": "success",
        "message": "Webhook received",
        "signal": latest_signal
    })

@app.route("/latest", methods=["GET"])
def latest():
    global latest_signal

    secret = request.args.get("secret")

    if secret != SECRET_KEY:
        return jsonify({"status": "error", "message": "Invalid secret"}), 403

    if latest_signal is None:
        return "NO_SIGNAL"

    signal_to_send = latest_signal

    # Clear signal after EA reads it, so it does not repeat the same trade
    latest_signal = None

    return jsonify(signal_to_send)

@app.route("/webhook_ic", methods=["POST"])
def webhook_ic():
    global latest_ic_signal

    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    latest_ic_signal = data

    print("Received IC Markets signal:", latest_ic_signal)

    return jsonify({
        "status": "success",
        "message": "IC webhook received",
        "signal": latest_ic_signal
    })


@app.route("/latest_ic", methods=["GET"])
def latest_ic():
    global latest_ic_signal

    secret = request.args.get("secret")

    if secret != SECRET_KEY:
        return jsonify({"status": "error", "message": "Invalid secret"}), 403

    if latest_ic_signal is None:
        return "NO_SIGNAL"

    signal_to_send = latest_ic_signal
    latest_ic_signal = None

    return jsonify(signal_to_send)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
