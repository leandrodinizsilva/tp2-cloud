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

def recommend(musicList):
    model = readPickle()

    applicable_rules = model[model["antecedents"].apply(lambda antecedents: antecedents.issubset(musicList))]
    applicable_rules = applicable_rules.sort_values(by="confidence", ascending=False)
   
    recommendations = []

    limit = 0 
    for _, row in applicable_rules.iterrows():
        rec_len = len(recommendations)
        for song in row["consequents"]:
            if song not in recommendations and song not in musicList:
                recommendations.append(song)

        rec_len_new = len(recommendations)
        if (rec_len != rec_len_new):
            limit = limit + 1
        if limit >= 10:
            break

    if (len(recommendations) == 0):
        sampled_rules = model.sample(n=5)
        consequents_list = sampled_rules["consequents"].tolist()
        flattened_consequents = [song for consequent in consequents_list for song in consequent]
        flattened_consequents.insert(0, "Resultado Aleatório!")
        recommendations = flattened_consequents            

    return ', '.join(recommendations)


@app.route('/api/recommend', methods=['POST'])
def hello():
    data = request.get_json()
   
    rec = recommend(data["musicList"])     

    return jsonify({"songs": rec,
                    "version": version,
                    "model_date": model_date})

    if __name__ == '__main__':
        app.run(host=os.getenv('FLASK_RUN_HOST', '0.0.0.0'),
                port=int(os.getenv('FLASK_RUN_PORT', 31331)),
                debug=True)
