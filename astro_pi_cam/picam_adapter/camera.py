import io
import time
from pathlib import Path
import sys
from .base_camera import BaseCamera

try:
    import picamera
except ImportError:
    pass


if 'picamera' in sys.modules:
    class Camera(BaseCamera):
        @staticmethod
        def frames():
            with picamera.PiCamera() as camera:
                # let camera warm up
                time.sleep(2)

                stream = io.BytesIO()
                for _ in camera.capture_continuous(stream, 'jpeg',
                                                    use_video_port=True):
                    # return current frame
                    stream.seek(0)
                    yield stream.read()

                    # reset stream for next frame
                    stream.seek(0)
                    stream.truncate()
else:
    IMAGES_DIR = Path(Path(__file__).parent.absolute(), 'test_images')


    class Camera(BaseCamera):
        """An emulated camera implementation that streams a repeated sequence of
        files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
        imgs = [open(str(Path(IMAGES_DIR, f + '.jpg')), 'rb').read() for f in ['1', '2', '3']]

        @staticmethod
        def frames():
            while True:
                time.sleep(1)
                yield Camera.imgs[int(time.time()) % 3]
