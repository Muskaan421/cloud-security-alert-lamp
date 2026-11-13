from flask import Flask, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

events = [
    {
        "time": "Demo",
        "event": "Application started",
        "status": "NORMAL"
    }
]

failed_logins = 0
alert_active = False


@app.route("/")
def home():
    return render_template(
        "index.html",
        events=events,
        failed_logins=failed_logins,
        alert_active=alert_active
    )


@app.route("/simulate", methods=["POST"])
def simulate():
    global failed_logins, alert_active

    failed_logins += 1
    alert_active = failed_logins >= 3

    status = "SECURITY ALERT" if alert_active else "WARNING"

    events.insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "event": "Simulated failed sign-in",
        "status": status
    })

    return redirect(url_for("home"))


@app.route("/reset", methods=["POST"])
def reset():
    global failed_logins, alert_active

    failed_logins = 0
    alert_active = False
    events.clear()

    events.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "event": "Demo reset",
        "status": "NORMAL"
    })

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)