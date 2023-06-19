import pygame
import random

# Paramètres du jeu
SNAKE_SPEED = 15
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
SNAKE_WIDTH = 40
APPLE_IMAGE = pygame.image.load('pomelos.png')
APPLE_IMAGE = pygame.transform.scale(APPLE_IMAGE, (SNAKE_WIDTH + 50, SNAKE_WIDTH + 50))

# Initialisation de Pygame
pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Le serpent est une liste de carrés
snake = [pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, SNAKE_WIDTH, SNAKE_WIDTH)]
direction = 'right'


# Fonction pour dessiner le serpent
def draw_snake():
    for segment in snake:
        pygame.draw.rect(win, (0, 255, 0), segment)


# Boucle principale du jeu
def game_loop():
    global direction
    apple = pygame.Rect(random.randint(0, WINDOW_WIDTH - SNAKE_WIDTH), random.randint(0, WINDOW_HEIGHT - SNAKE_WIDTH),
                        SNAKE_WIDTH, SNAKE_WIDTH)
    clock = pygame.time.Clock()
    score = 0
    speed = SNAKE_SPEED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                elif event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'

        # Fait bouger le serpent
        if direction == 'up':
            snake.insert(0, snake[0].copy())
            snake[0].y -= SNAKE_WIDTH
        elif direction == 'down':
            snake.insert(0, snake[0].copy())
            snake[0].y += SNAKE_WIDTH
        elif direction == 'left':
            snake.insert(0, snake[0].copy())
            snake[0].x -= SNAKE_WIDTH
        elif direction == 'right':
            snake.insert(0, snake[0].copy())
            snake[0].x += SNAKE_WIDTH

        # Vérifie si le serpent a mangé la pomme
        if snake[0].colliderect(apple):
            score += 1
            speed += 0.1
            apple.topleft = (
                random.randint(0, WINDOW_WIDTH - SNAKE_WIDTH), random.randint(0, WINDOW_HEIGHT - SNAKE_WIDTH))
        else:
            snake.pop()

        # Si le serpent sort de l'écran, il apparait de l'autre côté
        if snake[0].x >= WINDOW_WIDTH:
            snake[0].x = 0
        if snake[0].x < 0:
            snake[0].x = WINDOW_WIDTH - SNAKE_WIDTH
        if snake[0].y >= WINDOW_HEIGHT:
            snake[0].y = 0
        if snake[0].y < 0:
            snake[0].y = WINDOW_HEIGHT - SNAKE_WIDTH

        # Dessine le serpent et la pomme
        win.fill((0, 0, 0))
        draw_snake()
        win.blit(APPLE_IMAGE, apple.center)
        pygame.display.update()

        # Gère la vitesse du serpent
        clock.tick(speed)


game_loop()
pygame.quit()
