from typing import Awaitable, Callable, TypeVar
from typing_extensions import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")
AsyncFunction = Callable[P, Awaitable[T]]