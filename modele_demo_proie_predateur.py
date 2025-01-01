import tkinter as tk
from tkinter import messagebox
import numpy as np
import subprocess
import sys
import matplotlib.pyplot as plt

# Fonction pour installer matplotlib si nécessaire
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Matplotlib not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
    print("Matplotlib installed successfully!")

# Simulation du modèle proie-prédateur avec matrice de payoffs
def lotka_volterra_with_payoff(alpha, beta, delta, gamma, prey_init, predator_init, steps):
    """
    Simule le modèle proie-prédateur Lotka-Volterra avec une matrice de payoffs.

    Parameters:
        alpha (float): Taux de croissance des proies.
        beta (float): Taux de prédation.
        delta (float): Taux de reproduction des prédateurs.
        gamma (float): Taux de mortalité des prédateurs.
        prey_init (int): Population initiale des proies.
        predator_init (int): Population initiale des prédateurs.
        steps (int): Nombre de pas de temps.

    Returns:
        prey_history (list): Évolution de la population des proies.
        predator_history (list): Évolution de la population des prédateurs.
        payoff_matrix (ndarray): Matrice des payoffs calculée au fil du temps.
    """
    # Initialisation des populations
    prey = prey_init
    predator = predator_init
    prey_history = [prey]
    predator_history = [predator]

    # Matrice de payoffs
    payoff_matrix = np.zeros((2, 2))

    for _ in range(steps):
        # Calcul des changements de population
        prey_change = alpha * prey - beta * prey * predator
        predator_change = delta * prey * predator - gamma * predator

        # Mise à jour des populations
        prey = max(prey + prey_change, 0)
        predator = max(predator + predator_change, 0)

        # Mise à jour de l'historique
        prey_history.append(prey)
        predator_history.append(predator)

        # Mise à jour des payoffs
        payoff_matrix[0, 0] += prey * alpha
        payoff_matrix[0, 1] += -beta * prey * predator
        payoff_matrix[1, 0] += delta * prey * predator
        payoff_matrix[1, 1] += -gamma * predator

    return prey_history, predator_history, payoff_matrix

# Affichage de la matrice des payoffs
def display_payoff_matrix(matrix):
    """
    Affiche la matrice de payoffs.

    Parameters:
        matrix (ndarray): La matrice des payoffs.
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.matshow(matrix, cmap="Blues")

    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha='center', va='center', color="white")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Proie', 'Prédateur'])
    ax.set_yticklabels(['Proie', 'Prédateur'])

    ax.set_xlabel('Interaction')
    ax.set_ylabel('Type')
    ax.set_title('Matrice des payoffs')
    plt.show()

# Fonction pour tracer les populations
def plot_population(prey_history, predator_history):
    """
    Trace l'évolution des populations des proies et des prédateurs.

    Parameters:
        prey_history (list): Évolution de la population des proies.
        predator_history (list): Évolution de la population des prédateurs.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(prey_history, label="Proies", color='green')
    plt.plot(predator_history, label="Prédateurs", color='red')
    plt.xlabel("Temps")
    plt.ylabel("Population")
    plt.title("Évolution des populations (Proies-Prédateurs)")
    plt.legend()
    plt.show()

# Fonction pour exécuter la simulation via l'interface utilisateur
def run_simulation():
    """
    Exécute la simulation du modèle proie-prédateur avec les paramètres saisis dans l'IHM.
    """
    try:
        # Récupération des valeurs saisies
        alpha = float(entry_alpha.get())
        beta = float(entry_beta.get())
        delta = float(entry_delta.get())
        gamma = float(entry_gamma.get())
        prey_init = int(entry_prey.get())
        predator_init = int(entry_predator.get())
        steps = int(entry_steps.get())

        # Validation des entrées
        if any(param <= 0 for param in [alpha, beta, delta, gamma, prey_init, predator_init, steps]):
            raise ValueError("Toutes les valeurs doivent être positives.")

        # Exécution de la simulation
        prey_history, predator_history, payoff_matrix = lotka_volterra_with_payoff(
            alpha, beta, delta, gamma, prey_init, predator_init, steps
        )

        # Affichage des résultats
        plot_population(prey_history, predator_history)
        display_payoff_matrix(payoff_matrix)

    except ValueError as e:
        messagebox.showerror("Erreur", f"Entrée invalide : {e}")

# Création de l'interface utilisateur
root = tk.Tk()
root.title("Simulation Proie-Prédateur")

# Labels et champs de saisie
tk.Label(root, text="Taux de croissance des proies (alpha)").grid(row=0, column=0, padx=10, pady=5)
entry_alpha = tk.Entry(root)
entry_alpha.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Taux de prédation (beta)").grid(row=1, column=0, padx=10, pady=5)
entry_beta = tk.Entry(root)
entry_beta.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Taux de reproduction des prédateurs (delta)").grid(row=2, column=0, padx=10, pady=5)
entry_delta = tk.Entry(root)
entry_delta.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Taux de mortalité des prédateurs (gamma)").grid(row=3, column=0, padx=10, pady=5)
entry_gamma = tk.Entry(root)
entry_gamma.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Population initiale des proies").grid(row=4, column=0, padx=10, pady=5)
entry_prey = tk.Entry(root)
entry_prey.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Population initiale des prédateurs").grid(row=5, column=0, padx=10, pady=5)
entry_predator = tk.Entry(root)
entry_predator.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Nombre de pas de temps").grid(row=6, column=0, padx=10, pady=5)
entry_steps = tk.Entry(root)
entry_steps.grid(row=6, column=1, padx=10, pady=5)

# Bouton pour exécuter la simulation
btn_run = tk.Button(root, text="Exécuter la simulation", command=run_simulation)
btn_run.grid(row=7, column=0, columnspan=2, pady=20)

# Boucle principale de l'IHM
root.mainloop()
