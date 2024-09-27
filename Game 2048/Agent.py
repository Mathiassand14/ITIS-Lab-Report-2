
# Game 2048: Artificial intelligence
from operator import indexOf

from sympy.core.random import randint

from Game2048 import Game2048
import numpy as np
import pygame
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from AI_Game2048 import run_game


def main():

	while True:
		pygame_enabled = False
		avr_pct = randint(0, 10) * 10
		num_games_pr_action = 2 ** randint(0, 5)
		print(num_games_pr_action, avr_pct)
		#i, amount = get_max_value_and_count(r"Game 2048\score.csv", "Iteration Per Action")
		#plot_distribution_from_csv(r"Game 2048\score.csv", "Iteration Per Action", "Score", 1, 100)
		score = np.empty((0, 3), int)

		sc = run_game(num_games_pr_action, pygame_enabled, avr_pct)
		score = np.append(score, [[num_games_pr_action, sc, avr_pct]], axis=0)
		print(score, num_games_pr_action, avr_pct)

		amount = 0
		save_array_to_csv(score, r"Game 2048\scorePercentiles.csv", ["Iteration Per Action", "Score", "Percentile"])
		print_matrix(r"Game 2048\scorePercentiles.csv", "Iteration Per Action", "Percentile", "Score")


def save_array_to_csv(array: np.ndarray, filename: str, column_names=None):
	try:
		# Opret DataFrame fra arrayet
		df = pd.DataFrame(array, columns=column_names)

		# Check om filen eksisterer
		file_exists = os.path.isfile(filename)

		# Hvis filen eksisterer, læs de eksisterende data
		if file_exists:
			with open(filename, 'a', newline='') as f:
				# Tilføj data uden overskrifter
				df.to_csv(f, index=False, header=False)
		else:
			# Hvis filen ikke eksisterer, skriv data med overskrifter
			df.to_csv(filename, index=False, header=True)

		print(f"Array gemt som CSV-fil: {filename}")
	except Exception as e:
		print(f"En fejl opstod under forsøget på at gemme arrayet som CSV: {e}")


def get_max_value_and_count(filename: str, column_name: str):
	# Få den absolutte sti til filen
	file_path = os.path.join(os.path.dirname(__file__), filename)

	df = pd.read_csv(filename)

	# Kontrollér om kolonnen findes
	if column_name not in df.columns:
		raise ValueError(f"Kolonnen '{column_name}' findes ikke i CSV-filen")

	# Hent højeste værdi i kolonnen
	max_value = df[column_name].max()

	# Tæl hvor mange gange den højeste værdi forekommer
	max_count = (df[column_name] == max_value).sum()

	return max_value, max_count

def plot_distribution_from_csv(filename: str, x_col: str, y_col: str, x_bin_size: float, y_bin_size: float):
	try:
		# Få den absolutte sti til filen
		file_path = os.path.join(os.path.dirname(__file__), filename)

		df = pd.read_csv(filename)

		if x_col not in df.columns or y_col not in df.columns:
			raise ValueError(f"Kolonnerne '{x_col}' og/eller '{y_col}' findes ikke i CSV-filen")

		# Sikr, at værdier ikke kommer under 0
		df[x_col] = df[x_col].clip(lower=1)
		df[y_col] = df[y_col].clip(lower=0)

		# Convert x_col values into bin labels
		df['x_bin'] = df[x_col] - 1


		# Plot violinplot
		plt.figure(figsize=(12, 6))
		sns.violinplot(x=x_col, y=y_col, data=df, inner=None, bw_adjust=0.2, bw_method=0.5, cut=0)

		# Beregn og plot kvartiler og gennemsnit
		grouped_df = df.groupby('x_bin')[y_col].describe(percentiles=[.25, .5, .75]).reset_index()
		mean_df = df.groupby('x_bin')[y_col].mean().reset_index()

		# Find den faktiske midtpunkt af hvert x_bin til korrekt justering
		bin_centers = sorted(df['x_bin'].unique())

		plt.plot(bin_centers, grouped_df['25%'], 'r--', label='1. kvartil (25%)')
		plt.plot(bin_centers, grouped_df['50%'], 'g-', label='Median (50%)')
		plt.plot(bin_centers, grouped_df['75%'], 'b--', label='3. kvartil (75%)')
		plt.plot(bin_centers, mean_df[y_col], 'm-.', label='Gennemsnit')

		# Tilføj labels og titler
		plt.xlabel(x_col)
		plt.ylabel(y_col)
		plt.title(f'Distribution af Observationer (x Bin Size: {x_bin_size})')
		plt.legend()
		plt.grid(axis='y')

		# Vis plot
		plt.show()

	except Exception as e:
		print(f"En fejl opstod under forsøget på at plotte fordelingen: {e}")

def print_matrix(csv_file, x_col, y_col, data_col):
	# Læs CSV-filen
	df = pd.read_csv(csv_file)
	x = df.sort_values(by = x_col)[x_col].unique()
	y = df.sort_values(by = y_col)[y_col].unique()
	data = []
	for i in y:
		dat = []
		for j in x:
			d = df[(df[x_col] == j) & (df[y_col] == i)][data_col]  # Note the correct x and y comparison
			dat.append({
				"Mean" : f"{d.mean():.2f}" if not pd.isna(d.mean()) else "NaN",
				"Std"  : f"{d.std():.2f}" if not pd.isna(d.std()) else "NaN",
				"Min"  : f"{d.min():.2f}" if not pd.isna(d.min()) else "NaN",
				"Max"  : f"{d.max():.2f}" if not pd.isna(d.max()) else "NaN",
				"Count": d.count()
			})
		data.append(dat)

	# Saml alle unikke nøgler
	all_labels = set()
	for dat in data:
		for da in dat:
			all_labels.update(da.keys())

	# Konverter sættet til en liste (valgfrit, hvis du vil have en liste som output)
	all_labels_list = list(all_labels)

	p = ""
	for i in x:
		p += "| " + f"{i}" + "\t" * ((len(all_labels_list) *(3) - len("| " + f"{i}") // 4))
	print("\t" * 2 + p)
	p = ""
	for i in all_labels_list:
		p += "| " + i + ":" + "\t" * (3 - len("| " + i + ":") // 4)
	print("\t" * 2 + p * len(x) + "\t" * 2)

	for idx, i in enumerate(y):
		p = ""
		for j in x:
			dat = data[idx]  # Adjusted indexing of data
			for t in all_labels_list:
				p += "| " + f"{dat[x.tolist().index(j)][t]}" + "\t" * (
							3 - len("| " + f"{dat[x.tolist().index(j)][t]}") // 4)
		print((str(i) if i != 0 else "Avr") + "\t" * 2 + p)
		print("--------+" + (("-" * (4 * 3 - 1) + "+") * len(all_labels_list)) * len(x))


if __name__ == "__main__":
	main()


if __name__ == "__main__":
	main()
