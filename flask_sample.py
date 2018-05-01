from flask import Flask, jsonify, request
import json
app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello():
    data = request.data
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
