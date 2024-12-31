import tkinter as tk
from tkinter import messagebox
import numpy as np
import subprocess
import sys

# Ensure matplotlib is installed
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Matplotlib not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
    print("Matplotlib installed successfully!")



def hawk_dove_game(V, C, population_size=100, generations=50):
    """
    Simulates the Hawk-Dove Game to explore stable evolutionary strategies.

    Parameters:
        V (float): Value of the resource.
        C (float): Cost of fighting.
        population_size (int): Total size of the population.
        generations (int): Number of generations to simulate.

    Returns:
        history (list): Fraction of Hawks in the population over time.
    """
    # Initialize population with random fractions of Hawks (1) and Doves (0)
    hawk_fraction = np.random.rand()
    history = [hawk_fraction]

    for _ in range(generations):
        # Compute payoffs
        hawk_hawk_payoff = (V - C) / 2 if C > V else 0
        hawk_dove_payoff = V
        dove_hawk_payoff = 0
        dove_dove_payoff = V / 2

        # Average payoffs for Hawks and Doves
        hawk_payoff = hawk_fraction * hawk_hawk_payoff + (1 - hawk_fraction) * hawk_dove_payoff
        dove_payoff = hawk_fraction * dove_hawk_payoff + (1 - hawk_fraction) * dove_dove_payoff

        # Fitness is proportional to payoffs
        total_fitness = hawk_fraction * hawk_payoff + (1 - hawk_fraction) * dove_payoff
        hawk_fraction = (hawk_fraction * hawk_payoff) / total_fitness
        
        # Record the fraction of Hawks in the population
        history.append(hawk_fraction)

    return history


def plot_hawk_dove(history):
    """
    Plots the results of the Hawk-Dove game simulation.

    Parameters:
        history (list): Fraction of Hawks in the population over time.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(history, label="Fraction of Hawks")
    plt.axhline(0.5, color='r', linestyle='--', label="ESS Threshold")
    plt.xlabel("Generations")
    plt.ylabel("Fraction of Hawks")
    plt.title("Hawk-Dove Game: Evolution of Strategies")
    plt.legend()
    plt.show()


def run_simulation():
    """
    Runs the Hawk-Dove simulation with parameters from the GUI.
    """
    try:
        # Récupération des valeurs saisies
        V = float(entry_value.get())
        C = float(entry_cost.get())
        population_size = int(entry_population.get())
        generations = int(entry_generations.get())

        # Validation des entrées
        if V <= 0 or C <= 0 or population_size <= 0 or generations <= 0:
            raise ValueError("Toutes les valeurs doivent être positives.")

        # Appel de la fonction de simulation
        history = hawk_dove_game(V, C, population_size, generations)

        # Affichage des résultats
        plot_hawk_dove(history)
    except ValueError as e:
        messagebox.showerror("Erreur", f"Entrée invalide : {e}")


# Création de l'IHM
root = tk.Tk()
root.title("Simulation du jeu Hawk-Dove")

# Labels et champs de saisie
tk.Label(root, text="Valeur de la ressource (V)").grid(row=0, column=0, padx=10, pady=5)
entry_value = tk.Entry(root)
entry_value.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Coût de la lutte (C)").grid(row=1, column=0, padx=10, pady=5)
entry_cost = tk.Entry(root)
entry_cost.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Taille de la population").grid(row=2, column=0, padx=10, pady=5)
entry_population = tk.Entry(root)
entry_population.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Nombre de générations").grid(row=3, column=0, padx=10, pady=5)
entry_generations = tk.Entry(root)
entry_generations.grid(row=3, column=1, padx=10, pady=5)

# Bouton pour exécuter la simulation
btn_run = tk.Button(root, text="Exécuter la simulation", command=run_simulation)
btn_run.grid(row=4, column=0, columnspan=2, pady=20)

# Boucle principale de l'IHM
root.mainloop()
