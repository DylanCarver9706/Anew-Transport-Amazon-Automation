Create a Python Virtual environment:
python -m venv <env name>
NOTE: Python 3+ is required

Start python virtual environment:
.\<env name>\Scripts\activate

Create an auth.json file with the key value pairs for Auth on Pro adb. The required key/value pairs are:
"pro_username"
"pro_password"
"database_host"
"database_user"
"database_password"
"database_database"

Install dependencies:
pip install -r requirements.txt

Start database in MySQL Workbench:
Open MySQL Workbench app
Login
Start the DB instance
If this is the first time opening the instance, run the contents of the SQL file in this repo to create the schema

Run python flask_api.py to start the Flask api

Login to ProABD in the Chrome Browser that appears

