import dataclasses
from typing import Dict, Any

from .camera_calibration import CameraCalibration
from .camera_properties import CameraProperties


@dataclasses.dataclass
class CameraConfiguration:
    camera_properties: Dict[CameraProperties, Any]
    camera_calibration: CameraCalibration = None
