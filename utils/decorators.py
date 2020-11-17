"""Decorators."""
def eval_safe(func):
    def wrapper(ref, *args):
        no_no = ["import"]
        for i in args:
            if any([True for k in no_no if k in i.lower()]):
                raise TypeError("Bro.")
        else:
            func(ref, *args)
    return wrapper