import numpy as np
import matplotlib.pyplot as plt
from pyit2fls import T1TSK, T1FS, tri_mf, trapezoid_mf
import json

#uniwersa
opt_universe = np.linspace(0, 10, 100)
bug_universe = np.linspace(0, 10, 100)
story_universe = np.linspace(0, 10, 100)
len_universe = np.linspace(5, 50, 100)
price_universe = np.linspace(0, 300, 100)

#zbiory rozmyte
opt_tragic = T1FS(opt_universe, trapezoid_mf, [-0.1, 0, 2, 4, 1.0])
opt_mid    = T1FS(opt_universe, tri_mf, [3, 5, 7, 1.0])
opt_good   = T1FS(opt_universe, tri_mf, [6, 8, 9, 1.0])
opt_perf   = T1FS(opt_universe, trapezoid_mf, [8, 9, 10, 10.1, 1.0])

bug_none   = T1FS(bug_universe, trapezoid_mf, [-0.1, 0, 1, 2, 1.0])
bug_few    = T1FS(bug_universe, tri_mf, [1, 3, 5, 1.0])
bug_med    = T1FS(bug_universe, tri_mf, [4, 6, 8, 1.0])
bug_many   = T1FS(bug_universe, trapezoid_mf, [7, 9, 10, 10.1, 1.0])

sto_boring = T1FS(story_universe, trapezoid_mf, [-0.1, 0, 3, 5, 1.0])
sto_mid    = T1FS(story_universe, tri_mf, [4, 6, 8, 1.0])
sto_cool   = T1FS(story_universe, trapezoid_mf, [7, 9, 10, 10.1, 1.0])

len_short  = T1FS(len_universe, trapezoid_mf, [-0.1, 0, 5, 10, 1.0])
len_mid    = T1FS(len_universe, tri_mf, [8, 15, 25, 1.0])
len_long   = T1FS(len_universe, tri_mf, [20, 40, 60, 1.0])
len_vlong  = T1FS(len_universe, trapezoid_mf, [50, 70, 100, 100.1, 1.0])

pri_cheap  = T1FS(price_universe, trapezoid_mf, [-0.1, 0, 50, 100, 1.0])
pri_mid    = T1FS(price_universe, tri_mf, [80, 150, 250, 1.0])
pri_expensive = T1FS(price_universe, trapezoid_mf, [200, 300, 400, 400.1, 1.0])

#Todo: ulepszyć funkcje
#funkcje #FRAGMENT AI#
def q_tragic(o, b, s, l, p): return np.clip(0.1*o - 0.5*b + 0.1*s, 0, 2)
def q_bad(o, b, s, l, p):    return np.clip(0.2*o - 0.3*b + 0.2*s, 2, 4)
def q_mid(o, b, s, l, p):    return np.clip(0.4*o - 0.2*b + 0.4*s + 0.05*l, 4, 6)
def q_good(o, b, s, l, p):   return np.clip(0.5*o - 0.1*b + 0.6*s + 0.05*l, 6, 8)
def q_perf(o, b, s, l, p):   return np.clip(0.6*o - 0.0*b + 0.8*s + 0.1*l, 8, 10)


my_tsk = T1TSK()
my_tsk.add_input_variable("Optymalizacja")
my_tsk.add_input_variable("Bugi")
my_tsk.add_input_variable("Fabula")
my_tsk.add_input_variable("Dlugosc")
my_tsk.add_input_variable("Cena")

my_tsk.add_output_variable("Jakosc_Gry")

#Todo: dodać więcej reguł
#reguły
my_tsk.add_rule([("Optymalizacja", opt_tragic), ("Bugi", bug_many)], [("Jakosc_Gry", q_tragic)])

my_tsk.add_rule([("Optymalizacja", opt_mid), ("Bugi", bug_few), ("Fabula", sto_mid)], [("Jakosc_Gry", q_mid)])

my_tsk.add_rule([("Optymalizacja", opt_perf), ("Bugi", bug_none), ("Fabula", sto_cool)], [("Jakosc_Gry", q_perf)])

#Todo: dodać wykresy przynależności

with open("games.json", "r", encoding="utf-8") as f:
    games = json.load(f)
    results = []

    for game in games:
        inputs = {
            "Optymalizacja": game["Optymalizacja"],
            "Bugi": game["Bugi"],
            "Fabula": game["Fabula"],
            "Dlugosc": game["Dlugosc"],
            "Cena": game["Cena"],
        }
        tup = (
            game["Optymalizacja"],
            game["Bugi"],
            game["Fabula"],
            game["Dlugosc"],
            game["Cena"],
        )

        score = my_tsk.evaluate(inputs, tup)
        results.append((game["name"], score))

    for name, score in results:
        print(name, score)
