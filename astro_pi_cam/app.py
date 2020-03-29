from flask import Flask, redirect, url_for
from flask_assets import Environment, Bundle
from camera import CAMERA_APP


app = Flask(__name__)
app.register_blueprint(CAMERA_APP, url_prefix='/camera')

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/astropi.scss', filters='pyscss', output='astropi.css')
assets.register('scss_all', scss)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('camera.index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
