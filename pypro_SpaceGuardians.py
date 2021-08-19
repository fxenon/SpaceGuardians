import pygame
import random
import math
from pygame import mixer

pygame.init()

# creating screen 980px x 540px
game_screen = pygame.display.set_mode((980, 540))

# adding background music
mixer.music.load('migi theme.wav')
mixer.music.play(-1)

# adding background image and icon image
background = pygame.image.load('bg1.png')
pygame.display.set_caption('Space Guardians')
game_icon = pygame.image.load('icon.png')
pygame.display.set_icon(game_icon)

# adding player character and its position
player_avatar = pygame.image.load('spaceship2_64x.png')
playerX_coordinate = 460
playerY_coordinate = 460
playerX_coordinate_change = 0
playerY_coordinate_change = 0

# creating and storing enemies positions and list
enemy_avatar = []
enemyX_coordinate = []
enemyY_coordinate = []
enemyX_coordinate_change = []
enemyY_coordinate_change = []
num_of_enemies = 7

# adding enemies to play field
for i in range(num_of_enemies):
    enemy_avatar.append(pygame.image.load(f'enemy ({random.randint(1, 7)}).png'))
    enemyX_coordinate.append(random.randint(0, 980))
    enemyY_coordinate.append(random.randint(0, 60))
    enemyX_coordinate_change.append(1.5)
    enemyY_coordinate_change.append(0)

# adding ammunition
laser1 = pygame.image.load('laser24x.png')
laser2 = pygame.image.load('laser24x.png')
laserX_coordinate = playerX_coordinate
laserY_coordinate = playerY_coordinate
laserX_coordinate_change = 0
laserY_coordinate_change = 16
ammunition_loaded = 'loaded'

# initializing score and adding it to screen
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 24)
scoreX_coordinate = 15
scoreY_coordinate = 10

# placing game over text
game_over_text = pygame.font.Font('freesansbold.ttf', 64)
game_overX_coordinate = 315
game_overY_coordinate = 220


# func for placing score on screen
def show_score(x, y):
    score = score_font.render('Score: ' + str(score_value), True, (225, 225, 225))
    game_screen.blit(score, (x, y))


# func for placing game over text on screen
def game_over(x, y):
    game_end = game_over_text.render('Game Over', True, (255, 255, 255))
    game_screen.blit(game_end, (x, y))


# adding player character to screen
def player(x, y):
    game_screen.blit(player_avatar, (round(x), round(y)))


# adding enemies to screen
def enemy(x, y, e_num):
    game_screen.blit(enemy_avatar[e_num], (round(x), round(y)))


# function for placing bullets and aligning it with the character by adding values in x and y coordinates
def fire_bullet(x, y):
    global ammunition_loaded
    ammunition_loaded = 'fire'
    game_screen.blit(laser1, (round(x + 18), round(y + 15)))
    game_screen.blit(laser2, (round(x + 71), round(y + 15)))


# function for calculating distance between bullets and enemies to check collision
def is_collision(e_x, e_y, b_x, b_y):
    distance = (math.sqrt(math.pow(e_x - b_x, 2)) + (math.pow(e_y - b_y, 2)))
    if distance < 60:
        return True
    else:
        return False


running = True
while running:
    # RGB value for bg
    game_screen.fill((5, 9, 3))
    game_screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_coordinate_change = -2.5
            if event.key == pygame.K_DOWN:
                playerY_coordinate_change = 2.5
            if event.key == pygame.K_LEFT:
                playerX_coordinate_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_coordinate_change = 3
            if event.key == pygame.K_SPACE:
                if ammunition_loaded == 'loaded':
                    bullet_sound = mixer.Sound('laser sound.wav')
                    bullet_sound.play()
                    laserX_coordinate = playerX_coordinate - 25
                    fire_bullet(laserX_coordinate, laserY_coordinate)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_coordinate_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_coordinate_change = 0

    playerX_coordinate += playerX_coordinate_change
    playerY_coordinate += playerY_coordinate_change

    # constraining player inside screen
    if playerX_coordinate <= 0:
        playerX_coordinate = 0
    elif playerX_coordinate >= 916:
        playerX_coordinate = 916
    if playerY_coordinate <= 0:
        playerY_coordinate = 0
    elif playerY_coordinate >= 476:
        playerY_coordinate = 476

    # constraining enemies inside screen
    for i in range(num_of_enemies):
        if enemyY_coordinate[i] > 520:
            for j in range(num_of_enemies):
                enemyY_coordinate[j] = 2000
            game_over(game_overX_coordinate, game_overY_coordinate)
            break

        # changing position of enemies
        enemyX_coordinate[i] += enemyX_coordinate_change[i]
        enemyY_coordinate[i] += enemyY_coordinate_change[i]
        if enemyX_coordinate[i] >= 916:
            enemyX_coordinate_change[i] = -1.4
            enemyY_coordinate_change[i] = 0.05
        elif enemyX_coordinate[i] <= 0:
            enemyX_coordinate_change[i] = 1.4
            enemyY_coordinate_change[i] = 0.05

        # creating collision engine
        collision = is_collision(enemyX_coordinate[i], enemyY_coordinate[i], laserX_coordinate, laserY_coordinate)
        if collision:
            collision_sound = mixer.Sound('collision.wav')
            collision_sound.play()
            laserY_coordinate = playerY_coordinate
            ammunition_loaded = 'loaded'
            score_value += 1
            enemyX_coordinate[i] = random.randint(0, 980)
            enemyY_coordinate[i] = random.randint(random.randint(0, 20), random.randint(21, 110))

        enemy(enemyX_coordinate[i], enemyY_coordinate[i], i)

    # checking if bullet have reached to 0 in y axis and then calling it back to player position
    if laserY_coordinate <= 0:
        laserY_coordinate = playerY_coordinate - 15
        ammunition_loaded = 'loaded'
    if ammunition_loaded == 'fire':
        fire_bullet(laserX_coordinate, laserY_coordinate)
        laserY_coordinate -= laserY_coordinate_change

    player(playerX_coordinate, playerY_coordinate)
    show_score(scoreX_coordinate, scoreY_coordinate)
    # updating game to process and update game for each change made trough out the game
    pygame.display.update()
