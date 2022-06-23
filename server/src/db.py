# Use an sqlite database with SQL Alchemy
from typing import List
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from src.models import Disorder, Symptom, DisorderSymptomAssociation

def get_db_engine(db_path: str) -> db.engine.base.Engine:
    return db.create_engine(db_path, echo=True)

class DisorderDB:
    def __init__(self, db_path: str):
        self.engine = get_db_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_disorders(self):
        return self.session.query(Disorder).all()

    def get_disorder_by_id(self, id):
        return self.session.query(Disorder).filter_by(id=id).first()

    def get_symptom_by_id(self, id):
        return self.session.query(Symptom).filter_by(id=id).first()

    def get_disorder_by_orpha_code(self, orpha_code):
        return self.session.query(Disorder).filter_by(orpha_code=orpha_code).first()

    def get_symptoms(self):
        return self.session.query(Symptom).all()

    def get_symptom_by_hpo_id(self, hpo_id):
        return self.session.query(Symptom).filter_by(hpo_id=hpo_id).first()

    def get_disorder_symptom_associations_by_symptom_ids(self, symptom_ids: List[int]):
        return self.session.query(DisorderSymptomAssociation).filter(DisorderSymptomAssociation.symptom_id.in_(symptom_ids)).all()

    def find_most_relevant_disorders(self,symptom_ids: List[int]):

        # Get all the disorder-symptom associations
        disorder_symptom_associations = self.get_disorder_symptom_associations_by_symptom_ids(symptom_ids)

        # Sort the disorder-symptom associations by the frequency of the symptom
        disorder_symptom_associations.sort(key=lambda x: x.frequency, reverse=True)

        # Get the top 10 disorders
        top_disorders = disorder_symptom_associations[:10]

        # Get the disorders
        top_disorders_with_symptoms = [
            {
                'disorder': self.get_disorder_by_id(disorder_symptom_association.disorder_id),
                'symptom': self.get_symptom_by_id(disorder_symptom_association.symptom_id),
                'frequency': disorder_symptom_association.frequency
            } 
            for disorder_symptom_association in top_disorders]

        return top_disorders_with_symptoms

    def add_disorders(self, disorders: List[Disorder]):
        self.session.add_all(disorders)
        self.session.commit()

    def add_symptoms(self, symptoms: List[Symptom]):
        seen_symptoms = set()
        for symptom in symptoms:
            if symptom.hpo_id not in seen_symptoms:
                self.session.add(symptom)
                seen_symptoms.add(symptom.hpo_id)
        self.session.commit()

    def add_disorder_symptom_associations(self, disorder_symptom_associations: List[DisorderSymptomAssociation]):
        self.session.add_all(disorder_symptom_associations)
        self.session.commit()
