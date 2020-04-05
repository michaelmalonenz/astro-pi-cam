from http import HTTPStatus
from importlib import import_module
import logging
import os
from flask import render_template, Blueprint, Response

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from picam_adapter import Camera


CAMERA_APP = Blueprint('camera', __name__, template_folder='templates')
LOGGER = logging.getLogger(__name__)


@CAMERA_APP.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@CAMERA_APP.route('/take_image', methods=['GET'])
def take_image():
    frame = Camera().get_frame()
    return (frame, HTTPStatus.OK, {'Content-Type': 'image/jpeg'})


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@CAMERA_APP.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
