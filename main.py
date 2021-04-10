import random
import time
import pygame
from pygame.locals import *

rgb = (71, 25, 25)
SIZE = 40


class Fruit:
    def __init__(self, parent_surface):
        self.Fruit = pygame.image.load('Apple2.jpg').convert()
        self.parent_surface = parent_surface
        self.x = random.randint(1, 25) * SIZE
        self.y = random.randint(1, 19) * SIZE

    def draw(self):
        self.parent_surface.blit(self.Fruit, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 25) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, parent_surface, length):
        self.block = pygame.image.load('Block.jpg').convert()
        self.parent_surface = parent_surface
        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.dir = "None"

    def draw(self):
        self.parent_surface.fill(rgb)
        for i in range(self.length):
            self.parent_surface.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        if self.x[0] > 1040:
            self.x[0] = 0
        if self.x[0] < 0:
            self.x[0] = 1040
        if self.y[0] > 760:
            self.y[0] = 0
        if self.y[0] < 0:
            self.y[0] = 760
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.dir == "UP":
            self.y[0] -= SIZE
        elif self.dir == "DOWN":
            self.y[0] += SIZE
        elif self.dir == "LEFT":
            self.x[0] -= SIZE
        elif self.dir == "RIGHT":
            self.x[0] += SIZE
        self.draw()

    def up(self):
        self.dir = "UP"

    def down(self):
        self.dir = "DOWN"

    def left(self):
        self.dir = "LEFT"

    def right(self):
        self.dir = "RIGHT"


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("Background.mp3")
        pygame.mixer.music.play()
        self.surface = pygame.display.set_mode((1080, 800))
        self.surface.fill(rgb)
        pygame.display.flip()
        self.Snake = Snake(self.surface, 1)
        self.Snake.draw()
        self.Fruit = Fruit(self.surface)
        self.Fruit.draw()
        self.running = True
        self.pause = False

    def collision(self):
        if self.Fruit.x == self.Snake.x[0] and self.Fruit.y == self.Snake.y[0]:
            sound = pygame.mixer.Sound('Eat.mp3')
            pygame.mixer.Sound.play(sound)
            return True
        else:
            return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render("Score : {0}".format(self.Snake.length - 1), True, (255, 255, 255))
        self.surface.blit(score, (900, 10))
        pygame.display.flip()

    def check_game_over(self):
        for i in range(1, self.Snake.length):
            if self.Snake.x[0] == self.Snake.x[i] and self.Snake.y[0] == self.Snake.y[i]:
                sound = pygame.mixer.Sound('Crash.mp3')
                pygame.mixer.Sound.play(sound)
                pygame.mixer.music.pause()
                self.pause = True

    def gameover(self):
        self.surface.fill(rgb)
        font = pygame.font.SysFont('arial', 30)
        score = font.render("Game Over!!   Score : {0}".format(self.Snake.length - 1), True, (255, 255, 255))
        msg = font.render("'ESC' To Exit    'Enter' To Play Again", True, (255, 255, 0))
        self.surface.blit(score, (340, 350))
        self.surface.blit(msg, (300, 400))
        pygame.display.flip()

    def play(self):
        self.Snake.walk()
        self.Fruit.draw()
        self.display_score()
        self.check_game_over()
        if self.collision():
            self.Snake.length += 1
            self.Snake.x.append(0)
            self.Snake.y.append(0)
            self.Fruit.move()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_UP:
                        self.Snake.up()
                    if event.key == K_DOWN:
                        self.Snake.down()
                    if event.key == K_LEFT:
                        self.Snake.left()
                    if event.key == K_RIGHT:
                        self.Snake.right()
                    if event.key == K_RETURN:
                        self.pause = False
                        self.Snake.length = 1
                        self.Snake.dir = "None"
                        pygame.mixer.music.play()
                elif event.type == QUIT:
                    self.running = False
            time.sleep(0.2)
            if not self.pause:
                self.play()
            else:
                self.gameover()


if __name__ == "__main__":
    game = Game()
    game.run()
