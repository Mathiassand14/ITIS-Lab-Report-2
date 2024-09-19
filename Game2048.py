# 2048 game

# Import libraries used for this program
 
import pygame
import numpy as np

#%%

class Game2048():    
    # Rendering?
    rendering = False

    
    def __init__(self, state=None):
        pygame.init()
        if state is None:
            self.board, self.score = self.new_game()
        else:
            board, score = state
            self.board, self.score = board.copy(), score

            
    def step(self, action):
        self.board, self.score = self.move(self.board, self.score, action)

        # return observation, reward, done
        done = self.game_over(self.board)        
        return ((self.board, self.score), self.score, done)
        
    def render(self):
        if not self.rendering:
            self.init_render()
            
        # Limit to 30 fps
        self.clock.tick(30)
     
        # Clear the screen
        self.screen.fill((187,173,160))
        
        # Draw board
        colors = [(205,193,180), (238,228,218), (237,224,200), (242,177,121), 
                  (245,149,99), (246,124,95), (246,94,69), (237,204,121), 
                  (237,204,97), (237,197,63), (121,204,237), (97,177,237), 
                  (63,149,204), (121,121,177), (40,40,80), (20,20,60)]
        
        border = 10
        pygame.draw.rect(self.screen, (187,173,160), pygame.Rect(100,0,600,600))
        for i in range(4):
            for j in range(4):
                val = self.board[i][j]
                validx = int(np.log2(val)) if val>0 else 0
                pygame.draw.rect(self.screen, colors[validx % len(colors)], pygame.Rect(100+150*j+border,150*i+border,150-2*border,150-2*border))
                if val>0:
                    text = self.font.render("{:}".format(val), True, (255,255,255))                
                    x = 175 + 150*j - text.get_width()/2
                    y = 75 + 150*i - text.get_height()/2                
                    self.screen.blit(text, (x, y))
        text = self.scorefont.render("{:}".format(self.score), True, (0,0,0))
        self.screen.blit(text, (790-text.get_width(), 10))

        # Display
        pygame.display.flip()

    def reset(self):
        self.board, self.score = self.new_game()

    def close(self):
        pygame.quit()
                 
    def init_render(self):
        self.screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption('2048')
        self.background = pygame.Surface(self.screen.get_size())
        self.rendering = True
        self.clock = pygame.time.Clock()

        # Set up game
        self.font = pygame.font.Font(None, 50)
        self.scorefont = pygame.font.Font(None, 30)
           
    def random_empty_pos(self, board):
        i, j = np.where(board==0)    
        k = np.random.randint(len(i))
        return (i[k], j[k])
    
    def game_over(self, board):
        # Space left on board?
        if not np.all(board):
            return False
        # Any neighbors that can be merged?
        for i in range(4):
            for j in range(3):
                if board[i,j]==board[i,j+1] or board[j,i]==board[j+1,i]:
                    return False
        return True
    
    def compress_left(self, board):
        for i in range(4):
            k = 0
            for j in range(4):
                if board[i,j]:
                    board[i,k] = board[i,j]
                    k += 1
            for j in range(k, 4):
                board[i,j] = 0       
        return board
    
    def move_left(self, board, score):
        # Remove zeros        
        board = self.compress_left(board)
        
        # Combine adjacent values (replace second val by zero)
        for i in range(4):
            for j in range(3):
                if board[i,j]==board[i,j+1] and board[i,j] != 0:
                    board[i,j] *= 2                    
                    board[i,j+1] = 0
                    score += board[i,j]
        # Remove zeros                    
        board = self.compress_left(board)    
        
        return (board, score)
    
    def move(self, board, score, direction='left'):
        # Save initial board
        initial_board = board.copy()
    
        # Rotate board, move left, rotate back
        if direction=='left':
            board, score = self.move_left(board, score)
        elif direction=='right':
            board = board[:,::-1]
            board, score = self.move_left(board, score)
            board = board[:,::-1]
        elif direction=='up':
            board = board.T
            board, score = self.move_left(board, score)
            board = board.T
        elif direction=='down':
            board = board.T[:,::-1]
            board, score = self.move_left(board, score)
            board = board[:,::-1].T
    
        # Add new 2 or 4 at random pos (if board has changed and there is space)
        if not np.all(board) and np.any(board != initial_board):
            board[self.random_empty_pos(board)] = [2,4][np.random.randint(2)]       
            
        return (board, score)
       
    def new_game(self):
        board = np.zeros((4, 4), dtype=int)
        for k in range(2):
            i, j = self.random_empty_pos(board)
            board[i,j] = 2
        score = 0
        return (board, score)


