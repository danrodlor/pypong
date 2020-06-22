import os
import pygame

# 1) Abstract the loading from the resource type, can hold a dict with the supported type, 
# its accepted_extensions and the loading function (lambda) 
# 2) Add try/catch when needed, define new type of exceptions (?)

class EmptySound():
    def play(self):
        pass

class MuteableSound():

    SOUNDS_MUTED = False

    def __init__(self, filepath):
        self.sound = pygame.mixer.Sound(filepath)

    def play(self):
        if self.SOUNDS_MUTED:
            pass
        else:
            self.sound.play()

    @classmethod
    def mute_all(cls):
        cls.SOUNDS_MUTED = True

    @classmethod
    def unmute_all(cls):
        cls.SOUNDS_MUTED = False

class ResourceLoader():

    RESOURCES = ('images', 'sounds')
    ACCEPTED_SOUND_EXTENSIONS = ('.ogg', '.mp3', '.wav')
    ACCEPTED_IMAGE_EXTENSIONS = ('.png', '.jpeg')

    def __init__(self, resource_root_path):
        self._cache = {}
        self._resource_root_path = resource_root_path
        self._load()

    def _load(self):
        if not self._cache:
            for resource_type in self.RESOURCES:
                resource_path = os.path.join(self._resource_root_path, resource_type)
                self._cache[resource_type] = {}
                for file in os.listdir(resource_path):
                    filepath = os.path.join(resource_path, file)
                    resource_name = file.split('.')[0]
                    if resource_type == 'images' and file.endswith(self.ACCEPTED_IMAGE_EXTENSIONS):
                        self._cache[resource_type][resource_name] = pygame.image.load(filepath).convert()
                    elif resource_type == 'sounds' and file.endswith(self.ACCEPTED_SOUND_EXTENSIONS):
                        self._cache[resource_type][resource_name] = MuteableSound(filepath)

            self.add_sound(None, EmptySound())

    def lookup(self, resource_type, resource_name):
        return self._cache[resource_type][resource_name]

    def get_image(self, image_name):
        return self.lookup('images', image_name)

    def get_sound(self, sound_name):
        return self.lookup('sounds', sound_name)

    def add_image(self, image_name, image_obj):
        self._cache['images'][image_name] = image_obj

    def add_sound(self, sound_name, sound_obj):
        self._cache['sounds'][sound_name] = sound_obj
