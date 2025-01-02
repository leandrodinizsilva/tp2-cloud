import os
import logging
import pandas as pd
import pickle
from flask import Flask,jsonify, request, make_response
from flask_cors import CORS
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

logging.basicConfig(level=logging.DEBUG)
version = os.getenv('APP_VERSION', 0)
model_date = os.getenv('MODEL_DATE', 0)

def readPickle():
    file = '/data/rule1.pkl'
    with open(file, 'rb') as file:
        rules = pickle.load(file)
        return rules

print("iniciei")

@app.route('/api/recommend', methods=['POST'])
def hello():
    data = request.get_json()
    print( "Hello World!")
    app.logger.debug(data)    

    return jsonify({"songs": 12312,
                    "version": version,
                    "model_date": model_date})

    if __name__ == '__main__':
        app.run(host=os.getenv('FLASK_RUN_HOST', '0.0.0.0'),
                port=int(os.getenv('FLASK_RUN_PORT', 31331)),
                debug=True)

@app.before_request
def handle_options_request():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response