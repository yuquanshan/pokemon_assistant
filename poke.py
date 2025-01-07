#!/usr/bin/env python3

from utils import Pokemon, PokemonType, listenAndResponse
import re
import getch

MY_TEAM = [
    Pokemon(name="月亮伊布", types=[PokemonType.DARK], attack_type=PokemonType.DARK, special_attack_types=[PokemonType.DARK]),
    Pokemon(name="耿鬼", types=[PokemonType.GHOST, PokemonType.POISON], attack_type=PokemonType.GHOST, special_attack_types=[PokemonType.POISON]),
    Pokemon(name="火爆猴", types=[PokemonType.FIGHTING], attack_type=PokemonType.FIGHTING, special_attack_types=[PokemonType.FIGHTING]),
]

key = None
while True:
    print("Welcome to Pokemon assistant, type any character to start recording, q to quit!")
    key = getch.getch()
    if key == 'q':
        break
    listenAndResponse(MY_TEAM)
