from typing import Awaitable, Callable, TypeVar, Union
from typing_extensions import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")
AsyncFunction = Union[Callable[P, Awaitable[T]], Callable]