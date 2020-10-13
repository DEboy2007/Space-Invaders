import pygame
import math
import random

playerSpeed = 5
distanceNeeded = 27
enemySpeed = 2
enemyDown = 40
bulletRespawn = 480
playerRespawn = 480

score = 0  # How many enemies have you got?
print("""WELCOME TO THIS GAME!!!
CONTROLS:
SPACE - SHOOT
LEFT ARROW - MOVE LEFT
RIGHT ARROW - MOVE RIGHT

DEFEAT THE ALIENS BEFORE THEY REACH YOU! ENJOY!""")
input("Click enter to play: ")
pygame.init()  # Necessary

screen = pygame.display.set_mode((800, 600))  # ((Width, Height))
# Background image
background = pygame.image.load("background.png")

# Title and Icon
pygame.display.set_caption("Space Invaders - By Dhanush Ekollu")  # Title
logo = pygame.image.load("Logo.png")  # Logo
pygame.display.set_icon(logo)
running = True

# Player
playerImg = pygame.image.load("Player.png")
playerX = 370
playerY = playerRespawn
playerX_change = 0

# Spawn many enemies
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load("Enemy.png"))
    EnemyX.append(random.randint(0, 730))  # Spawn at random X
    EnemyY.append(random.randint(50, 150))  # Spawn at random Y
    EnemyX_change.append(enemySpeed)  # Constantly move
    EnemyY_change.append(enemyDown)  # Whenever this is called, it goes down 40 pixels. Called when enemy hits boundary

# Bullet
BulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = bulletRespawn
bulletY_change = -10  # Constantly move upward
bullet_fired = False  # Has it been fired?


# Draw player
def player(x, y):
    screen.blit(playerImg, (int(x), int(y)))  # Draw player on screen. (Image, (x, y)). Needs to be int


# Draw enemy
def enemy(x, y, i):
    screen.blit(EnemyImg[i], (int(x), int(y)))


# Draw bullet
def fire_bullet(x, y):
    screen.blit(BulletImg, (int(x + 16), int(y + 10)))  # This is to make sure the bullet appears at the top of the ship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < distanceNeeded:
        return True
    else:
        return False


while running:  # Everything needs to happen in this loop
    screen.fill((0, 0, 0))  # RGB
    # Insert Background image
    screen.blit(background, (int(0), int(0)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Makes game quit when closed
            running = False
        # Control the player
        if event.type == pygame.KEYDOWN:  # When a key is pressed
            if event.key == pygame.K_LEFT:  # LEFT ARROW key (To move right)
                playerX_change = -playerSpeed  # Change position
            elif event.key == pygame.K_RIGHT:  # RIGHT ARROW key (To move left)
                playerX_change = playerSpeed
            # Otherwise bullet fired will move with ship when space pressed again:
            elif event.key == pygame.K_SPACE and not bullet_fired:
                bulletX = playerX  # Fire where the ship was when bullet fired, but don't follow the ship
                bullet_fired = True
        if event.type == pygame.KEYUP:  # Check when key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # Stop player

    playerX += playerX_change

    # So that the bullet stays on screen forever and so that the bullet won't be out of screen
    if bulletY <= 0:
        bullet_fired = False
        bulletY = bulletRespawn

    if bullet_fired:
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    # Do not allow to go beyond boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # Take into consideration size of image itself (64 pixels)
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):  # Each enemy
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = enemySpeed
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -enemySpeed  # Go the other way
            EnemyY[i] += EnemyY_change[i]  # Now make it go down

        # Check for collision
        collision = isCollision(EnemyX[i], EnemyY[i], bulletX, bulletY)
        if collision:
            bulletY = bulletRespawn
            bullet_fired = False
            score += 1
            EnemyX[i] = random.randint(0, 730)
            EnemyY[i] = random.randint(50, 150)
        enemy(EnemyX[i], EnemyY[i], i)

    player(playerX, playerY)  # This has to be after the screen.fill method because it is on top of it.
    pygame.display.update()  # Necessary
