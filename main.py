import numpy as np
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