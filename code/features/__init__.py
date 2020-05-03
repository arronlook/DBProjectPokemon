from .arron import __functions__ as arron_func
from .victor import __functions__ as victor_func
from .wilson import __functions__ as wilson_func
from .wendi import __functions__ as wendi_func

from .general import __functions__ as general_func

# __all__ = ["victor", "wilson", "aaron", "wendi", "general"]

__functions__ = {
    **arron_func,
    **victor_func,
    **wilson_func,
    **wendi_func,
    **general_func
}