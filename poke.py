#!/usr/bin/env python3

from utils import Pokemon, PokemonType, listenAndResponse, say, calc_defense_effect, listenAndResponse
from pynput import keyboard
import re
import getch

MY_TEAM = [
    Pokemon(name="月亮伊布", types=[PokemonType.DARK], attack_type=PokemonType.DARK, special_attack_types=[PokemonType.DARK]),
    Pokemon(name="耿鬼", types=[PokemonType.GHOST, PokemonType.POISON], attack_type=PokemonType.GHOST, special_attack_types=[PokemonType.POISON]),
    Pokemon(name="火爆猴", types=[PokemonType.FIGHTING], attack_type=PokemonType.FIGHTING, special_attack_types=[PokemonType.FIGHTING]),
]


def on_press(key):
    if key == keyboard.Key.esc:
        print('bye bye')
        return False # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'q':
        print('bye bye')
        return False # stop listener
    if re.match(r"[a-z]", k):
        key_in = True
        listenAndResponse(MY_TEAM)
    return True

#calc_defense_effect(MY_TEAM[1], [PokemonType.FIGHTING])
key = None
while True:
    print("Welcome to Pokemon assistant, type any character to start recording, q to quit!")
    key = getch.getch()
    if key == 'q':
        break
    listenAndResponse(MY_TEAM)

# listener = keyboard.Listener(on_press=on_press)
# listener.start()
# listener.join()
