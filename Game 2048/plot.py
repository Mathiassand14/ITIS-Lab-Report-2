import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from Agent import get_data


def plot_data_with_confidence_intervals(data):
    """
	Function to plot mean with confidence intervals.
	:param data: Dictionary containing keys 'Mean', 'ConIntB', and 'ConIntT'.
	"""
    # Create 'LogIndex' based on length of 'Mean'
    log_index = [2 ** i for i in range(len(data['Mean']))]

    plt.figure(figsize = (10, 6))

    # Plotting the mean
    sns.lineplot(x = log_index, y = data['Mean'], label = 'Mean', color = 'blue')

    # Plotting the confidence intervals
    plt.fill_between(log_index, data['ConIntB'], data['ConIntT'], color = 'blue', alpha = 0.3,
                     label = 'Confidence Interval')
    plt.xlabel('Index')
    plt.ylabel('Values')
    plt.title('Plot of Mean with Confidence Intervals')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    data = get_data("Chosen element number", r"scorePercentilesWithRealScore.csv", "Score", "Iteration Per Action",
                    "Percentile")[0]

    # Debug print to inspect data
    print("Fetched Data:\n", data)

    # Check if data is a dictionary and contains the keys 'Mean', 'ConIntB', and 'ConIntT'

    # Plot the data
    mean = [float(t["Mean"]) for t in data[0] ]

    conIntB = [float(t["ConIntB"]) for t in data[0]]

    conIntT = [float(t["ConIntT"]) for t in data[0]]

    id = [2**t for t in range(len(data[0]))]

    data_tuples = sorted(zip(mean, conIntB, conIntT, id), key = lambda x: x[0])

    # Pak data ud igen efter sortering
    sorted_mean, sorted_conIntB, sorted_conIntT, sorted_id = zip(*data_tuples)

    # Debug udskrifter for at bekræfte sorteringen
    print("Sorted Mean: ", sorted_mean)
    print("Sorted ConIntB: ", sorted_conIntB)
    print("Sorted ConIntT: ", sorted_conIntT)
    print("Sorted ID: ", sorted_id)

    # Plot de sorterede mean værdier
    plt.plot(sorted_id, sorted_mean, label = 'Mean', marker = 'o')

    # Plot de sorterede konfidensintervaller
    plt.fill_between(sorted_id, sorted_conIntB, sorted_conIntT, color = 'lightgray', alpha = 0.5,
                     label = 'Confidence Interval')

    # Tilføj logaritmisk skala til x-aksen med base 2
    plt.xscale('log', base = 2)

    # Tilføj labels og titel
    plt.xlabel('ID (log2 scale)')
    plt.ylabel('Values')
    plt.title('Mean Values with Confidence Intervals (Sorted, Log2 Scale)')

    # Tilføj legend
    plt.legend()

    # Vis plottet
    plt.show()




