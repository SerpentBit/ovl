# Version 0.1.2

## Changes:
- `BuiltInColors.purple_hsv` is now low=[130, 100, 100], high=[170, 255, 255]

## Bugfixes:
- Fixed a problem where `vision.apply_sample` couldnt accept `MultiColor` Objects
- Fixed an issue with passing parameters to a `Vision` object
- Value of `BuiltInColors.yellow_hsv` is now correct.
- Fixed an issue with `Sorters.descending_area_sort`
- `MultiColor` and `Color` object's `.light()` and `.dark()` now correctly return the changed Object.
- Set value for `Color` objects now works properly
