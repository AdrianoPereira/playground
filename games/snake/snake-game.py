import pygame
import random
# from pygame.locals import *


pygame.init()
pygame.display.set_caption("Adriano\'s Playground - Snake Game")

SIZE_WINDOW = (600, 600)
SIZE_BLOCK = (10, 10)
COLOR_SNAKE = (255, 255, 255)
COLOR_APPLE = (255, 0, 0)
COLOR_TEXT = (0, 255, 0)
COLOR_BKG = (0, 0, 0)
GRID_COLOR = (30, 30, 30)
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3


def generate_apple():
    def random_number():
        ans = random.randint(-10, 590)
        rem = ans%10
        return ans+10-rem

    x = random_number()
    y = random_number()
    return (x, y)


def eat_apple(snake, apple):
    return snake[0][0] == apple[0] and snake[0][1] == apple[1]


def detect_colision(snake):
    if snake[0][0] == SIZE_WINDOW[0] or snake[0][1] == SIZE_WINDOW[1]:
        return True
    if snake[0][0] < 0 or snake[0][1] < 0:
        return True

    for x in range(1, len(snake)-1):
        if snake[0][0] == snake[x][0] and snake[0][1] == snake[x][1]:
            return True
    return False


screen = pygame.display.set_mode(SIZE_WINDOW)

snake = [(200, 200), (210, 200), (220, 200)]
snake_sprite = pygame.Surface(SIZE_BLOCK)
snake_sprite.fill(COLOR_SNAKE)

apple_position = generate_apple()
# apple_sprite = pygame.Surface(SIZE_BLOCK)
apple_sprite = pygame.image.load("assets/apple.gif")
apple_sprite = pygame.transform.scale(apple_sprite, SIZE_BLOCK)
# apple_sprite.fill(COLOR_APPLE)
head_sprites = ["assets/head-up.png", "assets/head-right.png",
                "assets/head-down.png", "assets/head-left.png"]
body_sprites = ["assets/body-v.png", "assets/body-h.png"]

font = pygame.font.Font('freesansbold.ttf', 14)
score = 0

movement = LEFT
clock = pygame.time.Clock()
snapshot = 1
while True:
    clock.tick(10)
    pygame.image.save(screen, "snapshots/snake-%s.png"%(str(snapshot).zfill(5)))
    snapshot += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and movement is not DOWN:
                movement = UP
            if event.key == pygame.K_RIGHT and movement is not LEFT:
                movement = RIGHT
            if event.key == pygame.K_DOWN and movement is not UP:
                movement = DOWN
            if event.key == pygame.K_LEFT and movement is not RIGHT:
                movement = LEFT

    if eat_apple(snake, apple_position):
        apple_position = generate_apple()
        snake.append((0, 0))
        score += 1

    if detect_colision(snake):
        print('game over')

    for x in range(len(snake)-1, 0, -1):
        snake[x] =  (snake[x-1][0], snake[x-1][1])

    if movement == UP:
        snake[0] = (snake[0][0], snake[0][1]-10)
    if movement == RIGHT:
        snake[0] = (snake[0][0]+10, snake[0][1])
    if movement == DOWN:
        snake[0] = (snake[0][0], snake[0][1]+10)
    if movement == LEFT:
        snake[0] = (snake[0][0]-10, snake[0][1])

    screen.fill(COLOR_BKG)

    for x in range(0, 600, 10):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, 600))
        pygame.draw.line(screen, GRID_COLOR, (0, x), (600, x))
    score_text = font.render('Score: %s'%str(score).zfill(3), True, COLOR_TEXT)
    score_rect = score_text.get_rect()
    score_rect.topleft = (SIZE_WINDOW[0]-80, 10)
    screen.blit(score_text, score_rect)
    screen.blit(apple_sprite, apple_position)

    head_snake = pygame.image.load(head_sprites[movement])
    head_snake = pygame.transform.scale(head_snake, SIZE_BLOCK)
    screen.blit(head_snake, snake[0])
    body_snake = pygame.image.load(body_sprites[movement%2])
    body_snake = pygame.transform.scale(body_snake, SIZE_BLOCK)
    for pos in range(1, len(snake)):
        screen.blit(body_snake, snake[pos])

    pygame.display.update()
