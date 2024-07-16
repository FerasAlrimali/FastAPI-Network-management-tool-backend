# FastAPI-Network-management-tool-backend
# FastAPI-Network-management-tool-backend
This app is built on Poetry 
So to run the app u can use this command in the root file (poetry run start)
Make sure to install all the dependencies using the command (pip install -r requirements.txt) or poetry install
don't forget to change the DB credentials in the conf.py file 
for DB management we are using alembic so make sure to run these commands before running the app to create the DB and the tables (alembic revision --autogenerate -m "first_commit", alembic upgrade head) 