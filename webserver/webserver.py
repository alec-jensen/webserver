from dataclasses import dataclass
import logging
import datetime
import traceback
import asyncio
import os

from webserver.routes import RouteTree, split_path
from webserver.enums import Methods, ResponseCodes, Response, HTTPErrors
from webserver.typedefs import AsyncFunction, AsyncFunction
from webserver.log_formatter import LogFormatter, LogFileFormatter

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


@dataclass
class Request:
    method: Methods
    path: str
    headers: dict
    body: str
    client_address: tuple
    query_params: dict | None = None

    @classmethod
    def from_string(cls, request: str, client_address: tuple):
        lines = request.split("\r\n")
        method, path, _ = lines[0].split(" ")
        query_params = None
        if "?" in path:
            path, query_string = path.split("?")
            query_params = {}
            for param in query_string.split("&"):
                key, value = param.split("=")
                query_params[key] = value
        headers = {}
        for line in lines[1:]:
            if not line:
                break
            key, value = line.split(": ")
            headers[key] = value
        body = lines[-1]
        return cls(Methods[method], path, headers, body, client_address, query_params)


class Webserver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.timeout = 1.2 # seconds
        self.route_tree: RouteTree = RouteTree()
        self.static_files_dir: str | None = None

    def _send(self, writer, response: Response):
        writer.write(response.to_string().encode())
        writer.close()

    def start(self):
        if self.static_files_dir is not None:
            self.static_files_dir = os.path.abspath(self.static_files_dir)

        asyncio.run(self._run())

    async def _run(self):
        server = await asyncio.start_server(self._recv, self.host, self.port)
        logging.info(f"Server started on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

    async def _recv(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client_address = writer.get_extra_info("peername")
        MAX_REQUEST_SIZE = 1024 * 1024 * 30  # 30 MB
        try:
            async with asyncio.timeout(self.timeout):
                _request = (await reader.read(MAX_REQUEST_SIZE)).decode()
        except asyncio.TimeoutError:
            logging.error(f"Timed out receiving request from {client_address}")
            self._send(writer, HTTPErrors.REQUEST_TIMEOUT)
            return

        try:
            request = Request.from_string(_request, client_address)
        except Exception:
            logging.warning(f"Bad request from {client_address}")
            logging.debug(f"Error parsing request:\n{traceback.format_exc().strip()}")
            try:
                self._send(writer, HTTPErrors.BAD_REQUEST)
            except Exception:
                logging.info(f"Error sending response:\n{traceback.format_exc().strip()}")
            return

        request_response_code = ResponseCodes.OK

        route = self.route_tree.get_route(request.path, request.method)
        if route is None and self.static_files_dir:
            file_path = os.path.join(self.static_files_dir, request.path[1:])
            file_path = os.path.abspath(file_path)
            logging.debug(f"Checking for static file {file_path}")
            logging.debug(f"Static files dir: {self.static_files_dir}")
            
            if not os.path.commonprefix([self.static_files_dir, file_path]) == self.static_files_dir:
                self._send(writer, HTTPErrors.FORBIDDEN)
                return
            
            if os.path.exists(file_path):
                # deepcode ignore PT: the code above prevents path traversal
                with open(file_path, "r") as file:
                    self._send(writer, Response(file.read()))
                return
        if route is not None:
            path_vars = []
            for var in route.path_vars:
                path_vars.append(var["name"])
            handler_args = []
            for arg in route.handler_args:
                if arg == "request" and route.handler_signature.parameters[arg].annotation == Request:
                    handler_args.append(request)
                elif arg in path_vars:
                    value = split_path(request.path)[var["pos"]]
                    param_type = route.handler_signature.parameters[arg].annotation
                    handler_args.append(param_type(value))
                else:
                    if request.query_params is not None:
                        if arg in request.query_params.keys():
                            value = request.query_params[arg]
                            param_type = route.handler_signature.parameters[arg].annotation
                            try:
                                handler_args.append(param_type(value))
                            except ValueError:
                                self._send(writer, HTTPErrors.BAD_REQUEST)
                                return

            try:
                response = await route.handler(*handler_args) # type: ignore (im guessing a pylance bug)
                request_response_code = ResponseCodes.OK
                if issubclass(type(response), Response):
                    request_response_code = response.status
                    self._send(writer, response)
                else:
                    self._send(writer, Response(response))
                
            except Exception as e:
                logging.error(f"Error handling request:\n{traceback.format_exc().strip()}")
                request_response_code = ResponseCodes.INTERNAL_SERVER_ERROR
                self._send(writer, HTTPErrors.INTERNAL_SERVER_ERROR)
        else:
            request_response_code = ResponseCodes.NOT_FOUND
            self._send(writer, HTTPErrors.NOT_FOUND)

        logging.info(f"{request.client_address[0]} [{datetime.datetime.now()}] {request.method.value} {request.path} {request_response_code.value}")

    def _register_route(self, path: str, method: Methods, handler: AsyncFunction):
        if self.route_tree.get_route(path, method):
            raise ValueError(f"Route {method.value} {path} already exists")

        self.route_tree.add_route(path, method, handler)

    def get(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, Methods.GET, handler)
        return wrapper

    def head(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, Methods.HEAD, handler)
        return wrapper

    def post(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, Methods.POST, handler)
        return wrapper

    def put(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, Methods.PUT, handler)
        return wrapper

    def delete(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, Methods.DELETE, handler)
        return wrapper

    def connect(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, Methods.CONNECT, handler)
        return wrapper

    def options(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, Methods.OPTIONS, handler)
        return wrapper

    def trace(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, Methods.TRACE, handler)
        return wrapper

    def patch(self, path: str):
        def wrapper(handler: AsyncFunction):
            self._register_route(path, Methods.PATCH, handler)
        return wrapper
