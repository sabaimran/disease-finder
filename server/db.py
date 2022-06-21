# Use an sqlite database with SQL Alchemy
from typing import List
import sqlalchemy as db
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import sessionmaker

from models import Disorder, Symptom, DisorderSymptomAssociation

def get_db_engine():
    return db.create_engine('sqlite:///diseases.sqlite', echo=True)

session = sessionmaker(bind=get_db_engine())()

def get_disorders():
    return session.query(Disorder).all()

def get_disorder_by_id(id):
    return session.query(Disorder).filter_by(id=id).first()

def get_disorder_by_orpha_code(orpha_code):
    return session.query(Disorder).filter_by(orpha_code=orpha_code).first()

def get_symptoms():
    return session.query(Symptom).all()

def get_symptom_by_hpo_id(hpo_id):
    return session.query(Symptom).filter_by(hpo_id=hpo_id).first()

def get_disorder_symptom_associations_by_symptom_ids(symptom_ids: List[int]):
    return session.query(DisorderSymptomAssociation).filter(DisorderSymptomAssociation.symptom_id.in_(symptom_ids)).all()

def find_most_relevant_disorders(symptom_ids: List[int]):

    # Get all the disorder-symptom associations
    disorder_symptom_associations = get_disorder_symptom_associations_by_symptom_ids(symptom_ids)

    # Sort the disorder-symptom associations by the frequency of the symptom
    disorder_symptom_associations.sort(key=lambda x: x.frequency, reverse=True)

    # Get the top 10 disorders
    top_disorders = disorder_symptom_associations[:10]

    # Get the disorders
    top_disorders_with_symptoms = [{
        'disorder': get_disorder_by_id(disorder_symptom_association.disorder_id),
        'symptoms': get_symptom_by_hpo_id(disorder_symptom_association.symptom_id)} for disorder_symptom_association in top_disorders]

    return top_disorders_with_symptoms

def add_disorders(disorders: List[Disorder]):
    session.add_all(disorders)
    session.commit()

def add_symptoms(symptoms: List[Symptom]):
    seen_symptoms = set()
    for symptom in symptoms:
        if symptom.hpo_id not in seen_symptoms:
            session.add(symptom)
            seen_symptoms.add(symptom.hpo_id)
    session.commit()

def add_disorder_symptom_associations(disorder_symptom_associations: List[DisorderSymptomAssociation]):
    session.add_all(disorder_symptom_associations)
    session.commit()

def add_disorder(name, disorder_type, disorder_group, orpha_code, expert_link) -> Disorder:
    disorder = Disorder(name, disorder_type, disorder_group, orpha_code, expert_link)

    session.add(disorder)
    return disorder

def add_symptom(name, hpo_id) -> Symptom:
    # Check if the symptom already exists
    symptom = get_symptom_by_hpo_id(hpo_id)

    # If the system already exists, return it
    if symptom:
        return symptom

    # If the symptom doesn't exist, add it
    symptom = Symptom(name, hpo_id)
    session.add(symptom)
    session.commit()
    # session.refresh(symptom)
    return symptom

def add_disorder_symptom_association(disease: Disorder, symptom: Symptom, frequency: int) -> DisorderSymptomAssociation:
    session.add(DisorderSymptomAssociation(disease.id, symptom.id, frequency))
    session.commit()
