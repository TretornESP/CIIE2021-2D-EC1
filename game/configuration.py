class Configuration():
    METERS_PER_PIXEL = 0.03837

    def __init__(self, config):
        self._resolution = config["resolution"]
        self._name = config["name"]
        self._debug = config["debug"]

    def get_resolution(self):
        return (self._resolution[0], self._resolution[1])

    def get_name(self):
        return self._name

    def get_pixels(self, speed):
        pixels_x = speed[0] / Configuration.METERS_PER_PIXEL
        pixels_y = speed[1] / Configuration.METERS_PER_PIXEL
        return (pixels_x, pixels_y)

    def is_debug(self):
        return self._debug
