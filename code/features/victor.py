from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from namespaces import all_types, all_stats, all_moves
from database import DB_conn

def victor_feature1():
    print("Given the type(s) and stat(s), the analyzer will rank Pokemon ordered by the sum of the given stats")
    while True:
        # This while-loop sanitizes input for type
        type_completer = WordCompleter(all_types, ignore_case=True)
        input_types = prompt('Please enter type(s), seperated by space>', completer=type_completer)
        if input_types == "exit":
            return 
        input_types_arr = input_types.split()
        num_types = len(input_types_arr)
        
        if num_types < 1 or num_types > 2:
            print("Wrong number of type, please try again")
            continue

        if not all(poke_type in all_types for poke_type in input_types_arr):
            print("One of the type is not valid, please try again")
            continue
        break
        
    while True:
        # This while-loop sanitizes input for stats
        stat_completer = WordCompleter(all_stats, ignore_case=True)
        input_stats = prompt('Please enter stats you would like to analyze>', completer=stat_completer)
        if input_stats == "exit":
            return 
        input_stats_arr = input_stats.split()
        num_stats = len(input_stats_arr)
        if num_stats < 1 or num_stats > 6:
            print("Number of stats is incorrect. The range is 1-6")
            continue

        if not all(stat in all_stats for stat in input_stats_arr):
            print("Some stats you entered is invalid, please try again")
            continue

        break

    query = """
        SELECT
            tbl_pokemon.name,
            SUM({}) AS total
        FROM
            tbl_pokemon
        WHERE
            tbl_pokemon.type1 = %s
    """.format(input_stats.replace(' ', ' + '))
    
    if num_types == 2:
        query += """
            AND 
            tbl_pokemon.type2 = %s
        """

    query += """
        GROUP BY tbl_pokemon.name
        ORDER BY total DESC
    """
    connection = DB_conn.getConn()
    cursor = connection.cursor()
    with cursor as cursor:
        if num_types == 1:
            cursor.execute(query, (input_types_arr[0], ))
        else:
            cursor.execute(query, (input_types_arr[0], input_types_arr[1],))
        res = cursor.fetchall()
    
    print("Here are your results:")
    print("---------------------------")
    print("|   Pokemon   |   Total   |")
    print("---------------------------")
    for entry in res:
        print("|{:<12} | {:^10}|".format(entry[0], entry[1]))
    if len(res) == 0:
        print("|        No Results       |")
    print("---------------------------")

def victor_feature2():
    print("Given a move, find all the pokemon that can learn it ordered by stat.")
    while True:
        # This while-loop sanitizes input for type
        move_completer = WordCompleter(all_moves, ignore_case=True)
        move = prompt('Please a move>', completer=move_completer)
        if move == "exit":
            return 

        if move not in all_moves:
            print("move is not valid, please try again")
            continue
        break

    query = """
        SELECT
            tbl_pokemon.name,
            SUM(tbl_pokemon.hp + 
                tbl_pokemon.speed + 
                tbl_pokemon.attack + 
                tbl_pokemon.sp_attack + 
                tbl_pokemon.defense + 
                tbl_pokemon.sp_defense) AS total
        FROM
            tbl_allmoves
        INNER JOIN tbl_pokemon_moves ON tbl_allmoves.name = tbl_pokemon_moves.move_name
        INNER JOIN tbl_pokemon ON tbl_pokemon.pokedex_number = tbl_pokemon_moves.pokemon_id
        WHERE tbl_allmoves.name = %s
        GROUP BY tbl_pokemon.name
        ORDER BY total DESC;
    """
    connection = DB_conn.getConn()
    cursor = connection.cursor()
    with cursor as cursor:
        cursor.execute(query, (move,))
        res = cursor.fetchall()

    print("Here are your results:")
    print("---------------------------")
    print("|   Pokemon   |   Total   |")
    print("---------------------------")
    for entry in res:
        print("|{:<12} | {:^10}|".format(entry[0], entry[1]))
    if len(res) == 0:
        print("|        No Results       |")
    print("---------------------------")

__functions__ = {
    "StatAnalyzer": victor_feature1,
    "MoveStatAnalyzer": victor_feature2
}
