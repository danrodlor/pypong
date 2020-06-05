import pygame
from pygame.locals import *

# TODO:
# 1) InputController: user input handler
# 2) AIController: enemy controller - AI based
# IDEAS: Would be better to write a Controller abstract class definning a standarized way to access
# to the controller methods and variables and inherit from it? Maybe not and I can just write and input controller
# that drives the player based on an variable "device" whose value can be "keyboard"/"mouse"/"joystick"

class InputController():
    def __init__(self):
        self.action = 'stop'

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.action = 'down'
            elif event.key == pygame.K_UP:
                self.action = 'up'
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                if self.action == 'down':
                    self.action = 'stop'
            elif event.key == pygame.K_UP:
                if self.action == 'up':
                    self.action = 'stop'

# FIXME: This should go in another file, as well as the rest of the possible AI controllers...
class AIController():
    def __init__(self, game):
        self.action = 'stop'
        self.game = game

    def update(self):
        if self.game.ball.rect.centerx >= self.game.screen_rect.centerx:
            if self.game.enemy.rect.centery > self.game.ball.rect.centery:
                self.action = 'up'
            elif self.game.enemy.rect.centery < self.game.ball.rect.centery:
                self.action = 'down'
            else:
                self.action = 'stop'
        else:
            if self.game.enemy.rect.centery > self.game.screen_rect.centery + self.game.enemy.speed:
                self.action = 'up'
            elif self.game.enemy.rect.centery < self.game.screen_rect.centery - self.game.enemy.speed:
                self.action = 'down'
            else:
                self.action = 'stop'
