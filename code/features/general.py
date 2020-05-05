import pyfiglet

def logo():
    logo = pyfiglet.figlet_format("PokeDB")
    print(logo)
    print("S20 Database System final project. Type \"help\" to see a list of features. \n")

def help():
    print("-------------HELP------------\n")
    print("FindPokemon: Given part of a pokemon name, return all pokemon names that match it \n \
            \n \
                first_input: <part of a name> \n")
    print("FindMove: Given part of a move name, return all pokemon move names that match it \n \
            \n \
                first_input: <part of a name> \n")
    print("StatAnalyzer: Given pokemon type(s) and stat categories, list pokemons with highest combined stats \n \
            \n \
                first_input: <pokemon_type1> [pokemon_type2] \n \
                second_input: <stat1> <stat2> ... <stat6> \n")
    print("MoveStatAnalyzer: Given a move, find all the pokemon that can learn it ordered by stat. \n \
            \n \
                first_input: <move_name> \n")

    print("SuperEffective: Given a move, list all of the Pokemon that take super effective damage from this move, along with their modifier\n \
            \n \
                first_input: <move_name> \n")
    print("NotEffective: Given a move, list all of the Pokemon that take resist this move, along with their modifier\n \
            \n \
                first_input: <move_name> \n")
    print("GetPokemonFromMove: Given a move, list all of the Pokemons that can learn it.\n \
            \n \
                first_input: <move_name> \n")
    print("GetStrongMoves: Given the name of a pokemon, list all moves that will deal more damage than normal against that pokemon\n \
            \n \
                first_input: <pokemon name>\n")
    print("GetOffensiveMoves: Given two pokemon names, list all the moves that the first pokemon can learn to use to deal more damage than normal against the second pokemon\n \
            \n \
                first_input: <first pokemon name>\n \
                second_input: <second pokemon name> \n")
    print("", flush=True)

def quit_program():
    print("Goodbye!")
    exit()

__functions__ = {
    "help": help,
    "logo": logo,
    "quit": quit_program,
    "exit": quit_program
}