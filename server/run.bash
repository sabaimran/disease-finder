FLASK_ENV=development

# Iniitalize your virtual environment. Comment out this line after first run.
python3 -m venv .venv

# Activate the virtual environment.
source .venv/bin/activate

# Install dependencies.
pip install -r requirements.txt

# Initialize the database. Comment out this line after first run to speed up the process.
# python3 manage.py --drop-tables --setup-db --populate-db

# Start the server
flask run