from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin

#app = Flask(__name__,static_folder='./frontend/build',static_url_path='')
app = Flask(__name__)
CORS(app)

#@cross_origin()
@app.route("/api/model", methods=["get","post"])
def model():
    data = request.json
    #text = request.json['text']
    # sad
    print(data)
    return jsonify({'status': 200}) 

@app.route("/")
def serve():
    #return send_from_directory(app.static_folder, 'index.html')
    return "hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0')