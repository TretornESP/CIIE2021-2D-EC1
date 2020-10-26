import sys, logging

class Clog():
    def __init__(self, tag):
        self._tag = tag
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    def info(self, msg):
        logging.info('%s %s', self._tag, msg)

    def debug(self, msg):
        logging.debug('%s %s', self._tag, msg)
