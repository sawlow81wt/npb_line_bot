from flask import Flask, jsonify, request
import json
import getGameScore
app = Flask(__name__)

@app.route("/", methods=['GET'])
def post():
    favor_team = "阪神"
    data = getGameScore.get_today_score_list(favor_team)
    return_data = {idx: {"text":val} for idx, val in enumerate(data)}
    return jsonify({
        'status': 'OK',
        'data': return_data
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
