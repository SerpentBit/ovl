from inspect import getmembers, isfunction


def get_defined_methods():
    """
     Returns a list of all available functions within the current_vision scope
    :return: list of function object that are callable
    """
    function_list = []
    for module, module_object in globals().items():
        for sub_object_name, sub_object in getmembers(module_object):
            if isfunction(sub_object):
                function_list.append((sub_object_name, sub_object))
                continue
            for sub_members_name, sub_members_objects in getmembers(sub_object):
                if isfunction(sub_members_objects):
                    function_list.append((sub_members_name, sub_members_objects))
    return function_list
