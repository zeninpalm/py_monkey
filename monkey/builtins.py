from . import objects
from .evaluator import new_error


def _len(*args):
    if len(args) != 1:
        return new_error(f"wrong number of arguments, got={len(args)}, want=1")

    arg = args[0]
    if arg.type() == objects.STRING_OBJ:
        return objects.Integer(len(arg.value))
    else:
        return new_error(f"argument to 'len' is not supported, got {arg.type()}")

builtins = {
    "len": objects.Builtin(_len)
}