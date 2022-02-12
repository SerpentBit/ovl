import functools


class ReversePartial(functools.partial):
    """
     A keyword_partial that passes the call arguments before the loaded (passed in constructor) arguments
    """

    def __call__(*args, **keywords):
        if not args:
            raise TypeError("descriptor '__call__' of keyword_partial needs an argument")
        self, *args = args
        new_keyword_arguments = self.keywords.copy()
        new_keyword_arguments.update(keywords)
        return self.func(*args, *self.args, **new_keyword_arguments)
