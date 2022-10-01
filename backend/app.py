from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Index"

@app.route("/api/model", methods=["get","post"])
def model():
    data = request.json
    #text = request.json['text']
    print(data)
    return jsonify({'status': 200}) 