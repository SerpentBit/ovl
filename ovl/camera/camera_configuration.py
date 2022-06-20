import dataclasses
from typing import Dict, Any, Union, Optional

from .camera_calibration import CameraCalibration
from .camera_properties import CameraProperties


@dataclasses.dataclass
class CameraConfiguration:
    camera_properties: Dict[Union[CameraProperties, int], Any]
    camera_calibration: CameraCalibration = None
    camera_source: Optional[str] = None
