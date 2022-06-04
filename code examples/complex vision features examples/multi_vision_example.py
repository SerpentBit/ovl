import asyncio
import copy
from logging import getLogger


import ovl
from ovl import display_contours

logger = getLogger("multi_vision_example")

target_filters = [ovl.percent_area_filter(minimal_percent=2), ovl.area_sort()]

camera = ovl.Camera(0)

red_circle = ovl.Vision(target_filters=target_filters, threshold=ovl.HSV.red, camera=camera)

green_circle = copy.copy(red_circle)
green_circle.detector = ovl.ThresholdDetector(threshold=ovl.HSV.green)

yellow_circle = copy.copy(red_circle)
yellow_circle.detector = ovl.ThresholdDetector(threshold=ovl.HSV.yellow)

# connection = NetworkTablesConnection("1937")

circles = {"green": green_circle, "red": red_circle, "yellow": yellow_circle}
controller = ovl.MultiVision(visions=circles)

switcher = {"green": "red", "red": "yellow", "yellow": "green"}

current_color = "green"


@controller.vision_updater
async def update_vision(current_vision):
    global current_color
    next_vision_index = switcher[current_color]
    logger.info(f"Updating vision to {next_vision_index} ")
    current_color = next_vision_index
    await asyncio.sleep(3)
    return controller.visions[next_vision_index]


async def main():
    async for directions, targets, image in controller.start():
        # print(controller.current_vision.detector.threshold)
        display_contours(image, targets, display_loop=True)


asyncio.run(main())
