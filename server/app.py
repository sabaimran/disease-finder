from flask import Flask
from flask_cors import CORS
from flask import request

from src.constants import DATABASE_PATH
from src.db import DisorderDB
from src.models import Disorder, Symptom

app = Flask(__name__)
CORS(app)

db = DisorderDB(DATABASE_PATH)

"""
API Routes.
"""

# Get all disorders
@app.route("/disorders")
def disorders():
    return {
        "disorders": [disorder_to_dict(disorder) for disorder in db.get_disorders()]
    }

# Get all symptoms
@app.route("/symptoms")
def symptoms():
    return {
        "symptoms": [symptom_to_dict(symptom) for symptom in db.get_symptoms()]
    }

# Using a list of symptom IDs, return the likeliest diseases
@app.route("/find-disorders", methods=["POST"])
def find_disorders():
    symptom_ids = request.json["symptomIds"]
    most_relevant_disorders = db.find_most_relevant_disorders(symptom_ids)

    return {
        "disorders": [relevant_disorder_to_dict(disorder_with_metadata) for disorder_with_metadata in most_relevant_disorders]
    }


"""
Helper functions which convert our db types to dictionaries for convenient JSON-parsing.
"""

def relevant_disorder_to_dict(relevant_disorder: dict):
    return {
        "disorder": disorder_to_dict(relevant_disorder['disorder']),
        "score": relevant_disorder['score']
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