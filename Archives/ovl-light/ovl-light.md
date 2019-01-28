# ovl-light 
ovl-light is a lighter version of the library that doesnt not include the calibration module.
this removes the use of multiple dependencies - including sklearn, pandas and scipy.
The major and almost only affect this has is that you cannot run calibration scripts,
this does not stop you from using a calibration json and applying it to a vision object.
The main benefit and use of this is faster and smaller download - by a significant amount.
