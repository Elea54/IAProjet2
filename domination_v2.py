import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import logging

# Configuration du logging détaillé
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

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
    fighting_ability = np.random.uniform(0.5, 1.5, population_size)
    costs = np.zeros(population_size)
    alive = np.ones(population_size, dtype=bool)
    death_order = np.zeros(population_size, dtype=int)
    death_count = 0

    dominance_history = []
    costs_history = []
    abilities_history = []

    logging.debug(f"Initialisation: capacité de combat = {fighting_ability}")

    for generation in range(generations):
        logging.debug(f"--- Génération {generation} ---")
        if np.sum(alive) <= 1:  # Vérifier si seulement un individu reste en vie
            logging.warning(f"Seuls {np.sum(alive)} individus sont en vie à la génération {generation}. Arrêt de la simulation.")
            break
        # Chaque individu interagit avec un autre aléatoirement        
        for i in range(population_size):
            if not alive[i]:
                continue # Si l'individu est mort, il n'interagit pas

            opponent = np.random.randint(0, population_size)
            while opponent == i or not alive[opponent]:
                opponent = np.random.randint(0, population_size)

            logging.debug(f"Individu {i} (capacité {fighting_ability[i]}) combat contre Individu {opponent} (capacité {fighting_ability[opponent]})")
            # Calcul de la probabilité de victoire basée sur les capacités de combat
            prob_win = fighting_ability[i] / (fighting_ability[i] + fighting_ability[opponent])
             # Mise à jour des capacités et des coûts en fonction du résultat de l'interaction
            if np.random.rand() < prob_win:
                fighting_ability[i] += learning_rate * (1 - prob_win)
                costs[opponent] += damage_cost
                logging.debug(f"Individu {i} gagne. Nouvelle capacité = {fighting_ability[i]}")
            else:
                fighting_ability[opponent] += learning_rate * prob_win
                costs[i] += damage_cost
                logging.debug(f"Individu {opponent} gagne. Nouvelle capacité = {fighting_ability[opponent]}")
            # Gestion de la mortalité basée sur les coûts cumulés et la probabilité de risque
            if costs[i] * mortality_risk > np.random.rand() and alive[i]:
                alive[i] = False
                death_count += 1
                death_order[i] = death_count
                logging.info(f"Individu {i} mort à la génération {generation}.")
            if costs[opponent] * mortality_risk > np.random.rand() and alive[opponent]:
                alive[opponent] = False
                death_count += 1
                death_order[opponent] = death_count
                logging.info(f"Individu {opponent} mort à la génération {generation}.")
        # Classement de dominance basé sur les capacités de combat, ajusté pour les morts
        final_ranks = np.zeros_like(fighting_ability, dtype=int)
        sorted_indices = np.argsort(-fighting_ability)

        rank = 1
        for idx in sorted_indices:
            if alive[idx]:
                final_ranks[idx] = rank
                rank += 1
            else:
                final_ranks[idx] = population_size - death_order[idx] + 1

        logging.debug(f"Rangs finaux pour génération {generation}: {final_ranks}")
        
        dominance_history.append(np.copy(final_ranks))
        
        current_costs = np.copy(costs)
        current_abilities = np.copy(fighting_ability)
        
        for j in range(population_size):
            if not alive[j]:
                current_costs[j] = costs[j]
                current_abilities[j] = fighting_ability[j]
        
        costs_history.append(current_costs)
        abilities_history.append(current_abilities)

    return dominance_history, costs_history, abilities_history

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
        plt.plot(ranks)
    plt.xlabel("Générations")
    plt.ylabel("Rang de dominance")
    plt.title("Évolution des rangs de dominance")
    plt.legend(loc="best", fontsize="small", ncol=2)

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
        messagebox.showwarning("Avertissement", f"Entrée invalide, utilisation des valeurs par défaut.")

# Interface graphique
root = tk.Tk()
root.title("Simulation de dominance sociale")

tk.Label(root, text="Taille de la population (10-30)").grid(row=0, column=0, padx=10, pady=5)
entry_population = tk.Entry(root)
entry_population.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nombre de générations (10-30)").grid(row=1, column=0, padx=10, pady=5)
entry_generations = tk.Entry(root)
entry_generations.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Taux d'apprentissage (0.01-1)").grid(row=2, column=0, padx=10, pady=5)
entry_learning_rate = tk.Entry(root)
entry_learning_rate.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Coût des dégâts (0.1-1.0)").grid(row=3, column=0, padx=10, pady=5)
entry_damage_cost = tk.Entry(root)
entry_damage_cost.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Risque de mortalité (0.001-0.5)").grid(row=4, column=0, padx=10, pady=5)
entry_mortality_risk = tk.Entry(root)
entry_mortality_risk.grid(row=4, column=1, padx=10, pady=5)

btn_run = tk.Button(root, text="Lancer la simulation", command=run_simulation_ui)
btn_run.grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()
