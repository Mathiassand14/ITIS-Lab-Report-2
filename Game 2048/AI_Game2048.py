# Game 2048: Artificial intelligence
from operator import indexOf
from Game2048 import Game2048
import numpy as np
import pygame
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Instructions:
#   Move up, down, left, or right to merge the tiles. The objective is to
#   get a tile with the number 2048 (or higher)
#
# Control:
#    arrows  : Merge up, down, left, or right
#    r       : Restart game
#    q / ESC : Quit


from Montecarlo import rate_actions
def run_game(num_games_pr_action: int = 10):
    env = Game2048(pygame_enabled = False)
    env.reset()
    actions = ['left', 'right', 'up', 'down']
    exit_program = False
    action_taken = False

    while not exit_program:
        env.render()


        # Process game events
        if env.pygame_enabled:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_program = True
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        exit_program = True
                    if event.key == pygame.K_UP:
                        action, action_taken = 'up', True
                    if event.key == pygame.K_DOWN:
                        action, action_taken  = 'down', True
                    if event.key == pygame.K_RIGHT:
                        action, action_taken  = 'right', True
                    if event.key == pygame.K_LEFT:
                        action, action_taken  = 'left', True
                    if event.key == pygame.K_r:
                        env.reset()


        # INSERT YOUR CODE HERE
        #
        # Implement an AI to play 2048 using simple Monte Carlo search
        #
        # The information you have available is the game state (board, score)
        #
        # You control the game by setting the action to either
        #    'up', 'down', 'left', or 'right'
        #
        # HINTS
        # You can set up a new game simulation at the current game state like this
        # sim = Game2048((env.board, env.score))
        #
        # You can then play a random game like this
        # done = False
        # while not done:
        #     action = actions[np.random.randint(4)]
        #     (board, score), reward, done = sim.step(action)
        #
        # When you take an action, set the variable action_taken to True. As you
        # can see below, the code only steps the environment when action_taken
        # is True, since the whole game runs in an infinite loop.

        r_a = rate_actions(env, num_games_pr_action, actions)
        # END O
        best_action=indexOf(r_a,max(r_a))
        action=actions[best_action]
        action_taken = True
        done = False
        if action_taken:
            (board, score), reward, done = env.step(action)
            action_taken = False
        if done:
            break


    env.close()

    return score

def main():
    i, amount = get_max_value_and_count("score.csv", "Iteration Per Action")
    while True:
        plot_distribution_from_csv("score.csv", "Iteration Per Action", "Score", 1, 10)
        score = np.empty((0, 2), int)
        mean = np.empty((0, 2), float)
        avr = 0

        for j in range(amount, 100):
            sc = run_game(i)
            score = np.append(score, [[i, sc]], axis = 0)
            avr = np.average(score[:, 1])
            print(avr, i, j)

        mean = np.append(mean, [[i, avr]], axis = 0)

        i += 1
        amount = 0
        save_array_to_csv(score, "score.csv", ["Iteration Per Action", "Score"])
        save_array_to_csv(mean, "mean.csv", ["Iteration Per Action", "Mean Score"])



def save_array_to_csv(array: np.ndarray, filename: str, column_names = None):
    try:
        df = pd.DataFrame(array, columns = column_names)

        if os.path.isfile(filename):  # Check if file exists
            existing_df = pd.read_csv(filename)

            # Check if the headers match
            if not existing_df.columns.equals(df.columns):
                print(f"Kolonneoverskrifterne matcher ikke. Eksisterende kolonner: "
                    f"{existing_df.columns.values} | Nye kolonner: {df.columns.values}")
                return  # Or handle it as required, e.g., correcting headers or raising an error

            # Append data
            df.to_csv(filename, mode = 'a', index = False, header = False)
        else:
            # Write data with header
            df.to_csv(filename, mode = 'w', index = False, header = True)

        print(f"Array gemt som CSV-fil: {filename}")
    except Exception as e:
        print(f"En fejl opstod under forsøget på at gemme arrayet som CSV: {e}")


def get_max_value_and_count(filename: str, column_name: str):
    # Få den absolutte sti til filen
    file_path = os.path.join(os.path.dirname(__file__), filename)

    df = pd.read_csv(file_path)

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

		df = pd.read_csv(file_path)

		if x_col not in df.columns or y_col not in df.columns:
			raise ValueError(f"Kolonnerne '{x_col}' og/eller '{y_col}' findes ikke i CSV-filen")

		# Sikr, at værdier ikke kommer under 0
		df[x_col] = df[x_col].clip(lower = 1)
		df[y_col] = df[y_col].clip(lower = 0)

		# Convert x_col values into bin labels
		df['x_bin'] = df[x_col] -1


		# Plot violinplot
		plt.figure(figsize = (12, 6))
		sns.violinplot(x = x_col, y = y_col, data = df, inner = None,)

		# Beregn og plot kvartiler og gennemsnit
		grouped_df = df.groupby('x_bin')[y_col].describe(percentiles = [.25, .5, .75]).reset_index()
		mean_df = df.groupby('x_bin')[y_col].mean().reset_index()

		# Find den faktiske midtpunkt af hvert x_bin til korrekt justering
		bin_centers = sorted(df['x_bin'].unique())

		plt.plot(bin_centers, grouped_df['25%'], 'r--', label = '1. kvartil (25%)')
		plt.plot(bin_centers, grouped_df['50%'], 'g-', label = 'Median (50%)')
		plt.plot(bin_centers, grouped_df['75%'], 'b--', label = '3. kvartil (75%)')
		plt.plot(bin_centers, mean_df[y_col], 'm-.', label = 'Gennemsnit')

		# Tilføj labels og titler
		plt.xlabel(x_col)
		plt.ylabel(y_col)
		plt.title(f'Distribution af Observationer (x Bin Size: {x_bin_size})')
		plt.legend()

		# Vis plot
		plt.show()

	except Exception as e:
		print(f"En fejl opstod under forsøget på at plotte fordelingen: {e}")


if __name__ == "__main__":
    main()
