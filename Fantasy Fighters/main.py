# Modules used for the game
import pygame
from pygame import mixer
from settings import *
from fighter import Fighter

mixer.init()
pygame.init()

# Function to initialize the game
def initialize_game():
    # Window settings
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_NAME)

    clock = pygame.time.Clock()
    
    return screen, clock

# Function to load the game assets
def load_assets():
    # In-game audio
    pygame.mixer.music.load("assets/audio/music.wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1, 0.0, 5000)
    sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
    sword_fx.set_volume(0.1)

    # Background image
    bg_image = pygame.image.load("assets/images/background/background_stage.png").convert_alpha()

    # Load fighter spritesheets
    warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
    samurai_sheet = pygame.image.load("assets/images/samurai/Sprites/samurai.png").convert_alpha()

    return bg_image, warrior_sheet, samurai_sheet, sword_fx

# Function to wait for a key press
def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Function to display the main menu
def main_menu():
    screen.fill(BLACK)
    draw_text("Press ENTER to start", count_font, WHITE, 120, 250)
    pygame.display.update()
    wait_for_key() # Start the game after pressing 'ENTER'

# Function to display the game-over screen
def game_over():
    screen.fill(BLACK)
    draw_text("GAME OVER", count_font, WHITE, 325, 250)
    pygame.display.update()
    pygame.time.delay(2000)  # Display for 2 seconds
    main_menu()  # Go back to the main menu

# Function to draw text in the game
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Function to draw background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Adjust image proportions to fit in window
    screen.blit(scaled_bg, (0, 0))

# Function to draw fighter's health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, 408, 38)) # Shadow border 
    pygame.draw.rect(screen, RED, (x, y, 400, 30)) # Health loss
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30)) # Health left


# Initialize game
screen, clock = initialize_game()

# Load assets
bg_image, warrior_sheet, samurai_sheet, sword_fx = load_assets()

# Set text font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Main menu loop
main_menu()

# Create two instances of fighters
fighter_1 = Fighter(1, 200, 350, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 350, True, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS, sword_fx)

# Game loop
run = True
while run:
    clock.tick(FPS)

    # Draw background
    draw_bg()

    # Show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("Player 1: " + str(score[0]), score_font, WHITE, 20, 60)
    draw_text("Player 2: " + str(score[1]), score_font, WHITE, 580, 60)

    # Update countdown
    if intro_count <= 0:
        # Move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # Display count timer
        draw_text(str(intro_count), count_font, YELLOW, 480, 230)
        # Update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # Update fighters
    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            winner += 2
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            winner += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        
    else:
        # Display victory image
        draw_text(f"PLAYER {winner} WINS", count_font, YELLOW, 280, 200)
        if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
            round_over = False
            winner = 0
            intro_count = 4
            fighter_1 = Fighter(1, 200, 350, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 700, 350, True, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS, sword_fx)

    # Check for game over
    if score[0] >= wins_required and round_over == False or score[1] >= wins_required and round_over == False:
        # Display game over screen
        game_over()
        # Reset scores and fighters
        score = [0, 0]
        fighter_1 = Fighter(1, 200, 350, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
        fighter_2 = Fighter(2, 700, 350, True, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS, sword_fx)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update display
    pygame.display.update()

# Exit pygame
pygame.quit()
