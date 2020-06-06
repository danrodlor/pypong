import os
import json
import datetime
import pygame
import config
from widgets import SimpleButton

# TODO:
#       - Should be StorageSlot a widget (inheritance) or should it be composed by a widget?
#       ---->THEORY SAYS COMPOSITION OVER INHERITANCE...
#       - May be this can be just a couple of functions create_folder/check_files/save/load
#       - file and screenshot filenames can be removed, duplicated info ----> Check this out

class StorageSlot(SimpleButton):

    def __init__(self, slot_id, x, y, width, height, screen, **kwargs):
        super().__init__(x, y, width, height, screen, **kwargs)
        self._id = str(slot_id)
        self._metadata = {}
        self._file = None
        self._filename = None
        self._screenshot_file = None
        self._screenshot_filename = None
        self._create_storage_folder()
        self._check_saved_files()

    def _create_storage_folder(self):
        if not os.path.isdir(config.STORAGE_BASE_PATH):
            os.mkdir(config.STORAGE_BASE_PATH)

    def _check_saved_files(self):
        slot_file_data = "_".join(["slot", self._id, "data"])
        slot_file_screenshot = "_".join(["slot", self._id, "screenshot"])
        for filename in os.listdir(config.STORAGE_BASE_PATH):
            if filename.startswith(slot_file_data) and filename != self._filename:
                self._filename = filename
                self._file = "\\".join([config.STORAGE_BASE_PATH, filename])
                with open(self._file, 'r') as loadfile:
                    storage_data = json.load(loadfile)
                    self._metadata = storage_data['metadata']
                self.textbox.modify(newtext=self._metadata['timestamp'])
            elif filename.startswith(slot_file_screenshot) and filename != self._screenshot_filename:
                self._screenshot_filename = filename
                self._screenshot_file = "\\".join([config.STORAGE_BASE_PATH, filename])
                screenshot = pygame.image.load(self._screenshot_file).convert()
                self._still_image = pygame.transform.scale(screenshot, (self._width, self._height))

    def _remove_last_saved_file(self):
        slot_file_data = "_".join(["slot", self._id, "data"])
        slot_file_screenshot = "_".join(["slot", self._id, "screenshot"])
        for filename in os.listdir(config.STORAGE_BASE_PATH):
            if filename.startswith(slot_file_data) or filename.startswith(slot_file_screenshot):
                filepath = "\\".join([config.STORAGE_BASE_PATH, filename])
                os.remove(filepath)

    def save_game(self, data):
        # TODO: Ask if the user is sure of the operation??
        self._remove_last_saved_file()

        date = datetime.datetime.now()
        strdate = date.strftime("%d-%m-%Y")
        strtime = date.strftime("%H-%M-%S")
        self._metadata['timestamp'] = " ".join([strdate, strtime])

        self._filename = "_".join(["slot", self._id, "data", strdate, strtime])
        self._file = "".join([config.STORAGE_BASE_PATH, "\\", self._filename, ".json"])

        # FIXME: Use the resource loader instead? Or better, just pass the image as a parameter to this method
        self._screenshot_filename = "_".join(["slot", self._id, "screenshot", strdate, strtime])
        self._screenshot_file = "".join([config.STORAGE_BASE_PATH, "\\", self._screenshot_filename, ".png"])
        screenshot = pygame.image.frombuffer(config.PAUSED_GAME_IMG_STRING, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 'RGB').convert()
        pygame.image.save(screenshot, self._screenshot_file)

        self._still_image = pygame.transform.scale(screenshot, (self._width, self._height))
        self.textbox.modify(newtext=self._metadata['timestamp'])

        storage_data = {'metadata': self._metadata, 'data': data}

        with open(self._file, 'w') as savefile:
            json.dump(storage_data, savefile, indent=4)

    def load_game(self):
        with open(self._file, 'r') as loadfile:
            storage_data = json.load(loadfile)
        self.textbox.modify(newtext="Loaded")
        screenshot = pygame.image.load(self._screenshot_file).convert()
        screenshot_img_string = pygame.image.tostring(screenshot, 'RGB')
        config.PAUSED_GAME_IMG_STRING = screenshot_img_string

        return storage_data['data']

    def update(self, event):
        self._check_saved_files()
        super().update(event)
