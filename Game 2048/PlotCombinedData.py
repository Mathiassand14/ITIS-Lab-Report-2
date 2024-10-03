
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from Agent import get_data

def plot_combined_data(data_with_real_score, data_without_real_score):
	"""
	Function to plot mean with confidence intervals for two datasets.
	:param data_with_real_score: Dictionary containing keys 'Mean', 'ConIntB', 'ConIntT' from the 'scorePercentilesWithRealScore.csv'.
	:param data_without_real_score: Dictionary containing keys 'Mean', 'ConIntB', 'ConIntT' from the 'scorePercentiles.csv'.
	"""
	# Create 'LogIndex' based on length of 'Mean' from the first dataset
	log_index = [2 ** i for i in range(len(data_with_real_score['Mean']))]

	plt.figure(figsize=(10, 6))

	# Check if lengths of all arrays are the same
	if not all(len(data_with_real_score[key]) == len(data_without_real_score[key]) for key in data_with_real_score):
		raise ValueError("All arrays in data_with_real_score and data_without_real_score must be of the same length")

	# Plotting the mean for data_with_real_score
	sns.lineplot(x=log_index, y=data_with_real_score['Mean'], label='Mean - With Real Score', color='blue')
	plt.fill_between(log_index, data_with_real_score['ConIntB'], data_with_real_score['ConIntT'], color='blue', alpha=0.3, label='Confidence Interval - With Real Score')

	# Plotting the mean for data_without_real_score
	sns.lineplot(x=log_index, y=data_without_real_score['Mean'], label='Mean - Without Real Score', color='green')
	plt.fill_between(log_index, data_without_real_score['ConIntB'], data_without_real_score['ConIntT'], color='green', alpha=0.3, label='Confidence Interval - Without Real Score')

	plt.xlabel('Index')
	plt.xscale('log', base = 2)
	plt.ylabel('Values')
	plt.title('Plot of Mean with Confidence Intervals')
	plt.legend()
	plt.show()

if __name__ == "__main__":
	# Fetch data from both files
	data_with_real_score = get_data("Chosen element number", r"scorePercentilesWithRealScore.csv", "Score", "Iteration Per Action", "Percentile")[0]
	data_without_real_score = get_data("Chosen element number", r"scorePercentiles.csv", "Score", "Iteration Per Action", "Percentile")[0]

	# Debug print to inspect data
	print("Fetched Data with Real Score:\n", data_with_real_score)
	print("Fetched Data without Real Score:\n", data_without_real_score)

	# Prepare data for plotting
	data_with_real_score = {
		'Mean': [float(t["Mean"]) for t in data_with_real_score[0]],
		'ConIntB': [float(t["ConIntB"]) for t in data_with_real_score[0]],
		'ConIntT': [float(t["ConIntT"]) for t in data_with_real_score[0]]
	}

	data_without_real_score = {
		'Mean': [float(t["Mean"]) for t in data_without_real_score[0]],
		'ConIntB': [float(t["ConIntB"]) for t in data_without_real_score[0]],
		'ConIntT': [float(t["ConIntT"]) for t in data_without_real_score[0]]
	}

	# Ensure lengths are the same for plotting
	if len(data_with_real_score['Mean']) != len(data_without_real_score['Mean']):
		min_length = min(len(data_with_real_score['Mean']), len(data_without_real_score['Mean']))
		data_with_real_score = {key: value[:min_length] for key, value in data_with_real_score.items()}
		data_without_real_score = {key: value[:min_length] for key, value in data_without_real_score.items()}

	# Plot the combined data
	plot_combined_data(data_with_real_score, data_without_real_score)
