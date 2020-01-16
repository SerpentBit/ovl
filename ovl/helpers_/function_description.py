def function_description(function):
    return ("Function Name: {function_name}\n"
            "documentation:\n{documentation}"
            .format(function_name=function.__name__, documentation=function.__doc__))
