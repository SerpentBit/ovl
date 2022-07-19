import ovl
from ovl import CameraConfiguration, CameraProperties

camera = ovl.Camera(0, start_immediately=False)

camera_config = CameraConfiguration({
    CameraProperties.IMAGE_WIDTH: 640,  # set image width to 640 pixels
    CameraProperties.IMAGE_HEIGHT: 480,  # set image width to 480 pixels
    CameraProperties.CAMERA_FPS: 60,  # Frame per second to 60
    CameraProperties.AUTO_EXPOSURE: 0  # Turn off auto exposure
})

camera.configure_camera(camera_config)

camera.set_exposure(-12, configuration_delay=2)  # Setting exposure usually demands a delay for adjustment
camera.start()

while True:
    image = camera.get_image()
    ovl.display_image(image, display_loop=True)
