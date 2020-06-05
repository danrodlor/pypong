import random
import pygame
from pygame.locals import *

# TODO:
# - direction string variables can be avoided using xspeed and yspeed with positive and negative values, so that no check is needed
# - add angles to ball bounce
# - redesign the controller interface..., add a function to get the action: MB the class has to implement Controllable abstract class

class Ball(pygame.sprite.Sprite):

    def __init__(self, size, x, y, speed, board, bounce_sound=None, hit_sound=None):
        super().__init__()
        self.size = size
        self.image = pygame.Surface([size, size])
        self.image.fill(pygame.Color('white'))
        self.rect = self.image.get_rect(center=(x, y))
        self.initial_speed = speed
        self.xspeed = speed
        self.yspeed = speed
        self.board = board
        self.board_rect = self.board.get_rect()
        self.xdirection = random.choice(['rigth', 'left'])
        self.ydirection = random.choice(['up', 'down'])
        self.bounce_sound = bounce_sound
        self.hit_sound = hit_sound

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, x):
        self.rect.x = x

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, y):
        self.rect.y = y

    def _check_board_boundaries(self):
        if self.y >= self.board_rect.height - self.size:
            self.ydirection = 'up'
            self.bounce_sound.play()
        elif self.y <= 0:
            self.ydirection = 'down'
            self.bounce_sound.play()

    def reset(self):
        self.rect.center = self.board_rect.center
        self.xdirection = random.choice(['rigth', 'left'])
        self.ydirection = random.choice(['up', 'down'])
        self.xspeed = self.initial_speed
        self.yspeed = self.initial_speed

    def process_collision(self, entity):
        if (self.rect.right >= entity.rect.left) or (self.rect.left <= entity.rect.right):
            # FIXME: Complete this to bounce with angle depending on where they collide
            #bounce_angle = (entity.rect.centery - self.rect.centery)/entity.height
            if self.xdirection == 'rigth':
                self.xdirection = 'left'
                self.rect.right = entity.rect.left - self.xspeed
            elif self.xdirection == 'left':
                self.xdirection = 'rigth'
                self.rect.left = entity.rect.right + self.xspeed

            self.xspeed += 0.5
            self.yspeed += 0.5

            self.hit_sound.play()

    def update(self):
        self._check_board_boundaries()

        if self.xdirection == 'left':
            self.x -= self.xspeed
        elif self.xdirection == 'rigth':
            self.x += self.xspeed

        if self.ydirection == 'down':
            self.y += self.yspeed
        elif self.ydirection == 'up':
            self.y -= self.yspeed

    def draw(self):
        self.board.blit(self.image, self.rect)

class Paddle(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y, speed, board, controller):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color('white'))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.board = board
        self.board_rect = board.get_rect()
        self.controller = controller
        self.action = controller.action

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, x):
        self.rect.x = x

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, y):
        self.rect.y = y

    def reset(self):
        self.rect.centery = self.board_rect.centery

    def update(self):
        self.action = self.controller.action

        if self.action == 'stop':
            pass
        elif self.action == 'up':
            self.y -= self.speed
        elif self.action == 'down':
            self.y += self.speed

        self.rect.clamp_ip(self.board_rect)

    def draw(self):
        self.board.blit(self.image, self.rect)
