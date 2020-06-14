import config
import random
import pygame
from math import sin
from pygame.locals import *

# TODO:
# - redesign the controller interface..., add a function to get the action: MB the class has to implement Controllable abstract class

class Ball(pygame.sprite.Sprite):

    def __init__(self, size, x, y, speed, board, bounce_sound=None, hit_sound=None):
        super().__init__()
        self.size = size
        self.image = pygame.Surface([size, size])
        self.image.fill(pygame.Color('white'))
        self.rect = self.image.get_rect(center=(x, y))
        self.initial_speed = speed
        self.xspeed = random.choice([speed, -speed])
        self.yspeed = random.choice([speed, -speed])
        self.board = board
        self.board_rect = self.board.get_rect()
        self.fx = float(self.rect.x)
        self.fy = float(self.rect.y)
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
        if self.fy >= (self.board_rect.height - self.size) or self.fy <= 0:
            self.yspeed = -self.yspeed
            self.bounce_sound.play()

    def reset(self):
        self.rect.center = self.board_rect.center
        self.fx = self.rect.x
        self.fy = self.rect.y
        self.xspeed = random.choice([self.initial_speed, -self.initial_speed])
        self.yspeed = random.choice([self.initial_speed, -self.initial_speed])

    def process_collision(self, entity):
        if (self.rect.right >= entity.rect.left) or (self.rect.left <= entity.rect.right):

            if self.xspeed < 0:
                self.fx = entity.rect.right
            else:
                self.fx = entity.rect.left - self.size

            offset = (entity.rect.centery - self.rect.centery)
            normalized_offset = offset / (0.5 * (entity.height + self.size))
            bounce_angle = config.MAX_BOUNCING_ANGLE * normalized_offset

            self.xspeed = -self.xspeed
            self.yspeed = self.initial_speed * -sin(bounce_angle)

            self.hit_sound.play()

    def update(self):
        self._check_board_boundaries()
        self.fx += self.xspeed
        self.fy += self.yspeed
        self.x = round(self.fx)
        self.y = round(self.fy)

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
