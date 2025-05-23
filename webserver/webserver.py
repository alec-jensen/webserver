from dataclasses import dataclass
import logging
import datetime
import traceback
import asyncio
import os
from typing import Optional

from webserver.routes import RouteTree, split_path
from webserver.enums import (
    HTTPMethod,
    HTTPResponseCode,
    HTTPResponse,
    HTTPError,
    HTTPVersion,
    HTTPRequest,
)
from webserver.typedefs import AsyncFunction
from webserver.log_formatter import LogFormatter, LogFileFormatter
from webserver.exceptions import MethodNotAllowed
from webserver.error_handlers import BaseErrorHandler, DefaultErrorHandler

logFormatter = LogFormatter()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logFileFormatter = LogFileFormatter()
fileHandler = logging.FileHandler("webserver.log")
fileHandler.setFormatter(logFileFormatter)
logger.addHandler(fileHandler)


class Webserver:
    def __init__(
        self,
        host,
        port,
        static_files_dir: Optional[str] = None,
        error_handler: Optional[BaseErrorHandler] = DefaultErrorHandler(),
    ):
        self.host = host
        self.port = port
        self.timeout = 1.2  # seconds
        self.route_tree: RouteTree = RouteTree()
        self.static_files_dir: Optional[str] = static_files_dir

        if not isinstance(error_handler, BaseErrorHandler):
            raise TypeError("error_handler must be an instance of BaseErrorHandler")

        self.error_handler: BaseErrorHandler = error_handler

    def _send(self, writer, response: HTTPResponse):
        writer.write(response.to_string().encode())
        writer.close()

    def start(self):
        if self.static_files_dir is not None:
            self.static_files_dir = os.path.abspath(self.static_files_dir)

        self.running = True
        asyncio.run(self._run())

    async def _run(self):
        self.server = await asyncio.start_server(self._recv, self.host, self.port)
        logging.info(f"Server started on {self.host}:{self.port}")

        try:
            async with self.server:
                await self.server.serve_forever()
        except (KeyboardInterrupt, asyncio.CancelledError):
            logging.info("Shutting down server")
        except Exception:
            logging.error(f"Error running server:\n{traceback.format_exc().strip()}")
        finally:
            self.server.close()
            await self.server.wait_closed()

    async def _recv(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client_address = writer.get_extra_info("peername")
        MAX_REQUEST_SIZE = 1024 * 1024 * 30  # 30 MB
        try:
            async with asyncio.timeout(self.timeout):
                _request = (await reader.read(MAX_REQUEST_SIZE)).decode()
        except asyncio.TimeoutError:
            logging.error(f"Timed out receiving request from {client_address}")
            self._send(writer, HTTPError.REQUEST_TIMEOUT)
            return

        try:
            request = HTTPRequest.from_string(_request, client_address)
        except Exception:
            logging.warning(f"Bad request from {client_address}")
            logging.debug(f"Error parsing request:\n{traceback.format_exc().strip()}")
            try:
                self._send(writer, HTTPError.BAD_REQUEST)
            except Exception:
                logging.info(
                    f"Error sending response:\n{traceback.format_exc().strip()}"
                )
            return

        request_response_code = HTTPResponseCode.OK

        try:
            route = self.route_tree.get_route(request.path, request.method)
        except MethodNotAllowed:
            self._send(writer, HTTPError.METHOD_NOT_ALLOWED)
            return

        if route is None and self.static_files_dir:
            file_path = os.path.join(self.static_files_dir, request.path[1:])
            file_path = os.path.abspath(file_path)
            logging.debug(f"Checking for static file {file_path}")
            logging.debug(f"Static files dir: {self.static_files_dir}")

            if (
                not os.path.commonprefix([self.static_files_dir, file_path])
                == self.static_files_dir
            ):
                self._send(writer, HTTPError.FORBIDDEN)
                return

            if os.path.exists(file_path):
                # deepcode ignore PT: the code above prevents path traversal
                with open(file_path, "r") as file:
                    self._send(writer, HTTPResponse(file.read()))
                return
        if route is not None:
            path_vars = []
            for var in route.path_vars:
                path_vars.append(var["name"])
            handler_args = []
            for arg in route.handler_args:
                if (
                    arg == "request"
                    or route.handler_signature.parameters[arg].annotation == HTTPRequest
                ):
                    handler_args.append(request)
                elif arg in path_vars:
                    # value = split_path(request.path)[var["pos"]]
                    value = split_path(request.path)[path_vars.index(arg)]
                    param_type = route.handler_signature.parameters[arg].annotation
                    try:
                        handler_args.append(param_type(value))
                    except ValueError:
                        self._send(writer, HTTPError.BAD_REQUEST)
                        return
                    logging.debug(f"Found path variable {arg} with value {value}")
                else:
                    if request.query_params is not None:
                        if arg in request.query_params.keys():
                            value = request.query_params[arg]
                            param_type = route.handler_signature.parameters[
                                arg
                            ].annotation
                            try:
                                handler_args.append(param_type(value))
                            except ValueError:
                                self._send(writer, HTTPError.BAD_REQUEST)
                                return

            try:
                if callable(route.handler):
                    response = await route.handler(*handler_args)
                elif asyncio.iscoroutinefunction(route.handler):
                    response = await route.handler(*handler_args)
                else:
                    raise ValueError(
                        f"Handler for route {request.method.value} {request.path} is not a function"
                    )
                request_response_code = HTTPResponseCode.OK
                if issubclass(type(response), HTTPResponse):
                    request_response_code = response.status
                    self._send(writer, response)
                else:
                    self._send(writer, HTTPResponse(response))
            except Exception as e:
                logging.error(
                    f"Error handling request:\n{traceback.format_exc().strip()}"
                )

                response = self.error_handler.handle(e)

                if isinstance(response, HTTPResponse):
                    request_response_code = response.status
                    self._send(writer, response)
                else:
                    request_response_code = HTTPResponseCode.INTERNAL_SERVER_ERROR
                    self._send(writer, HTTPError.INTERNAL_SERVER_ERROR)
        else:
            request_response_code = HTTPResponseCode.NOT_FOUND
            self._send(writer, HTTPError.NOT_FOUND)

        logging.info(
            f"{request.client_address[0]} [{datetime.datetime.now()}] {request.method.value} {request.path} {request_response_code.value}"
        )

    def _register_route(self, path: str, method: HTTPMethod, handler: AsyncFunction):
        try:
            if self.route_tree.get_route(path, method):
                raise ValueError(f"Route {method.value} {path} already exists")
        except MethodNotAllowed:
            # This is expected if the method is not allowed
            pass

        self.route_tree.add_route(path, method, handler)

    def get(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, HTTPMethod.GET, handler)

        return wrapper

    def head(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, HTTPMethod.HEAD, handler)

        return wrapper

    def post(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, HTTPMethod.POST, handler)

        return wrapper

    def put(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, HTTPMethod.PUT, handler)

        return wrapper

    def delete(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, HTTPMethod.DELETE, handler)

        return wrapper

    def connect(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, HTTPMethod.CONNECT, handler)

        return wrapper

    def options(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, HTTPMethod.OPTIONS, handler)

        return wrapper

    def trace(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, HTTPMethod.TRACE, handler)

        return wrapper

    def patch(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, HTTPMethod.PATCH, handler)

        return wrapper
