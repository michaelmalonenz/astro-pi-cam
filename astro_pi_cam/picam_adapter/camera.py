import io
from datetime import datetime
import time
import os
from pathlib import Path
import sys
import gphoto2 as gp

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
    class Camera:

        def capture_still(self, **options):
            config = dslr_camera.get_config()
            dslr_camera.set_config(config)
            file_path = dslr_camera.capture(gp.GP_CAPTURE_IMAGE)
            camera_file = dslr_camera.file_get(
                file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
            return camera_file.stream.read()

elif 'picamera' in sys.modules:
    class Camera:

        def __init__(self):
            self.camera = None

        def __del__(self):
            if self.camera:
                self.camera.close()

        def capture_still(self, **options):
            if self.camera:
                self.camera.close()
            try:
                self.camera = picamera.PiCamera()

                # let camera warm up
                time.sleep(2)

                for key, value in options.items():
                    if key not in ('num_shots', 'frame_between'):
                        setattr(self.camera, key, value)

                directory = Path(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
                directory.mkdir(0o775)
                result = None
                for i in range(1, options['num_shots'] + 1):
                    stream = io.BytesIO()
                    self.camera.capture(stream, 'jpeg')
                    stream.seek(0)
                    result = stream.read()
                    with open(directory / f'{i:04d}.jpeg', 'wb') as fd:
                        fd.write(result)
                    if options.get('frame_between'):
                        time.sleep(options['frame_between'])
                return result
            finally:
                self.camera.close()
                self.camera = None
else:
    IMAGES_DIR = Path(Path(__file__).parent.absolute(), 'test_images')


    class Camera:
        """An emulated camera implementation that streams a repeated sequence of
        files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
        imgs = [open(str(Path(IMAGES_DIR, f + '.jpg')), 'rb').read() for f in ['1', '2', '3']]

        def capture_still(self, **options):
            return Camera.imgs[int(time.time()) % 3]
