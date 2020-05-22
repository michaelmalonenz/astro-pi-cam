import base64
from http import HTTPStatus
from importlib import import_module
import logging
import os
from flask import render_template, Blueprint, Response, request

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from picam_adapter import Camera


CAMERA_APP = Blueprint('camera', __name__, template_folder='templates')
LOGGER = logging.getLogger(__name__)
DEFAULTS = {
    'num_shots': '1',
    'shutter_speed': '40000',
    'frame_between': '50',
    'exposure_mode': 'auto',
}


@CAMERA_APP.route('/', methods=['GET'])
def index():
    return render_template('index.html.jinja', **DEFAULTS)


@CAMERA_APP.route('/take_image', methods=['GET', 'POST'])
def take_image():
    camera = Camera()
    options = {}
    for key, value in request.args.items():
        if key == 'denoise':
            options['image_denoise'] = value == 'on'
        elif key in ('shutter_speed', 'iso', 'num_shots', 'frame_between'):
            if value != '':
                options[key] = int(value)
        else:
            options[key] = value
    image = camera.capture_still(**options)
    return (base64.b64encode(image), HTTPStatus.CREATED)


@CAMERA_APP.route('/preview')
def preview_image():
    return render_template('preview.html')
