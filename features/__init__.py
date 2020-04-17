from .aaron import __functions__
from .victor import __functions__
from .wilson import __functions__

from .general import __functions__

__functions__ = {
    **aaron.__functions__,
    **victor.__functions__,
    **wilson.__functions__,
    **general.__functions__
}