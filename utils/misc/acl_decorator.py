def allow(state=False):
    def wrapper(func):
        setattr(func, 'allow', True)
        setattr(func, 'state', state)
        return func
    return wrapper
