"""Decorators."""
def eval_safe(func):
    async def wrapper(ref, *args):
        no_no = ["import"]
        for i in args:
            if any([True for k in no_no if k in i.lower()]):
                raise TypeError("Bro.")
        else:
            return await func(ref, *args)
    return wrapper 