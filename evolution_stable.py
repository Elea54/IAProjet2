import tkinter as tk
from tkinter import messagebox
import numpy as np
import subprocess
import sys
import matplotlib.pyplot as plt

# Installe automatiquement matplotlib
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Matplotlib not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
    print("Matplotlib installed successfully!")


def hawk_dove_game(V, C, population_size=100, generations=50):
    """
    Simule le jeu Aigle-Colombe pour explorer les stratégies évolutives stables.

    Parameters:
        V (float): Valeur de la ressource.
        C (float): Coût du combat.
        population_size (int): Taille totale de la population.
        generations (int): Nombre de générations à simuler.

    Returns:
        history (list): Fraction des Aigles dans la population au fil du temps.
        payoff_matrix (ndarray): La matrice de payoff moyenne après toutes les interactions.
    """
    # Initialiser la population avec des fractions aléatoires d'Aigles (1) et de Colombes (0)
    population = np.random.choice([0, 1], size=population_size)  # 0 = Colombe, 1 = Aigle
    history = [np.mean(population)]  # Suivre la fraction des Aigles

    # Créer une matrice vide pour les payoffs
    payoff_matrix = np.zeros((2, 2))  # [Aigle vs Colombe, Aigle vs Aigle, etc.]

    for _ in range(generations):
        # Réinitialiser la matrice des payoffs pour cette génération
        current_payoffs = np.zeros((2, 2))

        # Simuler le jeu entre toutes les paires d'individus
        for i in range(population_size):
            for j in range(i + 1, population_size):  # Éviter les paires répétées
                if population[i] == 1 and population[j] == 1:  # Aigle vs Aigle
                    payoff = (V / 2) - (C / 2)
                    current_payoffs[1, 1] += payoff
                elif population[i] == 1 and population[j] == 0:  # Aigle vs Colombe
                    current_payoffs[1, 0] += V
                elif population[i] == 0 and population[j] == 1:  # Colombe vs Aigle
                    current_payoffs[0, 1] += V
                elif population[i] == 0 and population[j] == 0:  # Colombe vs Colombe
                    payoff = V / 2
                    current_payoffs[0, 0] += payoff

        # Normaliser la matrice des payoffs
        total_interactions = population_size * (population_size - 1) / 2
        payoff_matrix = current_payoffs / total_interactions

        # Calculer la fraction des Aigles
        hawk_fraction = np.mean(population)
        history.append(hawk_fraction)

        # Mettre à jour la population basée sur les payoffs moyens
        fitness = np.zeros(population_size)
        for i in range(population_size):
            if population[i] == 1:  # Aigle
                fitness[i] = hawk_fraction * payoff_matrix[1, 1] + (1 - hawk_fraction) * payoff_matrix[1, 0]
            else:  # Colombe
                fitness[i] = hawk_fraction * payoff_matrix[0, 1] + (1 - hawk_fraction) * payoff_matrix[0, 0]

        # Mise à jour de la population en fonction de la fitness
        fitness /= np.sum(fitness)  # Normaliser les fitness pour les probabilités
        population = np.random.choice([0, 1], size=population_size, p=[1 - hawk_fraction, hawk_fraction])

    return history, payoff_matrix



def plot_hawk_dove(history):
    """
    Trace les résultats de la simulation du jeu Aigle-Colombe.

    Parameters:
        history (list): Fraction des Aigles dans la population au fil du temps.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(history, label="Fraction des Aigles")
    plt.axhline(0.5, color='r', linestyle='--', label="Seuil ESS")
    plt.xlabel("Générations")
    plt.ylabel("Fraction des Aigles")
    plt.title("Jeu Aigle-Colombe : Évolution des stratégies")
    plt.legend()
    plt.show()


def display_payoff_matrix(payoff_matrix):
    """
    Affiche la matrice de payoff.

    Parameters:
        payoff_matrix (ndarray): La matrice de payoff.
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.matshow(payoff_matrix, cmap="Blues")

    for i in range(2):
        for j in range(2):
            # Définir la couleur du texte en fonction de la valeur du payoff
            value = payoff_matrix[i, j]
            text_color = "black" if value < 1 else "white"  # Si la valeur est faible, le texte sera noir
            
            # Afficher la valeur avec la couleur appropriée
            ax.text(j, i, f"{value:.2f}", ha='center', va='center', color=text_color)
    
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Colombe', 'Aigle'])
    ax.set_yticklabels(['Colombe', 'Aigle'])

    ax.set_xlabel('Joueur 2')
    ax.set_ylabel('Joueur 1')
    ax.set_title('Matrice des payoffs')

    plt.show()



def run_simulation():
    """
    Exécute la simulation du jeu Aigle-Colombe avec les paramètres de l'IHM.
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

        # Exécution de la simulation
        history, payoff_matrix = hawk_dove_game(V, C, population_size, generations)

        # Affichage des résultats
        plot_hawk_dove(history)

        # Affichage de la matrice de payoffs
        display_payoff_matrix(payoff_matrix)

    except ValueError as e:
        messagebox.showerror("Erreur", f"Entrée invalide : {e}")


# Création de l'IHM
root = tk.Tk()
root.title("Simulation du jeu Aigle-Colombe")

# Labels et champs de saisie
tk.Label(root, text="Valeur de la ressource (V)").grid(row=0, column=0, padx=10, pady=5)
entry_value = tk.Entry(root)
entry_value.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Coût du combat (C)").grid(row=1, column=0, padx=10, pady=5)
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

# Boucle principale
root.mainloop()
