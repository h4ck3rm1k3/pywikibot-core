'''
from mustbe import must_be
'''
def must_be(group=None, right=None):
    """ Decorator to require a certain user status. For now, only the values
        group = 'user' and group = 'sysop' are supported. The right property
        will be ignored for now.

        @param group: the group the logged in user should belong to
                      legal values: 'user' and 'sysop'
        @param right: the rights the logged in user hsould have
                      not supported yet and thus ignored.
        @returns: a decorator to make sure the requirement is statisfied when
                  the decorated function is called.
    """
    if group == 'user':
        run = lambda self: self.login(False)
    elif group == 'sysop':
        run = lambda self: self.login(True)
    else:
        raise Exception("Not implemented")

    def decorator(fn):
        def callee(self, *args, **kwargs):
            run(self)
            return fn(self, *args, **kwargs)
        callee.__name__ = fn.__name__
        callee.__doc__ = fn.__doc__
        return callee

    return decorator
