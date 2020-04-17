import pyfiglet

def logo():
    logo = pyfiglet.figlet_format("PokeDB")
    print(logo)
    print("S20 Database System final project\n")

def help():
    print("This is an example help menu!")
    print("-------------HELP------------\n\n\n\n")

def quit_program():
    print("Goodbye!")
    exit()

__functions__ = {
    "help": help,
    "logo": logo,
    "quit": quit_program,
    "exit": quit_program
}