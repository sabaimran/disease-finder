from flask import Flask
from flask_cors import CORS
from flask import request

from db import get_disorders, get_symptoms, find_most_relevant_disorders

from models import Disorder, Symptom

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/disorders")
def disorders():
    return {
        "disorders": [disorder_to_dict(disorder) for disorder in get_disorders()]
    }

@app.route("/symptoms")
def symptoms():
    return {
        "symptoms": [symptom_to_dict(symptom) for symptom in get_symptoms()]
    }

# Define a POST request which takes a list of symptom IDs and returns the likeliest diseases
@app.route("/find-disorders", methods=["POST"])
def find_disorders():
    print(request)
    print(request.data)
    print('request in find-disorders', request.json)
    symptom_ids = request.json["symptomIds"]
    most_relevant_disorders_with_symptoms = find_most_relevant_disorders(symptom_ids)

    return {
        "disorders": [disorder_to_dict(disorder_with_symptom['disorder']) for disorder_with_symptom in most_relevant_disorders_with_symptoms]
    }

def disorder_to_dict(disorder: Disorder):
    return {
        "id": disorder.id,
        "name": disorder.name,
        "disorderType": disorder.disorder_type,
        "disorderGroup": disorder.disorder_group,
        "orphaCode": disorder.orpha_code,
        "expertLink": disorder.expert_link
    }

def symptom_to_dict(symptom: Symptom):
    return {
        "id": symptom.id,
        "hpoId": symptom.hpo_id,
        "name": symptom.name,
    }
    
if __name__ == "__main__":
    app.run()