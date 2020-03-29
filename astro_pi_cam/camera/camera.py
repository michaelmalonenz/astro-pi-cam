import logging
from flask import render_template, Blueprint


CAMERA_APP = Blueprint('camera', __name__, template_folder='templates')
LOGGER = logging.getLogger(__name__)


@CAMERA_APP.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@CAMERA_APP.route('/take_image', methods=['GET'])
def take_image():
    pass

