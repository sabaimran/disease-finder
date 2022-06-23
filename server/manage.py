import sys

import src.models as models
from src.db import DisorderDB
from src.constants import DATABASE_PATH
from src.disease_initializer import populate_diseases

# This module provides utility function for interacting with the database.

def setup_db(db: DisorderDB):
    """Create all tables."""
    models.create_tables(db.engine)

def drop_tables(db: DisorderDB):
    """Drop all tables."""
    models.drop_tables(db.engine)

if __name__ == "__main__":

    # If user passes the --drop-db flag, drop the tables
    if "--drop-tables" in sys.argv:
        db = DisorderDB(DATABASE_PATH)
        drop_tables(db)

    # If user passes the --setup-db flag, initialize the tables
    if "--setup-db" in sys.argv:
        db = DisorderDB(DATABASE_PATH)
        setup_db(db)

    # If the user passes the --populate-db flag, populate the tables
    if "--populate-db" in sys.argv:
        db = DisorderDB(DATABASE_PATH)
        populate_diseases(db=db)
