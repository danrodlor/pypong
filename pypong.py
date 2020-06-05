import os
import sys
import config
import pygame
from pygame.locals import *
from loader import ResourceLoader
from states import (GameStateManager, GameMainMenuState, GameOptionsMenuState,
                    GamePauseMenuState, GameRunningState, GameLoseScreenState,
                    GameWinScreenState, GameCountdownState, GameSaveMenuState,
                    GameLoadMenuState)

if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
    SCREEN = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    RESOURCE_LOADER = ResourceLoader(config.RESOURCES_BASE_PATH)
    STATES = {'MAIN_MENU_STATE': GameMainMenuState(SCREEN, RESOURCE_LOADER),
              'OPTIONS_MENU_STATE': GameOptionsMenuState(SCREEN, RESOURCE_LOADER),
              'PAUSE_MENU_STATE': GamePauseMenuState(SCREEN, RESOURCE_LOADER),
              'GAME_COUNTDOWN_STATE': GameCountdownState(SCREEN, RESOURCE_LOADER),
              'GAME_RUNNING_STATE': GameRunningState(SCREEN, RESOURCE_LOADER),
              'GAME_LOSE_SCREEN_STATE': GameLoseScreenState(SCREEN, RESOURCE_LOADER),
              'GAME_WIN_SCREEN_STATE': GameWinScreenState(SCREEN, RESOURCE_LOADER),
              'SAVE_MENU_STATE': GameSaveMenuState(SCREEN, RESOURCE_LOADER),
              'LOAD_MENU_STATE': GameLoadMenuState(SCREEN, RESOURCE_LOADER)}
    GAME = GameStateManager(STATES, 'MAIN_MENU_STATE', SCREEN, caption='PyPong!')
    GAME.run()
    pygame.quit()
    sys.exit()
