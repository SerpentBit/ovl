# General.numerical_replace

| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
| string |No default | string | N/A  | A string built from numbers |
| *args | No Default | N/A | N/A | The strings that will replace the numbers in the given string |

Returns the `string` after replacing the numbers appearing in it with the given strings in `*args` according to the order.

## Code Examples:
```
>>> string = "I went to the 0 to buy 1, 2, and 3"
>>> numerical_replace(string, "supermarket", "eggs", "milk", "flour")
'I went to the supermarket to buy eggs, milk, and flour'
```
</br> </br>
```
>>> string = "If 1 = 1 then 0 must equal 5"
>>> numerical_replace(string, "5")
'If 1 = 1 then 5 must equal 5'
```
</br></br>
```
>>> string = "If 1 = 1 then 0 must equal 3"
>>> numerical_replace(string, "1", "2", "3", "4")
'If 2 = 2 then 1 must equal 4'
```
