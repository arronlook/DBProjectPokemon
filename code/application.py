from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
import features

# For the surprise
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import threading

from load_data import findFile

main_menu_completer = WordCompleter(features.__functions__.keys(), ignore_case=True)

def call_feature(feature: str):
    if feature not in features.__functions__:
        print("Not a feature!")
    else:
        features.__functions__[feature]()

def main():
    try:
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.load(findFile("../themeSong.mp3")[1])
        pygame.mixer.music.play(-1)
        call_feature("logo")
        print("Turn up the volume if you can't hear it!", flush=True)
    except e:
        call_feature("logo")
        print("Failed to play surprise theme song.", flush=True)

    while 1:
        option = prompt('Awesome pokemon DB>', completer=main_menu_completer)
        call_feature(option)


if __name__ == "__main__":
    main()