
from Game2048 import Game2048
import numpy as np


def rate_actions_avr(board: Game2048, num_games_pr_action: int, posible_actions: list):
	actions_ratings = []
	for action in posible_actions:
		action_scores = []
		for i in range(num_games_pr_action):
			temp_board = Game2048((board.board, board.score),)
			(temp_board_state, temp_score), reward, done = temp_board.step(action)

			while not done:
				random_action = posible_actions[np.random.randint(len(posible_actions))]
				(temp_board_state, temp_score), reward, done = temp_board.step(random_action)


			action_scores.append(sum(temp_board.board))


		mean_action_score = np.mean(action_scores)
		actions_ratings.append(mean_action_score)
	return actions_ratings


def rate_actions_pct(board: Game2048, num_games_pr_action: int, posible_actions: list, pct: int):
	actions_ratings = []
	for action in posible_actions:
		action_scores = []
		for i in list(range(num_games_pr_action)):
			temp_board = Game2048((board.board, board.score), )
			(temp_board_state, temp_score), reward, done = temp_board.step(action)
			while not done:
				random_action = posible_actions[np.random.randint(len(posible_actions))]
				(temp_board_state, temp_score), reward, done = temp_board.step(random_action)
			action_scores.append(sum(temp_board.board))
			#print(t, "moves")
		if action_scores:  # Check if action_scores is not empty
			pct_action_score = np.percentile(action_scores, pct, method = "nearest")
		else:
			pct_action_score = 0  # Default value or handle it differently if needed

		actions_ratings.append(pct_action_score)
	return actions_ratings
