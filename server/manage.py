import sqlalchemy as db
import models
import db
import sys

from disease_initializer import populate_diseases

# This module provides utility function for interacting with the database.

def setup_db():
    """Create all tables."""
    engine = db.get_db_engine()
    models.create_tables(engine)

def drop_tables():
    """Drop all tables."""
    engine = db.get_db_engine()
    models.drop_tables(engine)

if __name__ == "__main__":
    # If user passes the --drop-db flag, drop the tables
    if "--drop-tables" in sys.argv:
        drop_tables()

    # If user passes the --setup-db flag, initialize the tables
    if "--setup-db" in sys.argv:
        setup_db()

    # If the user passes the --populate-db flag, populate the tables
    if "--populate-db" in sys.argv:
        populate_diseases()
