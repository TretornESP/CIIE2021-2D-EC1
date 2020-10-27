from game import ResourceManager

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Configuration(metaclass=Singleton):
    METERS_PER_PIXEL = 0.03837

    def __init__(self):
        config = ResourceManager.load_config()
        self._resolution = config["resolution"]
        self._name = config["name"]

    def get_resolution(self):
        return (self._resolution[0], self._resolution[1])

    def get_name(self):
        return self._name

    def get_pixels(self, speed):
        pixels_x = speed[0] / Configuration.METERS_PER_PIXEL
        pixels_y = speed[1] / Configuration.METERS_PER_PIXEL
        return (pixels_x, pixels_y)
