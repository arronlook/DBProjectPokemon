from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from namespaces import all_pokemon
def victor_feature1():
    pokemon_completer = WordCompleter(all_pokemon, ignore_case=True)
    option = prompt('Print a pokemon\'s name>', completer=pokemon_completer)
    print(option)

def victor_feature2():
    print("Victor feature 2")

__functions__ = {
    "victor_feature1": victor_feature1,
    "victor_feature2": victor_feature2
}