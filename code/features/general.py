import pyfiglet

def logo():
    logo = pyfiglet.figlet_format("PokeDB")
    print(logo)
    print("S20 Database System final project. Type \"help\" to see a list of features. \n")

def help():
    print("-------------HELP------------\n")
    print("StatAnalyzer: Given pokemon type(s) and stat categories, list pokemons with highest combined stats \n \
            \n \
                first_input: <pokemon_type1> [pokemon_type2] \n \
                second_input: <stat1> <stat2> ... <stat6> \n")
    print("SuperEffective: Given a move, list all of the Pokemon that take super effective damage from this move, along with their modifier\n \
            \n \
                first_input: <move_name> \n")
    print("NotEffective: Given a move, list all of the Pokemon that take resist this move, along with their modifier\n \
            \n \
                first_input: <move_name> \n")
    print("GetPokemonFromMove: Given a move, list all of the Pokemons that can learn it.\n \
            \n \
                first_input: <move_name> \n")

def quit_program():
    print("Goodbye!")
    exit()

__functions__ = {
    "help": help,
    "logo": logo,
    "quit": quit_program,
    "exit": quit_program
}