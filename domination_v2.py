import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Modèle de dominance sociale
def social_dominance_simulation(
    population_size=50, 
    generations=100, 
    learning_rate=0.1,
    damage_cost=0.2, 
    mortality_risk=0.05
):
    """
    Simule la formation de hiérarchies sociales via des interactions agressives.

    Parameters:
        population_size (int): Nombre d'individus dans la population.
        generations (int): Nombre de générations à simuler.
        learning_rate (float): Taux d'apprentissage des individus.
        damage_cost (float): Coût des dégâts par interaction.
        mortality_risk (float): Probabilité de mortalité due à des blessures cumulées.

    Returns:
        dominance_history (list): Évolution des rangs de dominance.
        costs_history (list): Coûts accumulés par les individus.
        abilities_history (list): Capacités de combat des individus par génération.
    """
    # Initialisation
    fighting_ability = np.random.uniform(0.5, 1.5, population_size)  # Capacités initiales
    costs = np.zeros(population_size)  # Coûts cumulés
    dominance_history = []
    costs_history = []
    abilities_history = []

    for generation in range(generations):
        # Interaction entre paires
        for i in range(population_size):
            opponent = np.random.randint(0, population_size)
            while opponent == i:
                opponent = np.random.randint(0, population_size)

            # Probabilité de victoire
            prob_win = fighting_ability[i] / (fighting_ability[i] + fighting_ability[opponent])

            # Résultat de l'interaction
            if np.random.rand() < prob_win:  # Individu i gagne
                fighting_ability[i] += learning_rate * (1 - prob_win)
                costs[opponent] += damage_cost
            else:  # Opposant gagne
                fighting_ability[opponent] += learning_rate * prob_win
                costs[i] += damage_cost

            # Risque de mortalité
            if costs[i] * mortality_risk > np.random.rand():
                fighting_ability[i] = 0  # Individu exclu (mort)
            if costs[opponent] * mortality_risk > np.random.rand():
                fighting_ability[opponent] = 0  # Opposant exclu (mort)

        # Mise à jour des rangs et historique
        dominance_ranks = np.argsort(fighting_ability)[::-1]
        dominance_history.append(np.copy(dominance_ranks))
        costs_history.append(np.copy(costs))
        abilities_history.append(np.copy(fighting_ability))

    return dominance_history, costs_history, abilities_history

# Fonction de visualisation
def plot_results(dominance_history, costs_history, abilities_history):
    """
    Trace les résultats de la simulation.

    Parameters:
        dominance_history (list): Évolution des rangs de dominance.
        costs_history (list): Coûts accumulés par les individus.
        abilities_history (list): Capacités de combat au fil des générations.
    """
    plt.figure(figsize=(18, 6))

    # Graphique des rangs de dominance
    plt.subplot(1, 3, 1)
    for i, ranks in enumerate(np.array(dominance_history).T):
        plt.plot(ranks, label=f"Individu {i}")
    plt.xlabel("Générations")
    plt.ylabel("Rang de dominance")
    plt.title("Évolution des rangs de dominance")

    # Graphique des coûts cumulés
    plt.subplot(1, 3, 2)
    costs_history_array = np.array(costs_history)
    for i in range(costs_history_array.shape[1]):
        plt.plot(costs_history_array[:, i], label=f"Individu {i}")
    plt.xlabel("Générations")
    plt.ylabel("Coûts cumulés")
    plt.title("Évolution des coûts par individu")

    # Graphique des capacités de combat
    plt.subplot(1, 3, 3)
    abilities_history_array = np.array(abilities_history)
    for i in range(abilities_history_array.shape[1]):
        plt.plot(abilities_history_array[:, i], label=f"Individu {i}")
    plt.xlabel("Générations")
    plt.ylabel("Capacités de combat")
    plt.title("Évolution des capacités de combat")

    plt.tight_layout()
    plt.show()


# Interface utilisateur avec Tkinter
def run_simulation_ui():
    try:
        population_size = int(entry_population.get())
        generations = int(entry_generations.get())
        learning_rate = float(entry_learning_rate.get())
        damage_cost = float(entry_damage_cost.get())
        mortality_risk = float(entry_mortality_risk.get())

        dominance_history, costs_history, abilities_history = social_dominance_simulation(
            population_size, generations, learning_rate, damage_cost, mortality_risk
        )
        plot_results(dominance_history, costs_history, abilities_history)
    except ValueError as e:
        messagebox.showerror("Erreur", f"Entrée invalide : {e}")


# Interface graphique
root = tk.Tk()
root.title("Simulation de dominance sociale")

tk.Label(root, text="Taille de la population").grid(row=0, column=0, padx=10, pady=5)
entry_population = tk.Entry(root)
entry_population.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nombre de générations").grid(row=1, column=0, padx=10, pady=5)
entry_generations = tk.Entry(root)
entry_generations.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Taux d'apprentissage").grid(row=2, column=0, padx=10, pady=5)
entry_learning_rate = tk.Entry(root)
entry_learning_rate.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Coût des dégâts").grid(row=3, column=0, padx=10, pady=5)
entry_damage_cost = tk.Entry(root)
entry_damage_cost.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Risque de mortalité").grid(row=4, column=0, padx=10, pady=5)
entry_mortality_risk = tk.Entry(root)
entry_mortality_risk.grid(row=4, column=1, padx=10, pady=5)

btn_run = tk.Button(root, text="Lancer la simulation", command=run_simulation_ui)
btn_run.grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()
