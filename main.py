import numpy as np
import matplotlib.pyplot as plt
from pyit2fls import T1TSK, T1FS, tri_mf, trapezoid_mf, T1FS_plot
import json

#uniwersa
opt_universe = np.linspace(0, 10, 100)
bug_universe = np.linspace(0, 10, 100)
story_universe = np.linspace(0, 10, 100)
len_universe = np.linspace(5, 150, 100)
price_universe = np.linspace(0, 300, 100)
quality_universe = np.linspace(0, 10, 100)

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

len_short  = T1FS(len_universe, trapezoid_mf, [-1, 0, 10, 20, 1.0])
len_mid    = T1FS(len_universe, tri_mf, [15, 30, 50, 1.0])
len_long   = T1FS(len_universe, tri_mf, [40, 65, 90, 1.0])
len_vlong  = T1FS(len_universe, trapezoid_mf, [80, 110, 150, 150.1, 1.0])

pri_cheap  = T1FS(price_universe, trapezoid_mf, [-0.1, 0, 50, 100, 1.0])
pri_mid    = T1FS(price_universe, tri_mf, [80, 150, 250, 1.0])
pri_expensive = T1FS(price_universe, trapezoid_mf, [200, 300, 400, 400.1, 1.0])

qual_tragic = T1FS(quality_universe, trapezoid_mf, [-0.5, 0, 1.5, 3.5, 1.0])
qual_bad    = T1FS(quality_universe, tri_mf,        [2, 3.5, 5, 1.0])
qual_mid    = T1FS(quality_universe, tri_mf,        [4, 5.5, 7, 1.0])
qual_good   = T1FS(quality_universe, tri_mf,        [6, 7.5, 8.5, 1.0])
qual_perf   = T1FS(quality_universe, trapezoid_mf,  [7.5, 9, 10.5, 11, 1.0])

#wykresy przynależności
T1FS_plot(
    opt_tragic, opt_mid, opt_good, opt_perf,
    title="Optymalizacja",
    legends=["tragic", "mid", "good", "perf"],
    xlabel="Wartość", ylabel="Przynależność"
)

# Bugi
T1FS_plot(
    bug_none, bug_few, bug_med, bug_many,
    title="Bugi",
    legends=["none", "few", "med", "many"],
    xlabel="Wartość", ylabel="Przynależność"
)

# Fabula
T1FS_plot(
    sto_boring, sto_mid, sto_cool,
    title="Fabula",
    legends=["boring", "mid", "cool"],
    xlabel="Wartość", ylabel="Przynależność"
)

# Dlugosc
T1FS_plot(
    len_short, len_mid, len_long, len_vlong,
    title="Dlugosc",
    legends=["short", "mid", "long", "vlong"],
    xlabel="Wartość", ylabel="Przynależność"
)

# Cena
T1FS_plot(
    pri_cheap, pri_mid, pri_expensive,
    title="Cena",
    legends=["cheap", "mid", "expensive"],
    xlabel="Wartość", ylabel="Przynależność"
)

T1FS_plot(
    qual_tragic, qual_bad, qual_mid, qual_good, qual_perf,
    title="Jakosc Gry",
    legends=["tragic", "bad", "mid", "good", "perf"],
    xlabel="Jakosc", ylabel="Przynależność"
)

#funkcje #FRAGMENT AI# prompt -> Porpaw logikę tych funkcji by miały więcej sensu
def q_tragic(o, b, s, l, p):
    # Kategoria: Tragedia. Bugi mają tu niszczycielską wagę (-0.6).
    # Nawet przy dobrej fabule, duża liczba błędów sprowadzi wynik w okolice 0.
    return 0.1*o - 0.6*b + 0.1*s + 0.5

def q_bad(o, b, s, l, p):
    # Kategoria: Słaba gra. Wciąż silna kara za bugi (-0.4).
    # Bias 1.5 pozwala na uzyskanie niskiej oceny, ale wyższej niż w q_tragic.
    return 0.15*o - 0.4*b + 0.2*s + 1.5

def q_mid(o, b, s, l, p):
    # Kategoria: Średniak. Balans między błędami a treścią.
    # Długość (l) zaczyna mieć marginalny wpływ (0.01).
    return 0.2*o - 0.3*b + 0.3*s + 0.01*l + 3.0

def q_good(o, b, s, l, p):
    # Kategoria: Dobra gra. Wysoki bias (4.0) gwarantuje solidną podstawę oceny.
    # Kara za bugi (-0.2) jest odczuwalna – zabugowana gra nie "udaje" ideału.
    return 0.2*o - 0.2*b + 0.4*s + 0.01*l + 4.0

def q_perf(o, b, s, l, p):
    # Kategoria: Majstersztyk. Największa waga fabuły (0.5).
    # Przy b=0, o=10, s=10 i l=50, funkcja zwraca idealne 10.0.
    # Każdy bug tutaj boli bardziej, bo psuje odbiór "perfekcji" (-0.2).
    return 0.2*o - 0.2*b + 0.5*s + 0.01*l + 2.5

my_tsk = T1TSK()
my_tsk.add_input_variable("Optymalizacja")
my_tsk.add_input_variable("Bugi")
my_tsk.add_input_variable("Fabula")
my_tsk.add_input_variable("Dlugosc")
my_tsk.add_input_variable("Cena")

my_tsk.add_output_variable("Jakosc_Gry")

#reguły
# ------------------ Quality Tragic ---------------------
my_tsk.add_rule(
    [("Optymalizacja", opt_tragic), ("Bugi", bug_many)],
    [("Jakosc_Gry", q_tragic)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_tragic), ("Bugi", bug_med)],
    [("Jakosc_Gry", q_tragic)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Bugi", bug_many)],
    [("Jakosc_Gry", q_tragic)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_tragic), ("Bugi", bug_few), ("Fabula", sto_boring)],
    [("Jakosc_Gry", q_tragic)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_tragic), ("Fabula", sto_boring), ("Dlugosc", len_vlong)],
    [("Jakosc_Gry", q_tragic)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_tragic), ("Fabula", sto_boring), ("Cena", pri_expensive)],
    [("Jakosc_Gry", q_tragic)]
)

# ------------------ Quality Bad ---------------------
my_tsk.add_rule(
    [("Optymalizacja", opt_tragic), ("Bugi", bug_few), ("Fabula", sto_mid)],
    [("Jakosc_Gry", q_bad)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_tragic), ("Bugi", bug_none), ("Fabula", sto_boring)],
    [("Jakosc_Gry", q_bad)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Bugi", bug_med)],
    [("Jakosc_Gry", q_bad)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Bugi", bug_many)],
    [("Jakosc_Gry", q_bad)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Fabula", sto_boring)],
    [("Jakosc_Gry", q_bad)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Fabula", sto_boring)],
    [("Jakosc_Gry", q_bad)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Fabula", sto_mid), ("Bugi", bug_med)],
    [("Jakosc_Gry", q_bad)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Fabula", sto_mid), ("Cena", pri_expensive)],
    [("Jakosc_Gry", q_bad)]
)

# ------------------ Quality Mid ---------------------
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Bugi", bug_few), ("Fabula", sto_mid)],
    [("Jakosc_Gry", q_mid)]
)  # ta już była u Ciebie

my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Bugi", bug_none), ("Fabula", sto_mid)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Bugi", bug_few), ("Fabula", sto_cool)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Bugi", bug_med), ("Fabula", sto_mid)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Bugi", bug_few), ("Fabula", sto_mid)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Bugi", bug_none), ("Fabula", sto_boring)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Fabula", sto_cool), ("Bugi", bug_med)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Fabula", sto_mid), ("Dlugosc", len_mid)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Fabula", sto_mid), ("Cena", pri_mid)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Fabula", sto_boring), ("Dlugosc", len_mid)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Fabula", sto_mid), ("Dlugosc", len_vlong)],
    [("Jakosc_Gry", q_mid)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Fabula", sto_cool), ("Cena", pri_expensive)],
    [("Jakosc_Gry", q_mid)]
)

# ------------------ Quality Good ---------------------
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Bugi", bug_few), ("Fabula", sto_cool)],
    [("Jakosc_Gry", q_good)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Bugi", bug_none), ("Fabula", sto_mid)],
    [("Jakosc_Gry", q_good)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Bugi", bug_none), ("Fabula", sto_cool)],
    [("Jakosc_Gry", q_good)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_perf), ("Bugi", bug_med), ("Fabula", sto_cool)],
    [("Jakosc_Gry", q_good)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_perf), ("Bugi", bug_few), ("Fabula", sto_mid)],
    [("Jakosc_Gry", q_good)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Fabula", sto_cool), ("Dlugosc", len_mid)],
    [("Jakosc_Gry", q_good)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Fabula", sto_mid), ("Dlugosc", len_short)],
    [("Jakosc_Gry", q_good)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Fabula", sto_mid), ("Cena", pri_cheap)],
    [("Jakosc_Gry", q_good)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_mid), ("Fabula", sto_cool), ("Cena", pri_cheap)],
    [("Jakosc_Gry", q_good)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_perf), ("Fabula", sto_mid), ("Cena", pri_mid)],
    [("Jakosc_Gry", q_good)]
)

# ------------------ Quality Perfect ---------------------
my_tsk.add_rule(
    [("Optymalizacja", opt_perf), ("Bugi", bug_none), ("Fabula", sto_cool)],
    [("Jakosc_Gry", q_perf)]
)  #
my_tsk.add_rule(
    [("Optymalizacja", opt_perf), ("Bugi", bug_few), ("Fabula", sto_cool)],
    [("Jakosc_Gry", q_perf)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Bugi", bug_none), ("Fabula", sto_cool)],
    [("Jakosc_Gry", q_perf)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_perf), ("Bugi", bug_none), ("Fabula", sto_mid), ("Dlugosc", len_mid)],
    [("Jakosc_Gry", q_perf)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_perf), ("Bugi", bug_none), ("Fabula", sto_cool), ("Dlugosc", len_mid)],
    [("Jakosc_Gry", q_perf)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_perf), ("Bugi", bug_none), ("Fabula", sto_cool), ("Cena", pri_cheap)],
    [("Jakosc_Gry", q_perf)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Bugi", bug_none), ("Fabula", sto_cool), ("Cena", pri_cheap)],
    [("Jakosc_Gry", q_perf)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_good), ("Bugi", bug_none), ("Fabula", sto_cool), ("Dlugosc", len_mid)],
    [("Jakosc_Gry", q_perf)]
)
my_tsk.add_rule(
    [("Optymalizacja", opt_perf), ("Bugi", bug_none), ("Fabula", sto_cool),
     ("Dlugosc", len_long), ("Cena", pri_mid)],
    [("Jakosc_Gry", q_perf)]
)

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

        evaluation_result = my_tsk.evaluate(inputs, tup)
        raw_score = evaluation_result["Jakosc_Gry"]
        score = np.clip(raw_score, 0, 10)
        results.append((game["name"], score))

    # fragment AI; prompt -> Do wykresu "Jakosc Gry" dodaj wynik gry.
    plt.figure(figsize=(12, 8))

    mfs = [qual_tragic, qual_bad, qual_mid, qual_good, qual_perf]
    labels = ["tragic", "bad", "mid", "good", "perf"]

    for mf, label in zip(mfs, labels):
        y_values = [mf(x) for x in quality_universe]
        plt.plot(quality_universe, y_values, label=label, alpha=0.7, linewidth=2)

    colors = ["black", "red", "green", "blue", "magenta", "cyan", "yellow", "orange", "brown"]
    for i, (name, score) in enumerate(results):
        plt.axvline(x=float(score),
                    color=colors[i % len(colors)],
                    linestyle="--",
                    linewidth=2.5,
                    label=f"{name}")

    plt.title("Wyniki")
    plt.xlabel("Jakość gry")
    plt.ylabel("Stopień przynależności")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, which='both', linestyle=':', alpha=0.5)
    plt.ylim(-0.05, 1.05)
    plt.xlim(0, 10)

    plt.tight_layout()
    plt.show()

    print("\n=== WYNIKI ===")
    for name, score in results:
        print(f"{name}: {score:.4f}")
