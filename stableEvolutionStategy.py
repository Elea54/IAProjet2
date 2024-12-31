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

# Parameters
V = 10  # Value of the resource
C = 20  # Cost of fighting
population_size = 100

generations = 100
history = hawk_dove_game(V, C, population_size, generations)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(history, label="Fraction of Hawks")
plt.axhline(0.5, color='r', linestyle='--', label="ESS Threshold")
plt.xlabel("Generations")
plt.ylabel("Fraction of Hawks")
plt.title("Hawk-Dove Game: Evolution of Strategies")
plt.legend()
plt.show()