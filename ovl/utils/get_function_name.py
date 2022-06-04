import functools


def get_function_name(func):
    """
    Get the name of a function.
    """
    try:
        if isinstance(func, functools.partial):
            return func.func.__name__
        return func.__name__
    except AttributeError:
        return repr(func)
