from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logs = []

@app.route("/log", methods=["POST"])
def log():
    logs.append(request.json)
    return {"ok": True}

@app.route("/logs")
def get_logs():
    return jsonify(logs[-20:])

app.run(host="0.0.0.0", port=8000)