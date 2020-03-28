from flask import Flask
from camera import CAMERA_APP


app = Flask(__name__)
app.register_blueprint(CAMERA_APP)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
