from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from database import DB_conn
from namespaces import all_pokemon, all_moves

def __getPokemons(move):
    pokemons = []

    query = """
            SELECT DISTINCT name 
            FROM tbl_pokemon
            WHERE pokedex_number IN
            (
                SELECT DISTINCT pokemon_id
                FROM tbl_pokemon_moves
                WHERE move_name ILIKE %s
            )
            """

    conn = DB_conn.getConn()
    with conn.cursor() as cursor:
        cursor.execute(query, (move,))
        pokemon_names = cursor.fetchall()

        for i in range(len(pokemon_names)):
            pokemons.append(pokemon_names[i][0])
    return pokemons

def __printPokemons(pokemons):
    max = 0
    for i in range(len(pokemons)):
        if max < len(pokemons[i]):
            max = len(pokemons[i])

    seperator = "-" * (max + 2)

    print(seperator, flush=True)
    for i in range(len(pokemons)):
        line = "|" + pokemons[i] + " " * (max - len(pokemons[i])) + "|"
        print(line, flush=True)
        print(seperator, flush=True)

def wendi_feature():
    """
    Given a pokemon move, return a list of pokemons that can learn it.
    """
    print("Please enter a pokemon move to get a list of pokemon that can learn it")
    while(True):
        moves_completer = WordCompleter(all_moves + ["Exit", "Quit"], ignore_case=True)
        move = prompt("Enter A Move>", completer=moves_completer)
        move = move.strip()
        if move.lower() == "exit" or move.lower() == "quit":
            return
        elif move.lower() not in (x.lower() for x in all_moves):
            if move != "":
                print("{} is not a legitimate pokemon move!".format(move))
            else:
                print("Please enter a valid move!", flush = True)
            continue

        print("These pokemons can learn {}:".format(move))

        pokemons = __getPokemons(move)

        __printPokemons(pokemons)

__functions__ = {
    "GetPokemonFromMove": wendi_feature
}