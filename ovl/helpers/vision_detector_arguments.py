from collections import namedtuple

from ..detectors.haar_cascade_detector import HaarCascadeDetector
from ..detectors.threshold_detector import ThresholdDetector

GroupToDetector = namedtuple("GroupToDetector", "constructor arguments")
_GROUP_TO_DETECTOR = {"threshold": GroupToDetector(ThresholdDetector, "threshold amd/or morphological functions"),
                      "haar_cascade": GroupToDetector(HaarCascadeDetector, "haar_classifier")}


def _argument_group_to_detector_constructor(argument_group, *args, **kwargs):
    return _GROUP_TO_DETECTOR[argument_group].constructor(*args, **kwargs)


def arguments_to_detector(mutually_exclusive_arguments):
    existing_group = None
    existing_group_name = None
    for group_name, argument_group in mutually_exclusive_arguments.items():
        if any(argument_group):
            if existing_group_name:
                raise ValueError(
                    "When passing parameters that create a Detector only 1 group can be passed,"
                    " got both '{}' and '{}'".format(_GROUP_TO_DETECTOR[group_name].arguments,
                                                     _GROUP_TO_DETECTOR[argument_group].arguments))
            else:
                existing_group = argument_group
                existing_group_name = group_name

    if existing_group_name is None:
        detector = None
    elif existing_group_name != "detector":
        detector = _argument_group_to_detector_constructor(existing_group_name, *existing_group)
    else:
        detector = existing_group
    return detector
