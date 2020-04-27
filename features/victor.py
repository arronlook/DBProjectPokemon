from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from namespaces import all_pokemon
from database_conn import DB_conn

def victor_feature1():
    pokemon_completer = WordCompleter(all_pokemon, ignore_case=True)
    option = prompt('Print a pokemon\'s name>', completer=pokemon_completer)
    print(option)

def victor_feature2():
    connection = DB_conn.getConn()
    cursor = connection.cursor()
    query = "SELECT * FROM tbl_pokemon"
    with cursor as cursor:
        cursor.execute(query)
        print(cursor.fetchall())

__functions__ = {
    "victor_feature1": victor_feature1,
    "victor_feature2": victor_feature2
}