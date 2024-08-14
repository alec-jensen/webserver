from typing import Awaitable, Callable, TypeVar, Union, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")
AsyncFunction = Union[Callable[P, Awaitable[T]], Callable]