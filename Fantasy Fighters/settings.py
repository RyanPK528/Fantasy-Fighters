import pygame

# Window settings 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
GAME_NAME = "Fantasy Fighters"

# FPS
FPS = 60

# Color settings
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game function variables
SPEED = 10 # movement value (move by 10px)
GRAVITY = 2 # movement value (move down by 2px)
intro_count = 4 # 4s countdown before each round
last_count_update = pygame.time.get_ticks() 
score = [0, 0] # [P1, P2]
round_over = False
round_over_cooldown = 2000 # 2s
winner = 0 # Player who won
wins_required = 3

# Fighter variables
WARRIOR_SIZE = 126
WARRIOR_SCALE = 3
WARRIOR_OFFSET = [60, 20]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
SAMURAI_SIZE = 200
SAMURAI_SCALE = 3
SAMURAI_OFFSET = [80, 60]
SAMURAI_DATA = [SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSET]

# Number of frames in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 3, 7, 9, 3, 11]
SAMURAI_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]