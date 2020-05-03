import pyfiglet

def logo():
    logo = pyfiglet.figlet_format("PokeDB")
    print(logo)
    print("S20 Database System final project\n")

def help():
    print("-------------HELP------------\n")
    print("StatAnalyzer: Given pokemon type(s) and stat categories, list pokemons with highest combined stats \n \
            \n \
                first_input: <pokemon_type1> <pokemon_type2> \n \
                second_input: <stat1> <stat2> \n")
    print("GetStrongMoves: Given the name of a pokemon, list all moves that will deal more damage than normal against that pokemon\n" + \
          "                input: <pokemon name>\n")
    print("GetOffensiveMoves: Given two pokemon names, list all the moves that the first pokemon can learn to use to deal more damage than normal against the second pokemon\n" + \
          "                   first_input: <first pokemon name>\n" + \
          "                   second_input: <second pokemon name>\n")
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