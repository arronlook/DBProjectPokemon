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

# Tree Explanation/Organization
<pre>
/code
|----/features
|    |
|    |----general.py -- handles the "help" command and printing out the
|    |                  logo at application startup
|    |
|    |----themeSong.mp3 -- the pokemon themesong to be played in the background
|    |
|    |----arron.py -- Contains queries for features:
|    |                - GetStrongMoves -- SELECT FROM WHERE ORDER BY
|    |                - GetOffensiveMoves -- SELECT FROM JOIN
|    |                                                   (SELECT FROM JOIN WHERE)
|    |                                       WHERE ORDER BY
|    |                - FindPokemon -- Uses arron_feature3 function
|    |                - FindMoves -- Uses arron_feature3 function
|    |                ----------------
|    |                Helper functions
|    |                arron_feature3 -- SELECT FROM WHERE ORDER BY
|    |                __printTypes -- SELECT FROM WHERE
|    |                __getWeaknesses -- SELECT FROM WHERE (SELECT FROM WHERE)
|    |
|    |----victor.py -- Contains queries for features:
|    |                 - StatAnalyzer -- SELECT FROM WHERE GROUP BY ORDER BY
|    |                 - MoveStatAnalyzer -- SELECT FROM INNER JOIN INNER JOIN
|    |                                        WHERE GROUP BY ORDER BY
|    |
|    |----wendi.py -- Contains queries for feature:
|    |                - GetPokemonFromMove -- SELECT FROM WHERE (SELECT FROM WHERE)
|    |
|    |----wilson.py -- Contains queries for features:
|    |                 - SuperEffective -- Uses helper functions
|    |                 - NotEffective -- Uses helper functions
|    |                 ----------------
|    |                 Helper functions
|    |                 checkType -- SELECT FROM WHERE ORDER BY
|    |                 flyingpress -- SELECT FROM WHERE ORDER BY
|    |                 freezedry -- SELECT FROM ((SELECT FROM WHERE)
|    |                                           UNION
|    |                                           (SELECT FROM WHERE))
|    |                              ORDER BY
|    |                 getType -- SELECT FROM WHERE
|    |                 printPokemonWeak -- SELECT FROM WHERE
|    |                 printPokemonStrong -- SELECT FROM WHERE
|
|----application.py -- the driver code for our application
|
|----database.py -- a singleton for the database connection object
|                -- Sets up the connection to postgres
|                -- Contains no queries. Queries are in the actual
|                   in the *.py files in /code/features described above
|
|----datasets.txt -- a list of where we got our datasets
|                 -- Note that All_moves.csv and pokemon.csv are in
|                    a separate branch because they were from Kaggle
|                    (you can cross reference with the memo we submitted)
|                 -- We abandoned name-moves.csv and used the dataset that
|                    pokeapi used (moves.csv and pokemon_moves.csv) to
|                    get a mapping between pokemon and the moves they
|                    can learn.
|
|----history.txt -- used for our prompt toolkit (UI related)
|
|----load_data.py -- Runs schema.sql and loads the data from the dataset
|                    csvs to the database, after preprocessing into other
|                    csv files.
|                 -- There might be encoding issues with reading and writing
|                    the csv files during the preprocessing step
|
|----namespaces.py -- contains a few static queries to get pokemon names
|                     and move names for the autocompletion in our UI
|
|----readme.md -- this document
|
|----requirements.txt -- list of dependencies for our app to run
|
|----schema.sql -- creates our relations and an index
</pre>
