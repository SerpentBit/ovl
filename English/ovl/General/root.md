# General.root

| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| base | No default | int, float | N/A  | The base number which is rooted by `degree` |
| degree | No Default | int, float | N/A | The root that `base` is rooted to |

Returns the result (as a 'float') of the `base` rooted by degree which is the same as `base` raised by the (`1/degree`).

Code Example:
```
>>> base = 9
>>> degree = 2
>>> root(base, degree)
3.0
```
</br></br>
```
>>> base = 8
>>> degree = 3
>>> root(base, degree)
2.0
```
