from typing import Any, List, Tuple
import urllib.request
import xml.etree.ElementTree as ET

from models import Disorder, Symptom, DisorderSymptomAssociation

from db import get_disorder_by_orpha_code, get_symptom_by_hpo_id, add_disorders, add_symptoms, add_disorder_symptom_associations

frequencies = {
    'Excluded (0%)': 0,
    'Very rare (<4-1%)': 1,
    'Occasional (29-5%)': 2,
    'Frequent (79-30%)': 3,
    'Very frequent (99-80%)': 4,
    'Obligate (100%)': 5
}

class RawDisorderSymptomAssociation:
    """
    Stores the raw association between disorders and symptoms.
    This is needed to later associate the objects stored in the db with their primary keys.
    """

    def __init__(self, symptom: Symptom, disorder: Disorder, frequency: int):
        self.symptom = symptom
        self.disorder = disorder
        self.frequency = frequency

def populate_diseases() -> None:
    """
    Retrieves the XML file from the server and parses it.
    Converts the raw data into the relevant data models and stores them in the database.
    """

    url = "http://www.orphadata.org/data/xml/en_product4.xml"
    xml_file = urllib.request.urlopen(url)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    disorders = []
    symptoms = []
    raw_disorder_symptom_associations = []

    for hpo_disorder_set_status in root.iter('HPODisorderSetStatus'):

        (disorder, hpo_disorder_association_list) = process_disorder(hpo_disorder_set_status)

        disorders.append(disorder)

        # Iterate through all of the HPO disease associations
        for hpo_disorder_association in hpo_disorder_association_list.iter('HPODisorderAssociation'):
            (symptom, disorder_symptom_association) = process_disorder_association(hpo_disorder_association, disorder)
            symptoms.append(symptom)
            raw_disorder_symptom_associations.append(disorder_symptom_association)

    add_disorders(disorders)
    add_symptoms(symptoms)

    final_disorder_symptom_associations = []

    # From the raw disorder and symptoms which are associated with each other, create links to the objects stored in the db.
    for association in raw_disorder_symptom_associations:
        final_disorder_symptom_associations.append(make_disorder_symptom_association(association))

    add_disorder_symptom_associations(final_disorder_symptom_associations)

def make_disorder_symptom_association(raw_association: RawDisorderSymptomAssociation) -> DisorderSymptomAssociation:
    """
    Creates a new disease-symptom association object.
    """
    disorder_id = get_disorder_by_orpha_code(raw_association.disorder.orpha_code).id
    symptom_id = get_symptom_by_hpo_id(raw_association.symptom.hpo_id).id
    return DisorderSymptomAssociation(disorder_id, symptom_id, raw_association.frequency)

def process_disorder(disorder_element) -> Tuple[Disorder, List[Any]]:
    """
    Processes a disease element from the XML file.
    Creates a new disorder object and returns it along with the list of HPO disease associations.
    """
    disorder_element = disorder_element.find('Disorder')
    orpha_code = disorder_element.find('OrphaCode').text
    disorder_name = disorder_element.find('Name').text
    expert_link = disorder_element.find('ExpertLink').text

    disorder_type = disorder_element.find('DisorderType')
    disorder_type_name = disorder_type.find('Name').text

    disorder_group = disorder_element.find('DisorderGroup')
    disorder_group_name = disorder_group.find('Name').text

    hpo_disorder_association_list = disorder_element.find("HPODisorderAssociationList")

    # Create a disorder object to be added to the database
    disorder = Disorder(disorder_name, disorder_type_name, disorder_group_name, orpha_code, expert_link)

    return disorder, hpo_disorder_association_list

def process_disorder_association(hpo_disorder_association: List[Any], disorder: Disorder) -> Tuple[Symptom, DisorderSymptomAssociation]:
    """
    Processes a disease-symptom association element from the XML file.
    """
    hpo_element = hpo_disorder_association.find('HPO')
    hpo_id = hpo_element.find("HPOId").text
    hpo_term = hpo_element.find("HPOTerm").text

    # Create a symptom to be added to the database.
    symptom = Symptom(hpo_term, hpo_id)

    hpo_frequency_element = hpo_disorder_association.find('HPOFrequency')
    hpo_frequency = hpo_frequency_element.find("Name").text

    # Create a raw disease-symptom association object. We'll later associate the disorder and symptoms to their ids for newly-created objects stored in the database.
    disorder_symptom_association = RawDisorderSymptomAssociation(symptom, disorder, frequencies[hpo_frequency])

    return (symptom, disorder_symptom_association)
