#!/usr/bin/env python3

from utils import Pokemon, PokemonType, listenAndResponse
import re
import getch

MY_TEAM = [
    Pokemon(name="月亮伊布", types=[PokemonType.DARK], attack_type=PokemonType.DARK, special_attack_types=[PokemonType.DARK]),
    Pokemon(name="耿鬼", types=[PokemonType.GHOST, PokemonType.POISON], attack_type=PokemonType.GHOST, special_attack_types=[PokemonType.POISON]),
    Pokemon(name="火爆猴", types=[PokemonType.FIGHTING], attack_type=PokemonType.FIGHTING, special_attack_types=[PokemonType.FIGHTING]),
]

TYPE_TEAM = [
    Pokemon(name=t.value, types=[t], attack_type=t, special_attack_types=[t])
    for t in PokemonType
]

key = None
while True:
    print("Welcome to Pokemon assistant, type any character to start recording, t to recommend a type, q to quit!")
    key = getch.getch()
    if key == 'q':
        break
    team = TYPE_TEAM if key == 't' else MY_TEAM
    listenAndResponse(team)
