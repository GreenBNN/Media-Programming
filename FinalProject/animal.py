import pygame
import random
import os
from math import radians, sin, cos

# Initialize Pygame
pygame.init()

# Set up screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animal Clicker Game")

# Load the background image
bg_image = pygame.image.load("shmup/img/bg.jpg")

# Load the bomb image and heart image
bomb_image = pygame.image.load("shmup/img/bomb.png")
heart_image = pygame.image.load("shmup/img/heart.png")

# Load images and sounds
horse_image = pygame.image.load("shmup/img/horse.png")
sheep_image = pygame.image.load("shmup/img/sheep.png")
goat_image = pygame.image.load("shmup/img/goat.png")

s1_sound = pygame.mixer.Sound("shmup/snd/horse.wav")
s2_sound = pygame.mixer.Sound("shmup/snd/goat.wav")
s3_sound = pygame.mixer.Sound("shmup/snd/sheep.wav")

bullet_image = pygame.image.load("shmup/img/bullet.png")
reload_sound = pygame.mixer.Sound("shmup/snd/bullet.wav")

# Load bomb sound
bomb_sound = pygame.mixer.Sound("shmup/snd/bomb.wav")

lightBlue = (4, 27, 96)

last_bullet_time = pygame.time.get_ticks()

# Function to play sound and respawn image
def play_sound_and_respawn(image_rect, sound):
    sound.play()
    image_rect.reset()

# Function to handle bomb click
def handle_bomb_click(bomb_rect):
    global lives
    bomb_sound.play()  # Play bomb sound
    bomb_rect.reset()
    lives -= 1

# Function to respawn image at a random location
def respawn_image(image_rect):
    image_rect.x = random.randint(0, width - image_rect.width)
    image_rect.y = random.randint(0, height - image_rect.height)

# Function to move the image
def move(image_rect):
    direct = random.choice([-1, 0, 1])

    if direct == -1:
        image_rect.angle += -10
    elif direct == 0:
        image_rect.angle += 0
    else:
        image_rect.angle += 10

    image_rect.y += image_rect.speed * sin(radians(image_rect.angle))
    image_rect.x += image_rect.speed * cos(radians(image_rect.angle))

    if (image_rect.x + image_rect.width > width) or (image_rect.x < 0):
        if image_rect.y > height / 5:
            image_rect.x -= image_rect.speed * cos(radians(image_rect.angle))
        else:
            respawn_image(image_rect)
    if image_rect.y + image_rect.height < 0 or image_rect.y > height + 30:
        respawn_image(image_rect)

# Class for image properties
class ImageRect:
    def __init__(self, image):
        self.image = image
        self.width, self.height = image.get_size()
        self.reset()

    def reset(self):
        self.angle = random.randint(0, 360)
        self.speed = 5
        self.x = random.randint(0, width - self.width)
        self.y = random.randint(0, height - self.height)

def is_on_image(image_rect, pos):
    return (
        image_rect.x <= pos[0] <= image_rect.x + image_rect.width and
        image_rect.y <= pos[1] <= image_rect.y + image_rect.height
    )

def draw_bullets():
    for i in range(bullet_count):
        screen.blit(bullet_image, (10 + i * (bullet_image.get_width() + 5), height - 50))

def fire_bullet():
    global bullet_count, reloading, last_bullet_time

    if bullet_count > 0 and not reloading:
        current_time = pygame.time.get_ticks()

        # Add a delay of 300 milliseconds (0.3 seconds) before firing the next bullet
        if current_time - last_bullet_time >= 300:
            bullet_count -= 1
            last_bullet_time = current_time
            if bullet_count == 0:
                reload_bullets()
                draw_bullets()

            return True
    elif reloading:
        # If reloading, reset the reloading flag once the process is completed
        reloading = False

    return False

def reload_bullets():
    global bullet_count, reloading
    reloading = True
    bullet_count = 5
    reload_sound.play()

# Initialize image rectangles
horse_rect = ImageRect(horse_image)
sheep_rect = ImageRect(sheep_image)
goat_rect = ImageRect(goat_image)

# Additional image rectangles
image_rect4 = ImageRect(horse_image)
image_rect5 = ImageRect(sheep_image)
image_rect6 = ImageRect(goat_image)
image_rect7 = ImageRect(horse_image)

# Game loop
running = True
clock = pygame.time.Clock()

# Added code for score
score = 0
font = pygame.font.Font(None, 36)

# Initialize bomb rectangle
bomb_rect = ImageRect(bomb_image)

# Initialize bomb-related variables
bombs = []  # List to store multiple bombs
bomb_creation_timer = 0
bomb_creation_interval = 2000  # Time interval in milliseconds (5 seconds)
bomb_speed = 10  # Adjust this value to control bomb speed
# Initialize lives
lives = 3

# Initialize variables for speed increase
speed_increase_timer = 0
speed_increase_interval = 2000  # Time interval in milliseconds (5 seconds)
speed_increase_amount = 1  # Adjust this value to control the speed increase

# Initialize game state
GAME_RUNNING = 0
GAME_OVER = 1
game_state = GAME_RUNNING

# bullet
bullet_count = 5
reloading = False

# Inside the game loop
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Restart the game on any key press
                game_state = GAME_RUNNING
                lives = 3
                score = 0
                speed_increase_timer = 0
                bomb_creation_timer = 0
                bombs = []
                bullets = []
                for image_rect in [horse_rect, sheep_rect, goat_rect, image_rect4, image_rect5, image_rect6, image_rect7]:
                    image_rect.reset()

    if game_state == GAME_RUNNING:
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check for mouse click
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # bullet

        # Fire bullet on mouse click
        if mouse_click[0]:
            if fire_bullet():
                # Perform actions when a bullet is fired
                for image_rect, sound in zip(
                        [horse_rect, sheep_rect, goat_rect, image_rect4, image_rect5, image_rect6, image_rect7],
                        [s1_sound, s2_sound, s3_sound, s1_sound, s2_sound, s3_sound, s1_sound]
                ):
                    if is_on_image(image_rect, (mouse_x, mouse_y)):
                        play_sound_and_respawn(image_rect, sound)
                        score += 100


        # Draw bullets
        draw_bullets()

        # Check for reloading
        if reloading and pygame.time.get_ticks() % 1000 == 0:  # Adjust the reloading duration
            reloading = False


        # for image_rect, sound in zip(
        #     [horse_rect, sheep_rect, goat_rect, image_rect4, image_rect5, image_rect6, image_rect7],
        #     [s1_sound, s2_sound, s3_sound, s1_sound, s2_sound, s3_sound, s1_sound]
        # ):
        #     if image_rect.x <= mouse_x <= image_rect.x + image_rect.width and \
        #             image_rect.y <= mouse_y <= image_rect.y + image_rect.height and mouse_click[0]:
        #         play_sound_and_respawn(image_rect, sound)
        #         score += 100

        if bomb_rect.x <= mouse_x <= bomb_rect.x + bomb_rect.width and \
                bomb_rect.y <= mouse_y <= bomb_rect.y + bomb_rect.height and mouse_click[0]:
            handle_bomb_click(bomb_rect)

        for image_rect in [horse_rect, sheep_rect, goat_rect, image_rect4, image_rect5, image_rect6, image_rect7]:
            move(image_rect)
            screen.blit(image_rect.image, (image_rect.x, image_rect.y))

        # Draw custom cursor
        pos = pygame.mouse.get_pos()
        r = 20
        l = 15
        color = (255, 0, 0) if any(is_on_image(image_rect, pos) for image_rect in [horse_rect, sheep_rect, goat_rect, image_rect4, image_rect5, image_rect6, image_rect7]) else (0, 255, 0)

        pygame.draw.ellipse(screen, color, (pos[0] - r / 2, pos[1] - r / 2, r, r), 4)
        pygame.draw.line(screen, color, (pos[0], pos[1] - l / 2), (pos[0], pos[1] - l), 4)
        pygame.draw.line(screen, color, (pos[0] + l / 2, pos[1]), (pos[0] + l, pos[1]), 4)
        pygame.draw.line(screen, color, (pos[0], pos[1] + l / 2), (pos[0], pos[1] + l), 4)
        pygame.draw.line(screen, color, (pos[0] - l / 2, pos[1]), (pos[0] - l, pos[1]), 4)

    # Draw bombs and handle bomb clicks
        for bomb_rect in bombs:
            move(bomb_rect)
            screen.blit(bomb_rect.image, (bomb_rect.x, bomb_rect.y))
            if is_on_image(bomb_rect, pygame.mouse.get_pos()) and mouse_click[0]:
                handle_bomb_click(bomb_rect)

        # Check bomb creation timer and create a new bomb
        bomb_creation_timer += clock.get_time()
        if bomb_creation_timer >= bomb_creation_interval:
            new_bomb = ImageRect(bomb_image)
            respawn_image(new_bomb)
            bombs.append(new_bomb)
            bomb_creation_timer = 0  # Move this line outside the if block

        # Check speed increase timer and increase speed
        speed_increase_timer += clock.get_time()*2
        if speed_increase_timer >= speed_increase_interval:
            for image_rect in [horse_rect, sheep_rect, goat_rect, image_rect4, image_rect5, image_rect6, image_rect7]:
                image_rect.speed += speed_increase_amount
            speed_increase_timer = 0
            bomb_speed += 1

        # Draw lives in the upper left corner
        heart_spacing = 5  # Adjust this value to control the spacing between hearts
        for i in range(lives):
            screen.blit(heart_image, (10 + i * (heart_image.get_width() + heart_spacing), 10))

        # Draw score in the upper right corner
        score_text = font.render("Score: {}".format(score), True, (0, 0, 0))
        screen.blit(score_text, (width - score_text.get_width() - 10, 10))

        pygame.display.flip()
        clock.tick(30)


        # Check for game over
        if lives == 0:
            game_state = GAME_OVER

    elif game_state == GAME_OVER:
        screen.fill((255, 255, 255))

        # Display "Game Over!" text
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, ((width - game_over_text.get_width()) // 2, (height - game_over_text.get_height()) // 2))

        # Display "Press any key to restart" text
        restart_text = font.render("Press any key to restart", True, (0, 0, 0))
        screen.blit(restart_text, ((width - restart_text.get_width()) // 2, (height + game_over_text.get_height()) // 2))



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
