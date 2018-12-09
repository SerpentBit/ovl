# Geometry.calculate_math_expression

| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
|expression |No default | string | N/A  | The math equation |
| value | No default | float | N/A | The value with which to replace the variable |
|additional_function | Math functions (see below) | function | N/A | Additional functions that can be used in the math expression | 
| symbol | 'x' | string | N/A | The variable in the equation |

Returns the solution to the given mathamatical expression using the given value.

</br>
</br>

## *Math Functions*
All of the functions available are:

| symbol| function| example| description|
|:---:|:---:|:---:|:---:|
|x | N/A | x| change is simply based on the index|
|+| addition| 5 + x| pixel plus 5|
|-| subtract| x - 3| pixel minus 3|
|*| multiplication| 2*x| pixel times 2|
| / | division| x/3| x divided by 3|
|%| modulus| x%2| the remainder of x divided by 2|
|**| exponent| x**2| x*x|
|log()| logarithim function| log(x,2) log(x)| log x in base 2 log x in base e|
|sin()| sine function| sin(30)| sine of 30 (0.5)|
|cos()| cosine function| cos(-120)| cosine of -120 (-0.5)|
|tan()| tangent function| tan(45)| tangent of 45 (1)|
|()| parentheses| 3*(x-2)| subtracts 2 from x and then multiplies by 3|
|fact()| factorial| fact(x)| the factorial of x|

</br>
</br>

Code example:
```
>>> calculate_math_expression("9 ** sin(10x))", 3)
3
```
