import io
import time
import os
from pathlib import Path
import sys
import gphoto2 as gp
from .base_camera import BaseCamera

try:
    import picamera
except ImportError:
    pass

try:
    dslr_camera = gp.Camera()
    dslr_camera.init()
except gp.GPhoto2Error as ex:
    dslr_camera = None


if dslr_camera is not None:
    class Camera(BaseCamera):
        def frames(self):
            pass

        def capture_still(self, **options):
            config = dslr_camera.get_config()
            dslr_camera.set_config(config)
            file_path = dslr_camera.capture(gp.GP_CAPTURE_IMAGE)
            camera_file = dslr_camera.file_get(
                file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
            return camera_file.stream.read()

elif 'picamera' in sys.modules:
    class Camera(BaseCamera):

        def __init__(self):
            super().__init__()
            self.camera = picamera.PiCamera()

        def __del__(self):
            if self.camera:
                self.camera.close()

        def frames(self):
            if self.camera is None:
                self.camera = picamera.PiCamera()
                # let camera warm up
                time.sleep(2)

            stream = io.BytesIO()
            for _ in self.camera.capture_continuous(stream, 'jpeg',
                                                use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

        def capture_still(self, **options):
            if self.camera:
                self.camera.close()
            self.camera = picamera.PiCamera()

            # let camera warm up
            time.sleep(2)

            for key, value in options.items():
                setattr(self.camera, key, value)

            stream = io.BytesIO()
            self.camera.capture(stream, 'jpeg')
            self.camera.close()
            self.camera = None
            stream.seek(0)
            return stream.read()

else:
    IMAGES_DIR = Path(Path(__file__).parent.absolute(), 'test_images')


    class Camera(BaseCamera):
        """An emulated camera implementation that streams a repeated sequence of
        files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
        imgs = [open(str(Path(IMAGES_DIR, f + '.jpg')), 'rb').read() for f in ['1', '2', '3']]

        def frames(self):
            while True:
                time.sleep(1)
                yield Camera.imgs[int(time.time()) % 3]

        def capture_still(self, **options):
            return Camera.imgs[int(time.time()) % 3]
