from flask import Flask, json, jsonify

api = Flask(__name__)
        
@api.route('/test', methods=['GET'])
def test() -> json:
    return jsonify({
        "message": "Hello World"
    })