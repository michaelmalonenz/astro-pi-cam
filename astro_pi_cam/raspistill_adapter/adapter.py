"""A class for wrapping access to the raspistill program for taking images using the
raspberry pi camera"""
from subprocess import run, CalledProcessError
import logging


LOGGER = logging.getLogger(__name__)


class RaspistillAdapter:

    def __init__(self):
        self.pause_time = 2

    def take_image(self):
        cmd = ['raspistill']
        try:
            result = run(cmd, check=True, capture_output=True)
            result.returncode
        except CalledProcessError:
            LOGGER.exception("raspistill failed to take an image")

