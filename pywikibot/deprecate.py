def warning (x):
    print(x)

def debug (x):
    print(x)

def deprecated(instead=None):
    """Decorator to output a method deprecation warning.

    @param instead: if provided, will be used to specify the replacement
    @type instead: string
    """
    def decorator(method):
        def wrapper(*args, **kwargs):
            funcname = method.__name__
            classname = args[0].__class__.__name__
            if instead:
                warning("%s.%s is DEPRECATED, use %s instead."
                        % (classname, funcname, instead))
            else:
                warning("%s.%s is DEPRECATED." % (classname, funcname))
            return method(*args, **kwargs)
        wrapper.__name__ = method.__name__
        return wrapper
    return decorator


def deprecate_arg(old_arg, new_arg):
    """Decorator to declare old_arg deprecated and replace it with new_arg"""

    def decorator(method):
        def wrapper(*__args, **__kw):
            meth_name = method.__name__
            if old_arg in __kw:
                if new_arg:
                    if new_arg in __kw:
                        warning(
"%(new_arg)s argument of %(meth_name)s replaces %(old_arg)s; cannot use both."
                            % locals())
                    else:
                        warning(
"%(old_arg)s argument of %(meth_name)s is deprecated; use %(new_arg)s instead."
                            % locals())
                        __kw[new_arg] = __kw[old_arg]
                else:
                    debug(
"%(old_arg)s argument of %(meth_name)s is deprecated."
                        % locals())
                del __kw[old_arg]
            return method(*__args, **__kw)
        wrapper.__doc__ = method.__doc__
        wrapper.__name__ = method.__name__
        return wrapper
    return decorator
