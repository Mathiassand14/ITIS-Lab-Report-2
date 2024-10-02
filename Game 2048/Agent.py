
# Game 2048: Artificial intelligence

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns

from AI_Game2048 import run_game
import scipy.stats as stats

def test():
	print_matrix(r"Game 2048\scorePercentilesWithRealScore.csv", "Iteration Per Action", "Percentile", "Score",
	             "Chosen element "
	             "number")
	print_matrix(r"Game 2048\scorePercentiles.csv", "Iteration Per Action", "Percentile", "Score", "Chosen element number")


def main():
	num = 0
	file = r"Game 2048\scorePercentiles.csv"

	file = r"Game 2048\scorePercentilesWithRealScore.csv"
	while True:

		pygame_enabled = 0
		#avr_pct = randint(0, 10) * 10
		#num_games_pr_action = 2 ** randint(2, 4)
		#avr_pct = 0
		#num_games_pr_action = 4
		#num += num_games_pr_action
		data = get_data("Chosen element number", file, "Score", "Iteration Per Action",
		                "Percentile")[0]
		if data.__len__() == 0:
			num_games_pr_action = 1
			avr_pct = 0
		else:
			element = []
			for t in range(len(data[0])):
				for i in range(len(data)):

					element = data[i][t]
					if element["Count"] < 100:
						element = [2**t,i*10]
						break
					elif len(data) <= 10:
						element = [2**(t),(i+1) * 10]


				if type(element) == list:
					break
			else:
				element = [2**(t+1),0]
			# Reassign these values
			num_games_pr_action = element[0]
			avr_pct = element[1]


		print(num_games_pr_action, avr_pct)
		#i, amount = get_max_value_and_count(r"Game 2048\score.csv", "Iteration Per Action")
		#plot_distribution_from_csv(r"Game 2048\score.csv", "Iteration Per Action", "Score", 1, 100)
		score = np.empty((0, 4), int)

		sc = run_game(num_games_pr_action, pygame_enabled, avr_pct)
		score = np.append(score, [[num_games_pr_action, sc, (np.percentile(list(range(1, num_games_pr_action + 1)), avr_pct,
		                                                method = "nearest") if avr_pct != 0 else 0),avr_pct]], axis=0)
		print(score, num_games_pr_action, (np.percentile(list(range(1, num_games_pr_action + 1)), avr_pct,
		                                                method = "nearest") if avr_pct != 0 else 0), num)

		amount = 0
		save_array_to_csv(score, file, ["Iteration Per Action", "Score", "Chosen element number", "Percentile"])
		print("old matrix")
<<<<<<< Updated upstream
		print_matrix(r"Game 2048\scorePercentilesWithRealScore.csv", "Iteration Per Action", "Percentile", "Score", "Chosen element "
=======
		print_matrix(r"Game 2048\scorePercentiles.csv", "Iteration Per Action", "Percentile", "Score", "Chosen element "
>>>>>>> Stashed changes
		                                                                                         "number")
		print_matrix(file, "Iteration Per Action", "Percentile", "Score", "Chosen element number")


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

def print_matrix(csv_file, x_col, y_col, data_col, chosen_element):
	# Læs CSV-filen
	data, x, y = get_data(chosen_element, csv_file, data_col, x_col, y_col)

	# Saml alle unikke nøgler
	all_labels = set()
	for dat in data:
		for da in dat:
			all_labels.update(da.keys())

	# Konverter sættet til en liste (valgfrit, hvis du vil have en liste som output)
	order = ["Count", "Mean", "Std", "Std_pct", "ConIntB", "ConIntT", "Max", "Min"]
	all_labels_list = list(all_labels)
	all_labels_list.sort(key = lambda x: order.index(x))

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


def get_data(chosen_element, csv_file, data_col, x_col, y_col):
	try:
		df = pd.read_csv(csv_file)

		# Opret en kombineret XY-kolonne
		df['XY'] = list(zip(df[x_col], df[y_col]))
		df['XC'] = list(zip(df[x_col], df[chosen_element]))
		x = df.sort_values(by = x_col)[x_col].unique()
		y = df.sort_values(by = y_col)[y_col].unique()
		data = []
		for i in y:
			dat = []
			for j in x:
				# Brug den kombinerede XY-kolonne til at hente data
				xy_matches = df[df['XY'] == (j, i)]
				if not xy_matches.empty:
					xc_value = xy_matches[chosen_element].values[0]
					d = df[(df['XY'] == (j, i)) | (df['XC'] == (j, xc_value))][data_col]
				else:
					d = pd.Series([], dtype = 'float64')  # Tom serie, hvis der ikke er nogen match

				dat.append({
					"Mean"   : f"{d.mean():.2f}" if not pd.isna(d.mean()) else "NaN",
					"Std"    : f"{d.std():.2f}" if not pd.isna(d.std()) else "NaN",
					"Min"    : f"{d.min():.2f}" if not pd.isna(d.min()) else "NaN",
					"Max"    : f"{d.max():.2f}" if not pd.isna(d.max()) else "NaN",
					"Count"  : d.count(),
					"Std_pct": f"{d.std() / d.mean() * 100:.2f}%" if not pd.isna(d.std()) and d.mean() != 0 else "NaN",
					"ConIntB" : f""
					            f"{stats.t.interval(0.95, len(d) - 1, loc = d.mean(), scale = stats.sem(d))[0]:.2f}"
					if not pd.isna(d.mean()) else "NaN",
					"ConIntT" : f"{stats.t.interval(0.95, len(d) - 1, loc = d.mean(), scale = stats.sem(d))[1]:.2f}"
					if not pd.isna(d.mean()) else "NaN"
				})
			data.append(dat)
		return data, x, y
	except:
		return None, None, None


if __name__ == "__main__":
	#main()
	test()



