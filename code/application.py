from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
import features
import playsound

from load_data import findFile

main_menu_completer = WordCompleter(features.__functions__.keys(), ignore_case=True)

def call_feature(feature: str):
    if feature not in features.__functions__:
        print("Not a feature!")
    else:
        features.__functions__[feature]()

def main():
    playsound.playsound(findFile("../themeSong.mp3")[1], False)
    call_feature("logo")
    while 1:
        option = prompt('Awesome pokemon DB>', completer=main_menu_completer)
        call_feature(option)


if __name__ == "__main__":
    main()