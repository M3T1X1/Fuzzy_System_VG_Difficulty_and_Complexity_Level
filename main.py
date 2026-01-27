import numpy as np
<<<<<<< HEAD
import matplotlib.pyplot as plt
from pyit2fls import T1TSK, T1FS, tri_mf, trapezoid_mf

# Uniwersa
pegi_domain = np.linspace(0, 18, 200)
mech_domain = np.linspace(0, 20, 200)

# Wejście 1: PEGI
pegi_low  = T1FS(pegi_domain, trapezoid_mf, [-1, 0, 7, 10, 1.0])  # Dla dzieci (3-7)
pegi_med  = T1FS(pegi_domain, tri_mf, [7, 12, 16, 1.0])           # Nastolatki (12-16)
pegi_high = T1FS(pegi_domain, tri_mf, [14, 16, 18, 1.0]) # Dorośli (18+)

# Wejście 2: Ilość Mechanik
mech_few  = T1FS(mech_domain, trapezoid_mf, [-1, 0, 3, 5, 1.0])   # Prosta gra
mech_avg  = T1FS(mech_domain, tri_mf, [3, 6, 9, 1.0])             # Standardowa
mech_many = T1FS(mech_domain, trapezoid_mf, [7, 10, 15, 16, 1.0]) # Złożona

plt.figure(figsize=(12, 5))

#Generowanie wykresu zostało zrobione wraz z pomocą chatbotów

# Wykres PEGI
plt.subplot(1, 2, 1)
plt.plot(pegi_domain, trapezoid_mf(pegi_domain, [-1, 0, 7, 10, 1.0]), label='Niskie (3-7)')
plt.plot(pegi_domain, tri_mf(pegi_domain, [7, 12, 16, 1.0]), label='Średnie (12-16)')
plt.plot(pegi_domain, trapezoid_mf(pegi_domain, [14, 18, 20, 21, 1.0]), label='Wysokie (18+)')
plt.title("Zmienna wejściowa: PEGI")
plt.xlabel("Kategoria wiekowa")
plt.legend()
plt.grid(True, alpha=0.3)

# Wykres Mechanik
plt.subplot(1, 2, 2)
plt.plot(mech_domain, trapezoid_mf(mech_domain, [-1, 0, 3, 5, 1.0]), label='Mało')
plt.plot(mech_domain, tri_mf(mech_domain, [3, 6, 9, 1.0]), label='Średnio')
plt.plot(mech_domain, trapezoid_mf(mech_domain, [7, 10, 15, 16, 1.0]), label='Dużo')
plt.title("Zmienna wejściowa: Ilość Mechanik")
plt.xlabel("Liczba mechanik")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

#Logika funkcji została zrobiona wraz z pomocą chatbotów

# Dla Trudności
def diff_easy(p, m):   return np.clip(0.5 + 0.4*p + 0.1*m, 0, 10)
def diff_medium(p, m): return np.clip(2.0 + 0.5*p + 0.2*m, 0, 10)
def diff_hard(p, m):   return np.clip(4.0 + 0.6*p + 0.3*m, 0, 10)

# Dla Skomplikowania
def comp_low(p, m):    return np.clip(0.2 + 0.01*p + 0.4*m, 0, 10)
def comp_med(p, m):    return np.clip(1.0 + 0.02*p + 0.7*m, 0, 10)
def comp_high(p, m):   return np.clip(2.0 + 0.05*p + 1.1*m, 0, 10)

my_tsk = T1TSK()
my_tsk.add_input_variable("PEGI")
my_tsk.add_input_variable("Mechanics")
my_tsk.add_output_variable("Difficulty")
my_tsk.add_output_variable("Complexity")


my_tsk.add_rule([("PEGI", pegi_low),  ("Mechanics", mech_few)], [("Difficulty", diff_easy), ("Complexity", comp_low)])
my_tsk.add_rule([("PEGI", pegi_med),  ("Mechanics", mech_few)], [("Difficulty", diff_easy), ("Complexity", comp_low)])
my_tsk.add_rule([("PEGI", pegi_high), ("Mechanics", mech_few)], [("Difficulty", diff_easy), ("Complexity", comp_low)]) # Np. Walking simulator

my_tsk.add_rule([("PEGI", pegi_low),  ("Mechanics", mech_avg)], [("Difficulty", diff_medium), ("Complexity", comp_med)])
my_tsk.add_rule([("PEGI", pegi_med),  ("Mechanics", mech_avg)], [("Difficulty", diff_medium), ("Complexity", comp_med)])
my_tsk.add_rule([("PEGI", pegi_high), ("Mechanics", mech_avg)], [("Difficulty", diff_medium), ("Complexity", comp_med)])

my_tsk.add_rule([("PEGI", pegi_low),  ("Mechanics", mech_many)], [("Difficulty", diff_hard), ("Complexity", comp_high)])
my_tsk.add_rule([("PEGI", pegi_med),  ("Mechanics", mech_many)], [("Difficulty", diff_hard), ("Complexity", comp_high)])
my_tsk.add_rule([("PEGI", pegi_high), ("Mechanics", mech_many)], [("Difficulty", diff_hard), ("Complexity", comp_high)]) # Np. Symulator lotu / RPG

# w3
input_pegi =  3.0
input_mech = 8.0

#
"""
geams = [
    g1 ->
    g2 ->
]

"""

results = my_tsk.evaluate(
    {"PEGI": input_pegi, "Mechanics": input_mech}, (input_pegi, input_mech))

print(f"Wejście -> PEGI: {input_pegi}, Ilość Mechanik: {input_mech}")
print(f"Ocena Trudności: {round(results['Difficulty'], 2)}")
print(f"Ocena Skomplikowania: {round(results['Complexity'], 2)}")
=======
from pyit2fls import T1TSK, T1FS, tri_mf, trapezoid_mf
import matplotlib.pyplot as plt

# Uniwersum
mechanics_universe = np.linspace(0.0, 10.0, 1000)
length_universe = np.linspace(0.0, 10.0, 1000)

# Zbiory rozmyte dla skomplikowania mechanik
simple_mechanics = T1FS(mechanics_universe, trapezoid_mf, [-1, 0, 3, 5, 1.0])
simple_mechanics.plot('simple mechanics')
medium_mechanics = T1FS(mechanics_universe, tri_mf, [3, 5, 7, 1.0])
medium_mechanics.plot('medium mechanics')
complex_mechanics = T1FS(mechanics_universe, trapezoid_mf, [6, 7, 10, 11, 1.0])
complex_mechanics.plot('complex mechanics')

# Zbiory rozmyte dla długości gry
short_game = T1FS(length_universe, trapezoid_mf, [-1, 0, 3, 5, 1.0])
short_game.plot('short <5h')
medium_game = T1FS(length_universe, tri_mf, [3, 5, 7, 1.0])
medium_game.plot('medium 20-50h')
long_game = T1FS(length_universe, trapezoid_mf, [6, 7, 10, 11, 1.0])
long_game.plot('long 100h+')

# Funkcje dla trudności gry
def low_difficulty(mech, length):
    return np.clip(0 + 0.4*mech + 0.2*length, 0, 10)

def medium_difficulty(mech, length):
    return np.clip(3 + 0.6*mech + 0.4*length, 0, 10)

def high_difficulty(mech, length):
    return np.clip(6 + 0.8*mech + 0.6*length, 0, 10)

# Funkcje TSK dla TEMPA ROZGRYWKI (0=szybka, 10=wolna)
def fast_pace(mech, length):
    return np.clip(0 + 0.7*mech + 0.1*length, 0, 10)  # Short + simple = fast

def medium_pace(mech, length):
    return np.clip(3 + 0.4*mech + 0.5*length, 0, 10)

def slow_pace(mech, length):
    return np.clip(6 + 0.2*mech + 0.8*length, 0, 10)  # Long + complex = slow

# Sterowniki TSK
controller_difficulty = T1TSK()
controller_pace = T1TSK()

# Zmienne wejściowe
for ctrl in [controller_difficulty, controller_pace]:
    ctrl.add_input_variable('mechanics')
    ctrl.add_input_variable('game_length')

controller_difficulty.add_output_variable('game_difficulty')
controller_pace.add_output_variable('game_pace')

# Reguły TRUDNOŚCI GRY
controller_difficulty.add_rule([('mechanics', simple_mechanics), ('game_length', short_game)], [('game_difficulty', low_difficulty)])
controller_difficulty.add_rule([('mechanics', simple_mechanics), ('game_length', medium_game)], [('game_difficulty', low_difficulty)])
controller_difficulty.add_rule([('mechanics', simple_mechanics), ('game_length', long_game)], [('game_difficulty', medium_difficulty)])
controller_difficulty.add_rule([('mechanics', medium_mechanics), ('game_length', short_game)], [('game_difficulty', low_difficulty)])
controller_difficulty.add_rule([('mechanics', medium_mechanics), ('game_length', medium_game)], [('game_difficulty', medium_difficulty)])
controller_difficulty.add_rule([('mechanics', medium_mechanics), ('game_length', long_game)], [('game_difficulty', medium_difficulty)])
controller_difficulty.add_rule([('mechanics', complex_mechanics), ('game_length', short_game)], [('game_difficulty', medium_difficulty)])
controller_difficulty.add_rule([('mechanics', complex_mechanics), ('game_length', medium_game)], [('game_difficulty', high_difficulty)])
controller_difficulty.add_rule([('mechanics', complex_mechanics), ('game_length', long_game)], [('game_difficulty', high_difficulty)])

# Reguły TEMPA ROZGRYWKI
controller_pace.add_rule([('mechanics', simple_mechanics), ('game_length', short_game)], [('game_pace', fast_pace)])
controller_pace.add_rule([('mechanics', simple_mechanics), ('game_length', medium_game)], [('game_pace', fast_pace)])
controller_pace.add_rule([('mechanics', simple_mechanics), ('game_length', long_game)], [('game_pace', medium_pace)])
controller_pace.add_rule([('mechanics', medium_mechanics), ('game_length', short_game)], [('game_pace', fast_pace)])
controller_pace.add_rule([('mechanics', medium_mechanics), ('game_length', medium_game)], [('game_pace', medium_pace)])
controller_pace.add_rule([('mechanics', medium_mechanics), ('game_length', long_game)], [('game_pace', medium_pace)])
controller_pace.add_rule([('mechanics', complex_mechanics), ('game_length', short_game)], [('game_pace', medium_pace)])
controller_pace.add_rule([('mechanics', complex_mechanics), ('game_length', medium_game)], [('game_pace', medium_pace)])
controller_pace.add_rule([('mechanics', complex_mechanics), ('game_length', long_game)], [('game_pace', slow_pace)])

game_name = 'Hollow Knight'
mech_input = 7.0   # Wysokie mechaniki (platformer souls-like)
length_input = 3.0 # Średnia długość (~30h main+extras)

diff_out = controller_difficulty.evaluate({"mechanics": mech_input, "game_length": length_input}, (mech_input, length_input))
pace_out = controller_pace.evaluate({"mechanics": mech_input, "game_length": length_input}, (mech_input, length_input))

print(f"{game_name} (mechanics={mech_input}, length={length_input}):")
print("Trudność gry:", round(diff_out['game_difficulty'], 2))
print("Tempo rozgrywki:", round(pace_out['game_pace'], 2))
plt.show()
>>>>>>> 172364f (feat: changed project logic, moved input values to json file)
