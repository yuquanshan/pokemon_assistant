import os
import time
import pyaudio
import wave
import speech_recognition as sr
import pinyin
import re
import csv
from dataclasses import dataclass
from functools import reduce
from enum import Enum
import pyttsx3

RECOGNIZER = sr.Recognizer()
SPEAKER = pyttsx3.init()
RIVAL_TYPE_NOT_FOUND = "未找到对手属性"

class PokemonType(Enum):
    NORMAL = "一般"
    FIGHTING = "格斗"
    FLYING = "飞行"
    POISON = "毒"
    GROUND = "地面"
    ROCK = "岩石"
    BUG = "虫"
    GHOST = "幽灵"
    STEEL = "钢"
    FIRE = "火"
    WATER = "水"
    GRASS = "草"
    ELECTRIC = "电"
    PSYCHIC = "超能力"
    ICE = "冰"
    DRAGON = "龙"
    DARK = "恶"
    FAIRY = "妖精"

@dataclass
class Pokemon:
    name: str
    types: [PokemonType]
    attack_type: PokemonType
    special_attack_types: [PokemonType]

def load_attack_effect_table(fn: str):
    res = {}
    with open(fn, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tp = PokemonType[row['Attacking'].upper()]
            res[tp] = {}
            for t, e in row.items():
                if t != 'Attacking':
                    res[tp][PokemonType[t.upper()]] = float(e)
    return res


ATTACK_EFFECTS_FILE = 'chart.csv'
ATTACK_EFFECTS = load_attack_effect_table('chart.csv')


def say(txt: str):
    SPEAKER.say(txt)
    SPEAKER.runAndWait()
    #print("done speaking")

def listenAndResponse(my_team:[Pokemon]):
    print('\a')

    try:
        with sr.Microphone() as source:
            print("Say something!")
            audio = RECOGNIZER.listen(source, phrase_time_limit=1.5)
        res = RECOGNIZER.recognize_google(audio, language='zh-CN', show_all=True)
        print(res)
        alters = [i['transcript'] for i in res['alternative']]
        rival_types = build_rivalry_types(alters)
        if len(rival_types) == 0:
            print(RIVAL_TYPE_NOT_FOUND)
            say(RIVAL_TYPE_NOT_FOUND)
            return
        ranked = rank_team_members(my_team, rival_types)
        adv = list(filter(lambda a: a[0] >= 1, ranked))
        disadv = list(filter(lambda a: a[0] < 1, ranked))
        print(f"????? {adv}   {disadv}")
        if len(adv) > 0:
            say("优势")
            for p in adv:
                say(p[1].name)
        if len(adv) > 0:
            say("劣势")
            for p in disadv:
                say(p[1].name)
    except Exception as e:
        return
    return


def build_rivalry_types(alters: [str]) -> [PokemonType]:
    v = {
        PokemonType.NORMAL: ["yiban"],
        PokemonType.FIGHTING: ["gedou"],
        PokemonType.FLYING: ["feixing"],
        PokemonType.POISON: ["du", "duxi"],
        PokemonType.GROUND: ["dimian"],
        PokemonType.ROCK: ["yanshi"],
        PokemonType.BUG: ["chong"],
        PokemonType.GHOST: ["youling"],
        PokemonType.STEEL: ["gang", "tie"],
        PokemonType.FIRE: ["huo"],
        PokemonType.WATER: ["shui"],
        PokemonType.GRASS: ["caoxi", "zhiwu"],
        PokemonType.ELECTRIC: ["dianxi", "shandian", "leidian"],
        PokemonType.PSYCHIC: ["chaonengli"],
        PokemonType.ICE: ["bingxi"],
        PokemonType.DRAGON: ["longxi"],
        PokemonType.DARK: ["exi", "emo", "heian", "anhei"],
        PokemonType.FAIRY: ["yaojing"],
    }
    rival_types = []
    for alter in alters:
        p = pinyin.get(alter, format="strip")
        for pt, l in v.items():
            for i in l:
                if i in p:
                    rival_types.append(pt)
                    print(alter + " matches " + str(pt))
    return list(set(rival_types))


def rank_team_members(my_team: [Pokemon], rival_types: [PokemonType]) -> [(int, Pokemon)]:
    scores = [(calc_advantage(pokemon, rival_types), pokemon) for pokemon in my_team]
    res = sorted(scores, key=lambda p : p[0], reverse=True)
    print(f"Sorted pokemon order: {[(r[1].name, r[0]) for r in res]}")
    return res

# calculate battle advantage by , assuming the attack speed are the same with your rival
def calc_advantage(pokemon: Pokemon, rival_types: [PokemonType]) -> int:
    return calc_attack_effect(pokemon, rival_types) / calc_defense_effect(pokemon, rival_types)

def calc_attack_effect(pokemon: Pokemon, rival_types: [PokemonType]) -> int:
    res = 1.0
    for r in rival_types:
        res = res * ATTACK_EFFECTS[pokemon.attack_type][r]
    print(f"attach effect: {res}")
    return res


def calc_defense_effect(pokemon: Pokemon, rival_types: [PokemonType]) -> int:
    # for double type rival, assuming its attack type is equally probable
    print(f"{pokemon} {rival_types}")
    fct = 1 / len(rival_types)
    res = 0.0
    for r in rival_types:
        eff = 1.0
        for t in pokemon.types:
            eff = eff * max(0.001, ATTACK_EFFECTS[r][t]) # avoid dividing by 0
        res = res + fct * eff
    print(f"defense effect: {res}")
    return res


# deprecated
def play(fname: str) -> None:
    chunk = 1024
    f = wave.open(fname, "rb")

    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    #stop stream
    stream.stop_stream()
    stream.close()

    #close PyAudio
    p.terminate()
    return

def pokeLookupAndSay(alters: [str]) -> None:
    v = {
        "一般": ["yiban"],
        "格斗": ["gedou"],
        "飞行": ["feixing"],
        "毒": ["du", "duxi"],
        "地面": ["dimian"],
        "岩石": ["yanshi"],
        "虫": ["chong"],
        "幽灵": ["youling"],
        "钢": ["gang"],
        "火": ["huo"],
        "水": ["shui"],
        "草": ["caoxi", "zhiwu"],
        "电": ["dianxi", "shandian", "leidian"],
        "超能力": ["chaonengli"],
        "冰": ["bingxi"],
        "龙": ["longxi"],
        "恶": ["exi", "emo"],
        "妖精": ["yaojing"],
    }
    d = {
        "gengui.wav": v["草"] + v["妖精"] + v["超能力"] + v["格斗"] + v["虫"] + v["一般"],
        "yibu.wav": v["幽灵"] + v["超能力"],
        "whatever.wav": [],
        "monkey.wav": v["一般"] + v["岩石"] + v["钢"] + v["冰"] + v["恶"] + v["虫"],
    }

    filenames = []
    for alter in alters:
        p = pinyin.get(alter, format="strip")
        for fn, l in d.items():
            for i in l:
                if i in p:
                    filenames.append(fn)
                    print(alter + " matches " + fn)
    filenames = list(set(filenames))
    for fn in filenames:
        play(fn)
    if len(filenames) == 0:
        play("whatever.wav")
    return
