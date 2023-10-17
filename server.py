from flask import Flask, json

api = Flask(__name__)
        
@api.route('/test', methods=['GET'])
def test() -> json:
    return {
        "message": "Hello World"
    }