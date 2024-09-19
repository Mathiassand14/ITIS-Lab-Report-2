# Game 2048: Artificial intelligence

# Instructions:
#   Move up, down, left, or right to merge the tiles. The objective is to 
#   get a tile with the number 2048 (or higher)
#
# Control:
#    arrows  : Merge up, down, left, or right
#    r       : Restart game
#    q / ESC : Quit

from Game2048 import Game2048
import numpy as np
import pygame

env = Game2048()
env.reset()
actions = ['left', 'right', 'up', 'down']
exit_program = False
action_taken = False
while not exit_program:
    env.render()

    # Process game events
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
    # can see below, the code only steps the envirionment when action_taken 
    # is True, since the whole game runs in an infinite loop.
    

    # END OF YOUR CODE
    
    if action_taken:
        (board, score), reward, done = env.step(action)
        action_taken = False

env.close()
