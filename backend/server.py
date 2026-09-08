from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import sys
import os

app = Flask(__name__)
CORS(app)

process = None


@app.route("/start", methods=["POST"])
def start():
    global process

    if process is None or process.poll() is not None:
        project_folder = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        python_file = os.path.join(
            project_folder,
            "virtual_mouse.py"
        )

        process = subprocess.Popen(
            [sys.executable, python_file]
        )

        return jsonify({"status": "started"})

    return jsonify({"status": "already running"})


@app.route("/stop", methods=["POST"])
def stop():
    global process

    if process and process.poll() is None:
        process.terminate()
        process = None

        return jsonify({"status": "stopped"})

    return jsonify({"status": "not running"})


@app.route("/status")
def status():
    running = (
        process is not None
        and process.poll() is None
    )

    return jsonify({"running": running})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )