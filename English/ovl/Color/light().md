# *.light()*

This function is used for quick debugging and testing. This function exists both for the `MultiColor` Class and the `Color` Class
The Function returns a **copy** of the changed value

| Parameter Name | Default value | Types | Value range | Description | 
| :---: |  :---: | :---: | :---: | :---: |
|Amount| 50| int| 0< x < 255| The amount decreased from the low bounds saturation value. Affects all colors in a `MultiColor`|

```
>>> c1, c2 = Color([20, 100, 100], [37, 255, 255]), Color([40, 75, 100], [75, 255, 255])
>>> c1.light() 
[20 50 100]  [37 255 255] 
>>> c1
[20 100 100] [37 255 255]  
>>> m = MultiColor([c1, c2])
>>> m.light(25)
[20 75 100] [37 255 255], [40 50 100] [75 255 255] 
>>> m
[20 100 100] [37 255 255], [40 75 100] [75 255 255] 
```
As we can see the original object does not change, `light()` returns a copy.
