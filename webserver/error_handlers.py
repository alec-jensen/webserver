from abc import ABC, abstractmethod

from webserver.enums import HTTPResponse, HTTPError


class BaseErrorHandler(ABC):
    """Base class for error handlers."""

    @abstractmethod
    def handle(self, error: Exception) -> HTTPResponse:
        raise NotImplementedError("Subclasses must implement this method")


class DefaultErrorHandler(BaseErrorHandler):
    """Default error handler that returns a 500 Internal Server Error response."""

    def handle(self, error):
        return HTTPError.INTERNAL_SERVER_ERROR


class ExceptionAwareErrorHandler(BaseErrorHandler):
    """
    Error handler that is aware of exceptions and can handle them accordingly.
    This is useful for handling specific exceptions and returning appropriate HTTP responses.
    For example, if a ValueError is raised, it can return a 400 Bad Request response.
    """

    def handle(self, error):
        if isinstance(error, ValueError) or isinstance(error, TypeError):
            return HTTPError.BAD_REQUEST
        elif isinstance(error, FileNotFoundError):
            return HTTPError.NOT_FOUND

        return HTTPError.INTERNAL_SERVER_ERROR
