# 2048 game implementation in Python using Pygame and NumPy libraries
import numpy as np
import pygame


# Define the Game2048 class
class Game2048():
    # Class variable to check if rendering is enabled
    rendering = False

    # Initialization method
    def __init__(self, state=None, pygame_enabled = True):
        self._pygame_enabled = pygame_enabled
        if self._pygame_enabled:
            pygame.init()  # Initialize Pygame
        if state is None:
            # Start a new game if no state is provided
            self.board, self.score = self.new_game()
        else:
            # Use the provided state
            board, score = state
            self.board, self.score = board.copy(), score

    @property
    def pygame_enabled(self):
        """Property to get pygame_enabled"""
        return self._pygame_enabled

    # Method to perform a game step based on action
    def step(self, action):
        # Move the tiles based on the action
        self.board, self.score = self.move(self.board, self.score, action)
        # Check if the game is over
        done = self.game_over(self.board)
        # Return the new state, score, and whether the game is done
        return ((self.board, self.score), self.score, done)

    # Method to render the game
    def render(self):
        if self._pygame_enabled:
            if not self.rendering:
                # Initialize rendering if it's not already initialized
                self.init_render()
                # Limit the frame rate to 30 fps
            self.clock.tick(30)
            # Clear the screen with a background color
            self.screen.fill((187, 173, 160))
            # Define colors for the tiles
            colors = [
                (205, 193, 180), (238, 228, 218), (237, 224, 200), (242, 177, 121),
                (245, 149, 99), (246, 124, 95), (246, 94, 69), (237, 204, 121),
                (237, 204, 97), (237, 197, 63), (121, 204, 237), (97, 177, 237),
                (63, 149, 204), (121, 121, 177), (40, 40, 80), (20, 20, 60)
            ]
            # Define tile border size
            border = 10
            # Draw the main game area background
            pygame.draw.rect(self.screen, (187, 173, 160), pygame.Rect(100, 0, 600, 600))
            # Draw each tile on the board
            for i in range(4):
                for j in range(4):
                    val = self.board[i][j]
                    # Calculate color index based on tile value
                    validx = int(np.log2(val)) if val > 0 else 0
                    # Draw the tile with the appropriate color
                    pygame.draw.rect(
                        self.screen, colors[validx % len(colors)],
                        pygame.Rect(100 + 150 * j + border, 150 * i + border, 150 - 2 * border, 150 - 2 * border)
                    )
                    if val > 0:
                        # Render the tile value as text
                        text = self.font.render("{:}".format(val), True, (255, 255, 255))
                        # Calculate the text position
                        x = 175 + 150 * j - text.get_width() / 2
                        y = 75 + 150 * i - text.get_height() / 2
                        self.screen.blit(text, (x, y))
            # Render the score
            text = self.scorefont.render("{:}".format(self.score), True, (0, 0, 0))
            self.screen.blit(text, (790 - text.get_width(), 10))
            # Update the display
            pygame.display.flip()

    # Method to reset the game
    def reset(self):
        self.board, self.score = self.new_game()

    # Method to close the game
    def close(self):
        if self._pygame_enabled:
            pygame.quit()

    # Method to initialize rendering properties
    def init_render(self):
        # Set up the game window
        self.screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption('2048')
        self.background = pygame.Surface(self.screen.get_size())
        self.rendering = True
        self.clock = pygame.time.Clock()
        # Set up fonts
        self.font = pygame.font.Font(None, 50)
        self.scorefont = pygame.font.Font(None, 30)

    # Method to find a random empty position on the board
    def random_empty_pos(self, board):
        i, j = np.where(board == 0)  # Find empty positions
        k = np.random.randint(len(i))  # Pick a random empty position
        return (i[k], j[k])

    # Method to check if the game is over
    def game_over(self, board):
        # Check if there are empty spaces
        if not np.all(board):
            return False
        # Check if any neighboring tiles can be merged
        for i in range(4):
            for j in range(3):
                if board[i, j] == board[i, j + 1] or board[j, i] == board[j + 1, i]:
                    return False
        return True

    # Method to compress tiles to the left
    def compress_left(self, board):
        for i in range(4):
            k = 0  # Pointer for the next non-zero position
            for j in range(4):
                if board[i, j]:  # If the tile is non-zero
                    board[i, k] = board[i, j]  # Move it to the next non-zero position
                    k += 1
            for j in range(k, 4):
                board[i, j] = 0  # Fill the rest with zeros
        return board


    # Method to move and merge tiles to the left
    def move_left(self, board, score):
        board = self.compress_left(board)  # Compress tiles to the left
        for i in range(4):
            for j in range(3):
                if board[i, j] == board[i, j + 1] and board[i, j] != 0:  # Merge adjacent tiles of the same value
                    board[i, j] *= 2
                    board[i, j + 1] = 0
                    score += board[i, j]  # Update score
        board = self.compress_left(board)  # Compress again after merging
        return (board, score)

    # Method to move tiles in a specified direction
    def move(self, board, score, direction='left'):
        # Save initial state of the board
        initial_board = board.copy()
        # Handle the move direction
        if direction == 'left':
            board, score = self.move_left(board, score)
        elif direction == 'right':
            board = board[:, ::-1]  # Reverse the board horizontally
            board, score = self.move_left(board, score)
            board = board[:, ::-1]  # Reverse back
        elif direction == 'up':
            board = board.T  # Transpose the board
            board, score = self.move_left(board, score)
            board = board.T  # Transpose back
        elif direction == 'down':
            board = board.T[:, ::-1]  # Reverse and transpose the board
            board, score = self.move_left(board, score)
            board = board[:, ::-1].T  # Reverse and transpose back
        # Add a new tile if the board has changed and there is space
        if not np.all(board) and np.any(board != initial_board):
            board[self.random_empty_pos(board)] = [2, 4][np.random.randint(2)]
        return (board, score)

    # Method to start a new game
    def new_game(self):
        board = np.zeros((4, 4), dtype=int)  # Initialize a 4x4 board with zeros
        for k in range(2):
            i, j = self.random_empty_pos(board)  # Get random empty position
            board[i, j] = 2  # Place a new tile
        score = 0  # Initialize score
        return (board, score)




