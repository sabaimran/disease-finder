"""SQLAlchemy Data Models."""
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String


Base = declarative_base()

class Disorder(Base):
    """Disorder object."""

    __tablename__ = "disorder"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(225), nullable=False)
    disorder_type = Column(String(225), nullable=False)
    disorder_group = Column(String(225), nullable=False)
    orpha_code = Column(Integer, unique=True, nullable=False)
    expert_link = Column(String(225), nullable=False)

    def __repr__(self):
        return f"<{self.__class__}(name='{self.name}', disorder_type='{self.disorder_type}', disorder_group='{self.disorder_group}', orpha_code='{self.orpha_code}', expert_link='{self.expert_link}')>"
    
    def __init__(self, name, disorder_type, disorder_group, orpha_code, expert_link):
        self.name = name
        self.disorder_type = disorder_type
        self.disorder_group = disorder_group
        self.orpha_code = orpha_code
        self.expert_link = expert_link

class Symptom(Base):
    """Symptom object."""

    __tablename__ = "symptom"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    hpo_id = Column(String(225), unique=True, nullable=False)
    name = Column(String(225), nullable=False)

    def __repr__(self):
        return f"<{self.__class__}(name='{self.name}', hpo_id='{self.hpo_id}')>"

    def __init__(self, name, hpo_id):
        self.name = name
        self.hpo_id = hpo_id

class DisorderSymptomAssociation(Base):
    """DisorderSymptomAssociation object."""

    __tablename__ = "disease_symptom_association"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    disorder_id = Column(Integer, nullable=False)
    symptom_id = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<{self.__class__}(disease_id='{self.disorder_id}', symptom_id='{self.symptom_id}', frequency='{self.frequency}')>"

    def __init__(self, disorder_id, symptom_id, frequency):
        self.disorder_id = disorder_id
        self.symptom_id = symptom_id
        self.frequency = frequency

def create_tables(engine):
    """Create all tables."""

    Base.metadata.create_all(engine)


def drop_tables(engine):
    """Drop all tables."""

    Base.metadata.drop_all(engine)
