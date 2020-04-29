from .aaron import __functions__ as aaron_func
from .victor import __functions__ as victor_func
from .wilson import __functions__ as wilson_func

from .general import __functions__ as general_func

# __all__ = ["victor", "wilson", "aaron", "general"]

__functions__ = {
    **aaron_func,
    **victor_func,
    **wilson_func,
    **general_func
}