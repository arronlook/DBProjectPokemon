from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from database import DB_conn
from namespaces import all_pokemon, all_moves
import psycopg2.extras

"""
Initialization
"""
PokemonComplete = WordCompleter(all_pokemon + ["Exit", "Quit"], ignore_case=True)

def __printTypes(name):
    """
    Prints what the pokemon is and its types
    @param name is the name of the pokemon to get the dual types of
    """
    query = """
            SELECT type1, type2
            FROM tbl_pokemon
            WHERE name ILIKE %s
            """
    conn = DB_conn.getConn()
    with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
        cursor.execute(query, (name,))
        record = cursor.fetchone()
        type1 = record["type1"]
        type2 = record["type2"]
        if type2 == '' or type1 == type2: 
            print("{} is a {} type pokemon".format(name, type1), flush=True)
        else:
            print("{} is a {} {} type pokemon".format(name, type1, type2), flush=True)
        

def __getWeaknesses(name):
    """
    @param name is the name of the pokemon to get weaknesses for
    @returns a list of types that the pokemon is weak against
    """
    # halfQuery is completed a little later in the code
    halfQuery = """
                FROM tbl_weakness
                WHERE (type1, type2) IN (SELECT type1, type2
                                         FROM tbl_pokemon
                                         WHERE name ILIKE %(pokemon_name)s);
                          """
    ListOfTypesQuery = """
                       SELECT SUBSTRING(column_name, 9)
                       FROM information_schema.columns
                       WHERE table_schema='public' AND table_name='tbl_weakness' AND column_name NOT ILIKE 'type%';
                       """
    weaknesses = []
    connection = DB_conn.getConn()
    with connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
        cursor.execute(ListOfTypesQuery)
        types = [x[0] for x in cursor.fetchall()]

        # types is from a static query, so it is safe. Just wanted to ensure the order and flexibility
        query = "SELECT " + ", ".join(["against_" + x for x in types]) + halfQuery;

        cursor.execute(query, {"pokemon_name":name})
        row = cursor.fetchone()
        
        for i in range(len(types)):
            if row[i] > 1:
                weaknesses.append(types[i])
    return weaknesses

def __printMoveTable(moves, minName=15, minEffect=25):
    """
    Prints out the move table based on the moves provided
    @param moves is a list of (Name, Effect, Type, PP) tuples
    @param minName is the minimum width of a name per row
    @param minEffect is the minimum width of an effect description per row
    """
    padding = [4, 6, 4, 2]
    # Calculate padding
    if len(moves) != 0:
        # Clean up the result first
        for i in range(len(moves)):
            moves[i] = (moves[i]["name"].strip() if moves[i][0] is not None else "",
                        moves[i]["effect"].strip() if moves[i][1] is not None else "",
                        moves[i]["type"].strip() if moves[i][2] is not None else "",
                        str(moves[i]["pp"]).strip() if moves[i][3] is not None else "")
        for row in moves:
            for i in range(len(padding)):
                if padding[i] < len(row[i]):
                    padding[i] = len(row[i])
    # Limit name to minName char
    # limit effect to minEffect char
    padding[0] = min(minName, padding[0])
    padding[1] = min(minEffect, padding[1])

    from math import ceil;
    # Output results
    h_line = "-" * (sum(padding) + 13)
    print(h_line, flush=True)
    line = "| Name" + " " * (padding[0] - 4) + " |" + \
        " Effect" + " " * (padding[1] - 6) + " |" + \
        " Type" + " " * (padding[2] - 4) + " |" + \
        " PP" + " " * (padding[3] - 2) + " |"
    print(line, flush=True)
    print(h_line, flush=True)
    for row in moves:
        num_lines = max(ceil(len(row[0])/float(padding[0])), ceil(len(row[1])/float(padding[1])))
        for i in range(num_lines):
            line = "| "
            if i==0 and padding[0] >= len(row[0]):
                line += row[0] + " " * (padding[0] - len(row[0])) + " | "
            else: # elif (padding[0] * i) < len(row[0]):
                name = row[0][padding[0] * i : padding[0] * (i+1)]
                line += name + " " * (padding[0]-len(name)) + " | "
            
            if i==0 and padding[1] >= len(row[1]):
                line += row[1] + " " * (padding[1] - len(row[1])) + " | "
            else: # elif (padding[1] * i) < len(row[1]):
                effect = row[1][padding[1] * i : padding[1] * (i+1)]
                line += effect + " " * (padding[1] - len(effect)) + " | "
            if i==0:
                line += row[2] + " " * (padding[2] - len(row[2])) + " | "
                line += row[3] + " " * (padding[3] - len(row[3])) + " |"
            else:
                line += " " * padding[2] + " | " + " " * padding[3]  + " |"
            print(line, flush=True)
        print(h_line, flush=True)

    if len(moves)==0:
        print("|        No Results!        |")
        print(h_line, flush=True)


def arron_feature1():
    """
    Given a pokemon, get a list of pokemon moves (in general) that could be super effective against  it? (pokemon.csv with AllMoves) -- subquery 
    """
    print("Please provide a pokemon to retrieve a list of moves that are super affective against it")
    while (True):
        pokemonName = prompt("Enter Pokemon Name>",completer=PokemonComplete)
        pokemonName = pokemonName.strip()
        if pokemonName.lower() == "exit" or pokemonName.lower() == "quit":
            return
        elif pokemonName.lower() not in (x.lower() for x in all_pokemon):
            if pokemonName != "":
                print("{} is not a legitimate pokemon name!".format(pokemonName))
            else:
                print("Enter a valid Pokemon name!", flush=True)
            continue
        
        # Get type weaknesses of the valid pokemon
        Weaknesses = __getWeaknesses(pokemonName)

        # Weaknesses comes from a static query, so it should be safe
        query = """
                SELECT DISTINCT name, effect, type, pp
                FROM tbl_allmoves
                WHERE category <> 'Status' AND type ILIKE '""" + "\' OR type ILIKE \'".join(Weaknesses) + "'" + \
                "ORDER BY type, name;"

        __printTypes(pokemonName)
        print("Here are a table of moves that can deal more damage than normal against {}".format(pokemonName), flush=True)
        
        # Get the moves that are of those type weaknesses
        connection = DB_conn.getConn()
        with connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
            cursor.execute(query)
            moves = cursor.fetchall()
            __printMoveTable(moves)
            return

def arron_feature2():
    """
    Given a pokemon and an opponent pokemon, get a list of super effective moves the pokemon can learn against the opponent pokemon
    based on the types
    """
    pokemonOne = None
    pokemonTwo = None
    print("Given pokemon one and pokemon two, find moves that pokemon one can learn to use to deal a lot of damage to pokemon two", flush=True)
    while (True):
        if pokemonOne is None:
            pokemonOne = prompt("Enter name of Pokemon One>", completer=PokemonComplete)
            pokemonOne = pokemonOne.strip()
            if pokemonOne.lower() == "exit" or pokemonOne.lower() == "quit":
                return 
            elif pokemonOne.lower() not in (x.lower() for x in all_pokemon):
                if pokemonOne != "":
                    print("{} is not a legitimate pokemon name!".format(pokemonOne))
                else:
                    print("Enter a valid Pokemon name!", flush=True)
                pokemonOne = None
                continue
        elif pokemonTwo is None:
            pokemonTwo = prompt("Enter name of Pokemon Two>", completer=PokemonComplete)
            if pokemonTwo.lower() == "exit" or pokemonTwo.lower() == "quit":
                return
            elif pokemonTwo.lower() not in (x.lower() for x in all_pokemon):
                if pokemonTwo != "":
                    print("{} is not a legitimate pokemon name!".format(pokemonTwo))
                else:
                    print("Enter a valid Pokemon name!", flush=True)
                pokemonTwo = None
                continue
        else:
            # Start query execution
            weaknesses = __getWeaknesses(pokemonTwo)
            # weaknesses should be safe since it comes from a static query
            query = """
                    SELECT DISTINCT name, effect, type, pp
                    FROM tbl_allmoves JOIN (SELECT pokedex_number, move_name
                                            FROM tbl_pokemon JOIN tbl_pokemon_moves ON tbl_pokemon.pokedex_number=tbl_pokemon_moves.pokemon_id
                                            WHERE name ILIKE %(pokemonOne)s) AS move_map ON tbl_allmoves.name=move_map.move_name
                    WHERE category <> 'Status' AND type ILIKE '""" + "\' OR type ILIKE \'".join(weaknesses) + "'" + \
                    "ORDER BY type, name;"
            
            __printTypes(pokemonOne)
            __printTypes(pokemonTwo)
            print("Here are a table of moves that {} can use to deal more damage than normal against {}".format(pokemonOne, pokemonTwo), flush=True)
            
            conn = DB_conn.getConn()
            with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query, {"pokemonOne":pokemonOne})
                moves = cursor.fetchall()
                __printMoveTable(moves)
            return

__functions__ = {
    "GetStrongMoves": arron_feature1,
    "GetOffensiveMoves": arron_feature2
}
