import pygame
import random
import sys

pygame.init()
width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

block_size = 20

font_style = pygame.font.SysFont(None, 50)


class Snake:
    def __init__(self):
        self.size = 1
        self.elements = [[100, 100]]
        self.direction = "right"
        self.food_x = 0
        self.food_y = 0

    def draw(self):
        for i, element in enumerate(self.elements):
            if i == 0:
                block_size = 20
            elif i == len(self.elements) - 1:
                block_size = 15
            else:
                block_size = 10
            pygame.draw.rect(win, white, [element[0], element[1], block_size, block_size])

    def move(self):
        for i in range(len(self.elements) - 1, 0, -1):
            self.elements[i] = self.elements[i - 1][:]

        if self.direction == "right":
            self.elements[0][0] += block_size
        elif self.direction == "left":
            self.elements[0][0] -= block_size
        elif self.direction == "up":
            self.elements[0][1] -= block_size
        elif self.direction == "down":
            self.elements[0][1] += block_size

    def check_collision(self):
        if self.elements[0][0] >= width or self.elements[0][0] < 0 or self.elements[0][1] >= height or self.elements[0][
            1] < 0:
            return 1
        for i in range(1, len(self.elements)):
            if self.elements[i][0] == self.elements[0][0] and self.elements[i][1] == self.elements[0][1]:
                return 1
        return 0

    def check_food(self, score, speed):
        if self.elements[0][0] == self.food_x and self.elements[0][1] == self.food_y:
            self.size += 1
            self.food_x = 0
            self.food_y = 0
            score += 1
            speed += 1
        return score, speed

    def create_food(self):
        if self.food_x == 0 and self.food_y == 0:
            self.food_x = (block_size * (random.randint(1, (width // block_size) - 1)))
            self.food_y = (block_size * (random.randint(1, (height // block_size) - 1)))
        pygame.draw.rect(win, red, [self.food_x, self.food_y, block_size, block_size])


def display_score(score):
    score_text = font_style.render("Score: " + str(score), True, white)
    win.blit(score_text, [0, 0])


# Main loop
snake = Snake()
clock = pygame.time.Clock()
score = 0

speed = 10

while True:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = "up"
            elif event.key == pygame.K_DOWN:
                snake.direction = "down"
            elif event.key == pygame.K_LEFT:
                snake.direction = "left"
            elif event.key == pygame.K_RIGHT:
                snake.direction = "right"
    win.fill(black)
    snake.move()
    snake.draw()
    snake.create_food()
    score, speed = snake.check_food(score, speed)
    if snake.check_collision() == 1:
        pygame.quit()
        sys.exit()
    display_score(score)
    pygame.display.update()
