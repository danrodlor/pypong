import config
import pygame
from pygame.locals import *
from input import InputController, AIController
from entities import Paddle, Ball
from widgets import SimpleTextBox, SimpleButton
from storage import StorageSlot
from loader import MuteableSound

# TODO:
# 4) Decouple game variables (screen, clock...) from GameStateManager, maybe a Game class?
# 5) Decouple the use of screen in each state (just pass it as parameter in draw()) (classes should be reworked as well)
# 6) Add 'dt' in state machine and update methods of the states (classes should be reworked as well)
# 8) Add new method to state; resume/startup. Clear buttons, reset game... (MAY BE NOT)
# 11) Refactor class attributes that have to be private -> _whatever
# 14) Add a logger to the whole game
# 15) Add type hinting

# references:
#   - https://python-forum.io/Thread-PyGame-Creating-a-state-machine
#   - https://gist.github.com/iminurnamez/8d51f5b40032f106a847
#   - https://python-3-patterns-idioms-test.readthedocs.io/en/latest/StateMachine.html

class GameStateManager():

    def __init__(self, states, start_state, screen, caption='Game'):
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.caption = caption
        self.states = states
        self.current_state_name = start_state
        self.current_state = self.states[start_state]
        self.is_running = True
        self.is_fps_counter_enabled = False
        self._fps_counter = SimpleTextBox(650, 10, screen, text='60 fps', size=12)

        pygame.display.set_caption(self.caption)

    def _update_fps_counter(self):
        if self.is_fps_counter_enabled:
            average_fps = self.clock.get_fps()
            fps_str = "{0:.2f} fps".format(average_fps)
            self._fps_counter.modify(newtext=fps_str)
            self._fps_counter.update()

    def _draw_fps_counter(self):
        if self.is_fps_counter_enabled:
            self._fps_counter.draw()

    def switch_state(self):
        next_state_name = self.current_state.next_state
        self.current_state.clean()
        self.current_state_name = next_state_name
        self.current_state = self.states[self.current_state_name]

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.is_fps_counter_enabled = not self.is_fps_counter_enabled
            self.current_state.get_event(event)

    def update(self):
        if self.current_state.is_quit:
            self.is_running = False
        elif self.current_state.is_done:
            self.switch_state()

        self.current_state.update()
        self._update_fps_counter()

    def draw(self):
        self.current_state.draw()
        self._draw_fps_counter()

    def run(self):
        while self.is_running:
            dt = self.clock.tick(config.FPS)
            self.process_events()
            self.update()
            self.draw()
            pygame.display.update()

class State():
    SHARED_DATA = {'GAME_DATA': {}, 'GAME_CONTROL': {'data_loaded': False}}
    def __init__(self):
        self.next_state = None
        self.is_done = False
        self.is_quit = False

    def clean(self):
        self.is_done = False
        self.is_quit = False
        self.next_state = None

    def get_event(self, event):
        raise NotImplementedError

    # TODO: This should be update(self, dt)
    def update(self):
        raise NotImplementedError

    # TODO: This should be draw(self, screen)
    def draw(self):
        raise NotImplementedError

class GameMainMenuState(State):

    def __init__(self, screen, resource_loader):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.title = 'PyPong!'
        self.title_textbox = SimpleTextBox(self.screen_rect.centerx, 100, screen, text=self.title, size=72)
        self.play_button = SimpleButton(self.screen_rect.centerx, self.title_textbox.rect.bottom + 50, 150, 50, screen, text='PLAY', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.load_button = SimpleButton(self.screen_rect.centerx, self.play_button.rect.bottom + 50, 150, 50, screen, text='LOAD', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.options_button = SimpleButton(self.screen_rect.centerx, self.load_button.rect.bottom + 50, 150, 50, screen, text='OPTIONS', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.exit_button = SimpleButton(self.screen_rect.centerx, self.options_button.rect.bottom + 50, 150, 50, screen, text='EXIT', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.widgets = [self.title_textbox, self.play_button, self.load_button, self.options_button, self.exit_button]
        self.buttons = [self.play_button, self.load_button, self.options_button, self.exit_button]
        self.buttons_map = {0: "GAME_COUNTDOWN_STATE", 1: "LOAD_MENU_STATE", 2: "OPTIONS_MENU_STATE", 3: "EXIT"}

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.is_quit = True
        else:
            for button in self.buttons:
                button.update(event)

    def update(self):
        self.title_textbox.update()

        for idx, button in enumerate(self.buttons):
            if button.is_clicked:
                self.next_state = self.buttons_map.get(idx)
                if self.next_state is "EXIT":
                    self.is_quit = True
                else:
                    self.is_done = True
                button.clear()
                break
            else:
                self.next_state = None

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for widget in self.widgets:
            widget.draw()

class GameOptionsMenuState(State):

    def __init__(self, screen, resource_loader):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.title = 'OPTIONS'
        self.title_textbox = SimpleTextBox(self.screen_rect.centerx, 100, screen, text=self.title, size=72)
        self.sound_button = SimpleButton(self.screen_rect.centerx, self.title_textbox.rect.bottom + 100, 150, 50, screen, text='Sound: On', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.back_button = SimpleButton(self.screen_rect.centerx, self.sound_button.rect.bottom + 50, 150, 50, screen, text='BACK', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.widgets = [self.title_textbox, self.sound_button, self.back_button]
        self.buttons = [self.sound_button, self.back_button]
        self.buttons_map = {0: "TOGGLE_SOUND", 1: "MAIN_MENU_STATE"}
        self.has_sound = True

    def _toggle_sound(self):
        self.has_sound = not self.has_sound
        if self.has_sound:
            self.sound_button.textbox.modify(newtext='Sound: On')
            MuteableSound.unmute_all()
        else:
            self.sound_button.textbox.modify(newtext='Sound: Off')
            MuteableSound.mute_all()

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.is_quit = True
        else:
            for button in self.buttons:
                button.update(event)

    def update(self):
        self.title_textbox.update()

        for idx, button in enumerate(self.buttons):
            if button.is_clicked:
                self.next_state = self.buttons_map.get(idx)
                if self.next_state is "TOGGLE_SOUND":
                    self._toggle_sound()
                else:
                    self.is_done = True
                button.clear() 
                break
            else:
                self.next_state = None

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for widget in self.widgets:
            widget.draw()

class GamePauseMenuState(State):

    def __init__(self, screen, resource_loader):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.title = 'GAME PAUSED'
        self.title_textbox = SimpleTextBox(self.screen_rect.centerx, 100, screen, text=self.title, size=72)
        self.resume_button = SimpleButton(self.screen_rect.centerx, self.title_textbox.rect.bottom + 100, 150, 50, screen, text='RESUME', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.save_button = SimpleButton(self.screen_rect.centerx, self.resume_button.rect.bottom + 50, 150, 50, screen, text='SAVE', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.quit_button = SimpleButton(self.screen_rect.centerx, self.save_button.rect.bottom + 50, 150, 50, screen, text='QUIT', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.widgets = [self.title_textbox, self.resume_button, self.save_button, self.quit_button]
        self.buttons = [self.resume_button, self.save_button, self.quit_button]
        self.buttons_map = {0: "GAME_COUNTDOWN_STATE", 1: "SAVE_MENU_STATE", 2: "MAIN_MENU_STATE"}

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.is_quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.next_state = 'GAME_COUNTDOWN_STATE'
            self.is_done = True
        else:
            for button in self.buttons:
                # FIXME: State switch occurs at update (1-switch 2-update current), as buttons are being updated in
                # get_event() instead of update(), the changes are not applied until the next frame...
                button.update(event)

    def update(self):
        self.title_textbox.update()

        for idx, button in enumerate(self.buttons):
            if button.is_clicked:
                self.next_state = self.buttons_map.get(idx)
                self.is_done = True
                button.clear()
                break
            else:
                self.next_state = None

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for widget in self.widgets:
            widget.draw()

class GameCountdownState(State):

    TIME_IN_SECONDS = 3

    def __init__(self, screen, resource_loader):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.new_game_img = resource_loader.get_image('new_game_screenshot')
        self.background = self.new_game_img
        self.title = 'Game starts in...'
        self.title_textbox = SimpleTextBox(self.screen_rect.centerx, 100, screen, text=self.title, size=60)
        self.number_3 = SimpleTextBox(self.screen_rect.centerx, 250, screen, text='3', size=72)
        self.number_2 = SimpleTextBox(self.screen_rect.centerx, 250, screen, text='2', size=72)
        self.number_1 = SimpleTextBox(self.screen_rect.centerx, 250, screen, text='1', size=72)
        self.numbers = [self.number_3, self.number_2, self.number_1]
        self.current_number = self.numbers[0]
        self.counter = 0
        self.cowntdown_sound = resource_loader.get_sound('countdown_beep')
        self.match_start_sound = resource_loader.get_sound('match_beep')
        self.is_bg_set = False

    def _set_pause_background(self):
        if not self.is_bg_set:
            if config.PAUSED_GAME_IMG_STRING:
                self.background = pygame.image.fromstring(config.PAUSED_GAME_IMG_STRING,
                                                          (config.SCREEN_WIDTH,
                                                           config.SCREEN_HEIGHT),
                                                          'RGB')
            else:
                self.background = self.new_game_img
            self.background.set_alpha(100)
            self.is_bg_set = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.is_quit = True

    def update(self):
        self._set_pause_background()

        if self.counter >= (self.TIME_IN_SECONDS * config.FPS):
            self.counter = 0
            self.next_state = 'GAME_RUNNING_STATE'
            self.is_done = True
            self.is_bg_set = False
            self.match_start_sound.play()
        else:
            last_index = (self.counter - 1)//config.FPS
            current_index = self.counter//config.FPS
            self.current_number = self.numbers[current_index]
            if current_index != last_index:
                self.cowntdown_sound.play()
            self.counter += 1

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        self.screen.blit(self.background, (0, 0))
        self.title_textbox.draw()
        self.current_number.draw()

class GameRunningState(State):
    
    MAXIMUM_SCORE = 11

    def __init__(self, screen, resource_loader):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.player = Paddle(config.BRICK_SIZE, 3*config.BRICK_SIZE,
                             2*config.BRICK_SIZE, self.screen_rect.centery,
                             config.PLAYER_SPEED, self.screen, InputController())
        self.ball = Ball(config.BRICK_SIZE, self.screen_rect.centerx,
                         self.screen_rect.centery, 2, self.screen,
                         bounce_sound=resource_loader.get_sound('ball_bounce_2'),
                         hit_sound=resource_loader.get_sound('ball_hit'))
        self.enemy = Paddle(config.BRICK_SIZE, 3*config.BRICK_SIZE,
                            config.SCREEN_WIDTH - 2*config.BRICK_SIZE,
                            self.screen_rect.centery, config.ENEMY_SPEED,
                            self.screen, AIController(self))
        self.entities = [self.ball, self.player, self.enemy]
        self.paddles = [self.player, self.enemy]

        self.player_score = 0
        self.enemy_score = 0
        self.player_score_textbox = SimpleTextBox(self.screen_rect.centerx - 40, 36,
                                                  self.screen, text=str(self.player_score))
        self.enemy_score_textbox = SimpleTextBox(self.screen_rect.centerx + 40, 36,
                                                 self.screen, text=str(self.enemy_score))
        self.widgets = [self.player_score_textbox, self.enemy_score_textbox]
        self.score_point_sound = resource_loader.get_sound('score_point')

        self._init_static_elements()

    def _game_reset(self):
        for entity in self.entities:
            entity.reset()

        self.player_score = 0
        self.enemy_score = 0
        self.player_score_textbox.modify(newtext=str(self.player_score))
        self.enemy_score_textbox.modify(newtext=str(self.enemy_score))

        config.PAUSED_GAME_IMG_STRING = None

    def _update_game_data(self):
        self.SHARED_DATA['GAME_DATA'].update(
            {
            'player_x': self.player.x,
            'player_y': self.player.y,
            'player_score': self.player_score,
            'enemy_x': self.enemy.x,
            'enemy_y': self.enemy.y,
            'enemy_score': self.enemy_score,
            'ball_fx': self.ball.fx,
            'ball_fy': self.ball.fy,
            'ball_xspeed': self.ball.xspeed,
            'ball_yspeed': self.ball.yspeed,
            'ball_speed_coeff': self.ball.speed_coeff,
        }
        )

    def _load_game_data(self):
        self.player.x = self.SHARED_DATA['GAME_DATA']['player_x']
        self.player.y = self.SHARED_DATA['GAME_DATA']['player_y']
        self.player_score = self.SHARED_DATA['GAME_DATA']['player_score']
        self.enemy.x = self.SHARED_DATA['GAME_DATA']['enemy_x']
        self.enemy.y = self.SHARED_DATA['GAME_DATA']['enemy_y']
        self.enemy_score = self.SHARED_DATA['GAME_DATA']['enemy_score']
        self.ball.fx = self.SHARED_DATA['GAME_DATA']['ball_fx']
        self.ball.fy = self.SHARED_DATA['GAME_DATA']['ball_fy']
        self.ball.xspeed = self.SHARED_DATA['GAME_DATA']['ball_xspeed']
        self.ball.yspeed = self.SHARED_DATA['GAME_DATA']['ball_yspeed']
        self.ball.speed_coeff = self.SHARED_DATA['GAME_DATA']['ball_speed_coeff']

        self.player_score_textbox.modify(newtext=str(self.player_score))
        self.enemy_score_textbox.modify(newtext=str(self.enemy_score))

        self.SHARED_DATA['GAME_CONTROL']['data_loaded'] = False

    def _init_static_elements(self):
        self.middle_line = pygame.Surface([5, config.SCREEN_HEIGHT])
        self.middle_line.fill(pygame.Color('white'))

    def _draw_static_elements(self):
        self.screen.blit(self.middle_line, (self.screen_rect.centerx, 0))

    def _get_screenshot(self):
        screenshot_img_string = pygame.image.tostring(self.screen, 'RGB')
        config.PAUSED_GAME_IMG_STRING = screenshot_img_string

    def _check_collisions(self):
        for entity in pygame.sprite.spritecollide(self.ball, self.paddles, dokill=False):
            self.ball.process_collision(entity)

    def _execute_game_logic(self):
        if self.ball.rect.left < self.player.rect.left:
            self.enemy_score += 1
            self.enemy_score_textbox.modify(newtext=str(self.enemy_score))
            self.score_point_sound.play()
            self.ball.reset()
        elif self.ball.rect.right > self.enemy.rect.right:
            self.player_score += 1
            self.player_score_textbox.modify(newtext=str(self.player_score))
            self.score_point_sound.play()
            self.ball.reset()

        if self.enemy_score >= self.MAXIMUM_SCORE:
            self.next_state = 'GAME_LOSE_SCREEN_STATE'
            self.is_done = True
            self._game_reset()
        elif self.player_score >= self.MAXIMUM_SCORE:
            self.next_state = 'GAME_WIN_SCREEN_STATE'
            self.is_done = True
            self._game_reset()

        self._check_collisions()

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.is_quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.next_state = 'PAUSE_MENU_STATE'
            self._get_screenshot()
            self.is_done = True
        else:
            self.player.controller.handle_event(event)

    def update(self):
        if self.SHARED_DATA['GAME_CONTROL']['data_loaded']:
            self._load_game_data()

        self._execute_game_logic()

        self.enemy.controller.update()

        for entity in self.entities:
            entity.update()

        for widget in self.widgets:
            widget.update()

        self._update_game_data()

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        self._draw_static_elements()

        for entity in self.entities:
            entity.draw()

        for widget in self.widgets:
            widget.draw()

class GameLoseScreenState(State):

    def __init__(self, screen, resource_loader):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.title = 'YOU LOST!'
        self.title_textbox = SimpleTextBox(self.screen_rect.centerx, 100, screen, text=self.title, size=72, color='red')
        self.play_again_button = SimpleButton(self.screen_rect.centerx, self.title_textbox.rect.bottom + 100, 150, 50, screen, text='PLAY AGAIN!', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.quit_button = SimpleButton(self.screen_rect.centerx, self.play_again_button.rect.bottom + 50, 150, 50, screen, text='QUIT', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.widgets = [self.title_textbox, self.play_again_button, self.quit_button]
        self.buttons = [self.play_again_button, self.quit_button]
        self.buttons_map = {0: "GAME_COUNTDOWN_STATE", 1: "MAIN_MENU_STATE"}

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.is_quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.next_state = 'GAME_COUNTDOWN_STATE'
            self.is_done = True
        else:
            for button in self.buttons:
                button.update(event)

    def update(self):
        self.title_textbox.update()

        for idx, button in enumerate(self.buttons):
            if button.is_clicked:
                self.next_state = self.buttons_map.get(idx)
                self.is_done = True
                button.clear()
                break
            else:
                self.next_state = None

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for widget in self.widgets:
            widget.draw()

class GameWinScreenState(State):

    def __init__(self, screen, resource_loader):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.title = 'YOU WIN!'
        self.title_textbox = SimpleTextBox(self.screen_rect.centerx, 100, screen, text=self.title, size=72, color='green')
        self.play_again_button = SimpleButton(self.screen_rect.centerx, self.title_textbox.rect.bottom + 100, 150, 50, screen, text='PLAY AGAIN!', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.quit_button = SimpleButton(self.screen_rect.centerx, self.play_again_button.rect.bottom + 50, 150, 50, screen, text='QUIT', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.widgets = [self.title_textbox, self.play_again_button, self.quit_button]
        self.buttons = [self.play_again_button, self.quit_button]
        self.buttons_map = {0: "GAME_COUNTDOWN_STATE", 1: "MAIN_MENU_STATE"}

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.is_quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.next_state = 'GAME_COUNTDOWN_STATE'
            self.is_done = True
        else:
            for button in self.buttons:
                button.update(event)

    def update(self):
        self.title_textbox.update()

        for idx, button in enumerate(self.buttons):
            if button.is_clicked:
                self.next_state = self.buttons_map.get(idx)
                self.is_done = True
                button.clear()
                break
            else:
                self.next_state = None

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for widget in self.widgets:
            widget.draw()

class GameSaveMenuState(State):
    def __init__(self, screen, resource_loader):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.title = 'SAVE A GAME'
        self.title_textbox = SimpleTextBox(self.screen_rect.centerx, 100, screen, text=self.title, size=72, color='white')
        self.storage_slot_0 = StorageSlot(0, self.screen_rect.centerx, self.title_textbox.rect.bottom + 125, 300, 200, screen, callback=self._save_game, text='Free Slot', border=True, hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.confirm_button = SimpleButton(self.screen_rect.centerx, self.storage_slot_0.rect.bottom + 50, 150, 50, screen, text='CONFIRM', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.widgets = [self.title_textbox, self.confirm_button, self.storage_slot_0]
        self.buttons = [self.confirm_button, self.storage_slot_0]
        self.buttons_map = {0: "PAUSE_MENU_STATE", 1: "STAY"}

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.is_quit = True
        else:
            for button in self.buttons:
                button.update(event)

    def _save_game(self):
        self.storage_slot_0.save_game(self.SHARED_DATA)

    def update(self):
        self.title_textbox.update()

        for idx, button in enumerate(self.buttons):
            if button.is_clicked:
                self.next_state = self.buttons_map.get(idx)
                if self.next_state != "STAY":
                    self.is_done = True
                button.clear()
                break
            else:
                self.next_state = None

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for widget in self.widgets:
            widget.draw()

class GameLoadMenuState(State):
    def __init__(self, screen, resource_loader):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.title = 'LOAD A GAME'
        self.title_textbox = SimpleTextBox(self.screen_rect.centerx, 100, screen, text=self.title, size=72, color='white')
        self.storage_slot_0 = StorageSlot(0, self.screen_rect.centerx, self.title_textbox.rect.bottom + 125, 300, 200, screen, callback=self._load_game, text='Free Slot', border=True, hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.confirm_button = SimpleButton(self.screen_rect.centerx, self.storage_slot_0.rect.bottom + 50, 150, 50, screen, text='CONFIRM', hovered_sound=resource_loader.get_sound('btn_hover'), clicked_sound=resource_loader.get_sound('btn_click'))
        self.widgets = [self.title_textbox, self.confirm_button, self.storage_slot_0]
        self.buttons = [self.confirm_button, self.storage_slot_0]
        self.buttons_map = {0: "MAIN_MENU_STATE", 1: "STAY"}

    def _load_game(self):
        loaded_data = self.storage_slot_0.load_game()
        self.SHARED_DATA.update(loaded_data)
        self.SHARED_DATA['GAME_CONTROL']['data_loaded'] = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.is_quit = True
        else:
            for button in self.buttons:
                button.update(event)

    def update(self):
        self.title_textbox.update()

        for idx, button in enumerate(self.buttons):
            if button.is_clicked:
                self.next_state = self.buttons_map.get(idx)
                if self.next_state != "STAY":
                    self.is_done = True
                button.clear()
                break
            else:
                self.next_state = None

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for widget in self.widgets:
            widget.draw()
