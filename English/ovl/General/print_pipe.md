# Geometry.calculate_math_expression

| Parameter Name | Default value | Types | Value range | Description | 
| :---: | :---: | :---: | :---: | :---: |
|out |No default | None / bool / string | N/A  | The variable which dictates how the output will be printed |
| *args | No Default | N/A | N/A | The outputs |

Prints the output which is given in `*args` according to the type of `out`

'if out is None:`
Prints the output onto the screen.

`If out is False:`
The output isn't print at all.

`else:`
Prints the output onto the screen.
Opens/Creates a file in the current directory named `out` and writes all the output into it as well as the time the program was run.
