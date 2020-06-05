import pygame

class SimpleTextBox():

    def __init__(self, x, y, surface, text='placeholder', color='white', size=36):
        self._text = text
        self._color = pygame.Color(color)
        self._size = size
        self._font = pygame.font.SysFont('consolas', size, bold=True)
        self._pos = (x, y)
        self.rendered_text = self._font.render(text, True, self._color)
        self.rect = self.rendered_text.get_rect(center=(x, y))
        self.surface = surface
        self.is_modified = False

    def modify(self, newtext='modified', newcolor=None):
        self._text = newtext
        if newcolor:
            self._color = pygame.Color(newcolor)
        self.is_modified = True

    def update(self):
        if self.is_modified:
            self.rendered_text = self._font.render(self._text, True, self._color)
            self.rect = self.rendered_text.get_rect(center=self._pos)
            self.is_modified = False

    def draw(self):
        self.surface.blit(self.rendered_text, self.rect)

class SimpleButton(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, screen, color='black', hovered_color='grey',
                 border=False, border_width=2, border_color='white', text=None, text_color='white',
                 text_size=24, hovered_sound=None, clicked_sound=None, callback=None):
        super().__init__()
        self._pos = (x, y)
        self._width = width
        self._height = height
        self._color = pygame.Color(color)
        self._border = border
        self._border_width = border_width
        self._border_color = border_color
        self._hovered_color = pygame.Color(hovered_color)
        self._text = text
        self._text_color = text_color
        self._text_size = text_size
        if self._text:
            self.textbox = SimpleTextBox(x, y, screen, text, text_color, text_size)
        self._hovered_sound = hovered_sound
        self._clicked_sound = clicked_sound
        self.screen = screen
        self._still_image = pygame.Surface([width, height])
        self._still_image.fill(self._color)
        self._hovered_image = pygame.Surface([width, height])
        self._hovered_image.fill(self._hovered_color)
        self._callback = callback
        self.image = self._still_image
        self.rect = self.image.get_rect(center=(x, y))
        self.is_enabled = True
        self.is_hovered = False
        self.is_clicked = False
        self.is_played = False

    def enable(self):
        self.is_enabled = True
        self.clear()

    def disable(self):
        self.is_enabled = False
        self.clear()

    def clear(self):
        self.is_hovered = False
        self.is_clicked = False
        self.image = self._still_image

    def on_hover_check(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_x, mouse_y):
            self.is_hovered = True
            if not self.is_played:
                self._hovered_sound.play()
                self.is_played = True
            self.image = self._hovered_image
        else:
            self.is_hovered = False
            self.is_played = False
            self.image = self._still_image

        return self.is_hovered

    def on_click_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_clicked = True
            self._clicked_sound.play()
            if self._callback:
                self._callback()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_clicked = False

    def update(self, event):
        if self.is_enabled:
            if self.on_hover_check():
                self.on_click_check(event)
            if self._text:
                self.textbox.update()

    def draw(self):
        if self.is_enabled:
            if self._border:
                pygame.draw.rect(self.screen,
                                 pygame.Color(self._border_color),
                                 (self.rect.x - self._border_width,
                                  self.rect.y - self._border_width,
                                  self._width + 2*self._border_width,
                                  self._height + 2*self._border_width))

            self.screen.blit(self.image, self.rect)

            if self._text:
                self.textbox.draw()
