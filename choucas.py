import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def jackdaw_game(simulations=100, iterations=50, payoff_matrix_male=None, payoff_matrix_female=None):
    """
    Simule un modèle de théorie des jeux pour analyser les comportements des choucas en stress,
    et calcule les gains moyens pour les mâles et les femelles.

    Parameters:
        simulations (int): Nombre de simulations à exécuter.
        iterations (int): Nombre d'interactions par simulation.
        payoff_matrix_male (np.array): Matrice de gains pour les stratégies mâles.
        payoff_matrix_female (np.array): Matrice de gains pour les stratégies femelles.

    Returns:
        history (dict): Historique des proportions de stratégies des mâles et des femelles.
        average_gains (dict): Gains moyens pour les mâles et les femelles.
    """
    if payoff_matrix_male is None:
        payoff_matrix_male = np.array([
            [5, 2],
            [3, 4]
        ])
    
    if payoff_matrix_female is None:
        payoff_matrix_female = np.array([
            [5, 3],
            [2, 4]
        ])

    history = {
        "male_consolation": [],
        "male_avoidance": [],
        "female_signal": [],
        "female_neutral": []
    }
    
    average_gains = {
        "male": [],
        "female": []
    }

    for _ in range(simulations):
        male_strategy_counts = np.array([50, 50])
        female_strategy_counts = np.array([50, 50])
        male_gains = 0
        female_gains = 0

        for _ in range(iterations):
            male_probs = male_strategy_counts / np.sum(male_strategy_counts)
            female_probs = female_strategy_counts / np.sum(female_strategy_counts)

            male_choice = np.random.choice([0, 1], p=male_probs)
            female_choice = np.random.choice([0, 1], p=female_probs)

            male_gain = payoff_matrix_male[male_choice, female_choice]
            female_gain = payoff_matrix_female[male_choice, female_choice]

            male_strategy_counts[male_choice] += male_gain
            female_strategy_counts[female_choice] += female_gain

            male_gains += male_gain
            female_gains += female_gain

        total_male = np.sum(male_strategy_counts)
        total_female = np.sum(female_strategy_counts)

        history["male_consolation"].append(male_strategy_counts[0] / total_male)
        history["male_avoidance"].append(male_strategy_counts[1] / total_male)
        history["female_signal"].append(female_strategy_counts[0] / total_female)
        history["female_neutral"].append(female_strategy_counts[1] / total_female)

        average_gains["male"].append(male_gains / iterations)
        average_gains["female"].append(female_gains / iterations)

    return history, average_gains

def plot_results(history):
    """
    Affiche les résultats de la simulation.

    Parameters:
        history (dict): Historique des proportions de stratégies des mâles et des femelles.
    """
    plt.figure(figsize=(10, 6))
    
    # Stratégies des mâles
    plt.plot(history["male_consolation"], label="Mâle : Consolation", color="blue")
    plt.plot(history["male_avoidance"], label="Mâle : Évitement", color="red")

    # Stratégies des femelles
    plt.plot(history["female_signal"], label="Femelle : Signalement", linestyle="--", color="green")
    plt.plot(history["female_neutral"], label="Femelle : Neutralité", linestyle="--", color="orange")

    plt.xlabel("Simulations")
    plt.ylabel("Proportion des stratégies")
    plt.title("Analyse des comportements des choucas")
    plt.legend()
    plt.grid()
    plt.show()

def plot_average_gains(average_gains):
    """
    Affiche l'évolution des gains moyens pour les mâles et les femelles.

    Parameters:
        average_gains (dict): Gains moyens pour les mâles et les femelles.
    """
    plt.figure(figsize=(10, 6))

    plt.plot(average_gains["male"], label="Gains moyens des mâles", color="blue")
    plt.plot(average_gains["female"], label="Gains moyens des femelles", color="green")

    plt.xlabel("Simulations")
    plt.ylabel("Gains moyens")
    plt.title("Évolution des gains moyens pour les mâles et les femelles")
    plt.legend()
    plt.grid()
    plt.show()

def plot_final_strategy_distribution(history):
    """
    Affiche la distribution finale des stratégies adoptées par les mâles et les femelles.

    Parameters:
        history (dict): Historique des proportions de stratégies des mâles et des femelles.
    """
    final_male_consolation = history["male_consolation"][-1]
    final_male_avoidance = history["male_avoidance"][-1]
    final_female_signal = history["female_signal"][-1]
    final_female_neutral = history["female_neutral"][-1]

    strategies = ["Consolation (M)", "Évitement (M)", "Signalement (F)", "Neutralité (F)"]
    proportions = [final_male_consolation, final_male_avoidance, final_female_signal, final_female_neutral]

    plt.figure(figsize=(10, 6))
    plt.bar(strategies, proportions, color=["blue", "red", "green", "orange"])

    plt.xlabel("Stratégies")
    plt.ylabel("Proportion finale")
    plt.title("Distribution finale des stratégies")
    plt.grid(axis='y')
    plt.show()

def get_payoff_matrix():
    """
    Crée une interface utilisateur pour entrer des matrices de gains personnalisées pour la simulation.

    Returns:
        payoff_matrix_male (np.array): Matrice de gains personnalisée pour les stratégies mâles.
        payoff_matrix_female (np.array): Matrice de gains personnalisée pour les stratégies femelles.
    """
    def submit():
        # Récupérer les valeurs des champs d'entrée
        values = [float(entry.get()) for entry in entries]
        payoff_matrix_male = np.array([
            [values[0], values[1]],
            [values[2], values[3]]
        ])

        payoff_matrix_female = np.array([
            [values[4], values[5]],
            [values[6], values[7]]
        ])

        root.quit()  # Fermer la fenêtre
        return payoff_matrix_male, payoff_matrix_female

    root = tk.Tk()
    root.title("Matrice de gains")

    # Labels pour les champs d'entrée
    labels = [
        "Mâle : Consolation - Femelle : Signalement",
        "Mâle : Consolation - Femelle : Neutralité",
        "Mâle : Évitement - Femelle : Signalement",
        "Mâle : Évitement - Femelle : Neutralité",
        "Femelle : Signalement - Mâle : Consolation",
        "Femelle : Signalement - Mâle : Évitement",
        "Femelle : Neutralité - Mâle : Consolation",
        "Femelle : Neutralité - Mâle : Évitement"
    ]

    entries = []

    for i, label_text in enumerate(labels):
        label = ttk.Label(root, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)
        entry = ttk.Entry(root)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    submit_button = ttk.Button(root, text="Soumettre", command=submit)
    submit_button.grid(row=len(labels), columnspan=2, pady=10)

    root.mainloop()

    return submit()

# Obtenir des matrices de gains personnalisées de l'utilisateur
payoff_matrix_male, payoff_matrix_female = get_payoff_matrix()

# Exécuter la simulation avec les matrices de gains personnalisées
history, average_gains = jackdaw_game(simulations=100, iterations=50, payoff_matrix_male=payoff_matrix_male, payoff_matrix_female=payoff_matrix_female)
plot_results(history)
plot_average_gains(average_gains)
plot_final_strategy_distribution(history)