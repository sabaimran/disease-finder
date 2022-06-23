import pytest
from src.db import DisorderDB
import src.models as models
from src.disease_initializer import populate_diseases

class TestDiseaseInitializer:

    def test_populate_disease_get_disorders(self, db, expected_disorders):
        actual_disorders = db.get_disorders()

        assert len(actual_disorders) == len(expected_disorders)

        for (expected, actual) in zip(expected_disorders, actual_disorders):
            assert expected.name == actual.name
            assert expected.disorder_type == actual.disorder_type
            assert expected.disorder_group == actual.disorder_group
            assert expected.orpha_code == actual.orpha_code
            assert expected.expert_link == actual.expert_link

    def test_populate_disease_get_symptoms(self, db, expected_symptoms):
        actual_symptoms = db.get_symptoms()

        assert len(actual_symptoms) == len(expected_symptoms)

        for (expected, actual) in zip(expected_symptoms, actual_symptoms):
            assert expected.name == actual.name
            assert expected.hpo_id == actual.hpo_id

    def test_most_relevant_disorders(self, db, expected_symptom_disorder_associations):
        actual_associations = db.find_most_relevant_disorders([8])

        assert len(actual_associations) == len(expected_symptom_disorder_associations)

        for (expected, actual) in zip(expected_symptom_disorder_associations, actual_associations):
            expected_disorder = expected['disorder']
            actual_disorder = actual['disorder']
            assert expected_disorder.name == actual_disorder.name
            assert expected_disorder.disorder_type == actual_disorder.disorder_type
            assert expected_disorder.disorder_group == actual_disorder.disorder_group
            assert expected_disorder.orpha_code == actual_disorder.orpha_code
            assert expected_disorder.expert_link == actual_disorder.expert_link

            assert expected["score"] == actual["score"]
        

@pytest.fixture
def expected_disorders():
    return [
        models.Disorder(
            name='Alexander disease',
            disorder_type='Disease',
            disorder_group='Disorder',
            orpha_code=58,
            expert_link='http://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=en&Expert=58'),
        models.Disorder(
            name='Alpha-mannosidosis',
            disorder_type='Disease',
            disorder_group='Disorder',
            orpha_code=61,
            expert_link='http://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=en&Expert=61')
        ]

@pytest.fixture
def expected_symptoms():
    return [
        models.Symptom(name='Macrocephaly', hpo_id='HP:0000256'),
        models.Symptom(name='Hyperreflexia', hpo_id='HP:0001347'),
        models.Symptom(name='Megalencephaly', hpo_id='HP:0001355'),
        models.Symptom(name='Kyphosis', hpo_id='HP:0002808'),
        models.Symptom(name='Chorea', hpo_id='HP:0002072'),
        models.Symptom(name='Respiratory insufficiency', hpo_id='HP:0002093'),
        models.Symptom(name='Developmental regression', hpo_id='HP:0002376'),
        models.Symptom(name='Encephalitis', hpo_id='HP:0002383'),
        models.Symptom(name='Aqueductal stenosis', hpo_id='HP:0002410'),
        models.Symptom(name='Dysautonomia', hpo_id='HP:0002459'),
        models.Symptom(name='Bowel incontinence', hpo_id='HP:0002607'),
        models.Symptom(name='Macroglossia', hpo_id='HP:0000158'),
        models.Symptom(name='Coarse facial features', hpo_id='HP:0000280'),
        models.Symptom(name='Hearing impairment', hpo_id='HP:0000365'),
        models.Symptom(name='Cataract', hpo_id='HP:0000518'),
        models.Symptom(name='Intellectual disability', hpo_id='HP:0001249'),
        models.Symptom(name='Global developmental delay', hpo_id='HP:0001263'),
        models.Symptom(name='Splenomegaly', hpo_id='HP:0001744'),
        models.Symptom(name='Hepatomegaly', hpo_id='HP:0002240'),
        models.Symptom(name='Type II diabetes mellitus', hpo_id='HP:0005978'),
        models.Symptom(name='Generalized abnormality of skin', hpo_id='HP:0011354'),
        models.Symptom(name='Mandibular prognathia', hpo_id='HP:0000303'),
        models.Symptom(name='Widely spaced teeth', hpo_id='HP:0000687'),
        models.Symptom(name='Dental malocclusion', hpo_id='HP:0000689'),
        models.Symptom(name='Hallucinations', hpo_id='HP:0000738'),
        models.Symptom(name='Arthritis', hpo_id='HP:0001369'),
        models.Symptom(name='Recurrent respiratory infections', hpo_id='HP:0002205')
    ]

@pytest.fixture
def expected_symptom_disorder_associations():
    return [{
        'disorder': models.Disorder(name='Alexander disease', disorder_type='Disease', disorder_group='Disorder', orpha_code=58, expert_link='http://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=en&Expert=58'),
        'score': 2
    }]

@pytest.fixture
def db(xml_file):
    db = DisorderDB("sqlite:///test-disorders.sqlite")
    models.drop_tables(db.engine)
    models.create_tables(db.engine)

    populate_diseases(db, xml_file)

    return db

@pytest.fixture
def xml_file():
    """
    Returns the path to the XML file containing the test disorder data.
    """
    return "./pytest/en_product4.xml"
