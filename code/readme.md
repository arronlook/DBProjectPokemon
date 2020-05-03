# How we think Johnson will run it -- probably without traversing the directory?
0. pg_ctl start
1. Go to /DBPokemon (the root directory of this repo) and run the following commands
2. psql -U postgres < [db-setup.sql](/db-setup.sql)
3. python [retrieve_data.py](/retrieve_data.py)
4. python -m venv **directory**
5. **directory/Scripts/activate**
6. python -m pip install -r [code/requirements.txt](/code/requirements.txt)
7. python [code/load_data.py](/code/load_data.py)
8. python [code/application.py](/code/application.py)

