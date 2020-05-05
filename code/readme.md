# (SETUP) How we think Professor Johnson will run it -- probably without traversing the directory?
0. pg_ctl start
1. Go to /DBPokemon (the root directory of this repo) and run the following commands
2. psql -U postgres < [db-setup.sql](/db-setup.sql)
3. python [retrieve_data.py](/retrieve_data.py)
4. python -m venv **directory**
5. **directory/Scripts/activate**
6. python -m pip install -r [code/requirements.txt](/code/requirements.txt)
7. python [code/load_data.py](/code/load_data.py)
8. python [code/application.py](/code/application.py)

# How to run the application
In /DBPokemon (the root directory of this repo) run the following (assuming your virtual environment and postgres server are up and running):
```bash
python code/application.py
```

# How to use it
As prompted by the welcome logo, you can enter "**help**" in the prompt to get a list of features.

You can also just hit \[**TAB**\] multiple times to cycle through the list of commands you can choose from.

Once you select a command and hit enter, further prompts will engage the user.

**NOTE** Do not do this in the application.py:
```bash
Awesome pokemon DB> FindPokemon ch
```

That is incorrect behavior. Instead, do this:
```bash
Awesome pokemon DB> FindPokemon
Enter part of a pokemon name> ch
```