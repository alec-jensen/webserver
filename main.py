from dataclasses import dataclass
import logging
import datetime
import traceback
import asyncio

from routes import RouteTree, RouteNode
from enums import Methods, ResponseCodes
from typedefs import AsyncFunction
from log_formatter import LogFormatter, LogFileFormatter

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

    @classmethod
    def from_string(cls, request: str, client_address: tuple):
        lines = request.split("\r\n")
        method, path, _ = lines[0].split(" ")
        headers = {}
        for line in lines[1:]:
            if not line:
                break
            key, value = line.split(": ")
            headers[key] = value
        body = lines[-1]
        return cls(Methods[method], path, headers, body, client_address)


class Webserver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.timeout = 1200
        self.route_tree: RouteTree = RouteTree()

    def _send(self, writer, responsecode: ResponseCodes, response: str):
        http_response = f"""\
HTTP/1.1 {responsecode}

{response}
"""
        writer.write(http_response.encode())
        writer.close()

    def start(self):
        asyncio.run(self._run())

    async def _run(self):
        server = await asyncio.start_server(self._loop, self.host, self.port)
        logging.info(f"Server started on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

    async def _loop(self, reader, writer):
        client_address = writer.get_extra_info("peername")
        MAX_REQUEST_SIZE = 1024 * 1024 * 30  # 30 MB
        _request = (await reader.read(MAX_REQUEST_SIZE)).decode()

        try:
            request = Request.from_string(_request, client_address)
        except Exception as e:
            logging.warning(f"Bad request from {client_address}")
            logging.debug(f"Error parsing request:\n{
                          traceback.format_exc().strip()}")
            try:
                self._send(writer, ResponseCodes.BAD_REQUEST, "Bad Request")
            except Exception as e:
                logging.info(f"Error sending response:\n{traceback.format_exc().strip()}")
            return

        request_response_code = ResponseCodes.OK

        route = self.route_tree.get_route(request.path, request.method)
        if route is not None:
            logging.debug(f"Found route {route}")
            handler_args = []
            for arg in route.handler_args:
                if arg == "request":
                    handler_args.append(request)

            try:
                response = await route.handler(*handler_args) # type: ignore (im guessing a pylance bug)
                request_response_code = ResponseCodes.OK
                self._send(writer, ResponseCodes.OK, response)
            except Exception as e:
                logging.error(f"Error handling request:\n{traceback.format_exc().strip()}")
                request_response_code = ResponseCodes.INTERNAL_SERVER_ERROR
                self._send(writer,
                            ResponseCodes.INTERNAL_SERVER_ERROR,
                            "Internal Server Error")
        else:
            request_response_code = ResponseCodes.NOT_FOUND
            self._send(writer, ResponseCodes.NOT_FOUND, "Not Found")

        logging.info(f"{request.client_address[0]} [{datetime.datetime.now()}] \
                     {request.method.value} {request.path} {request_response_code.value}")

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


if __name__ == "__main__":
    server = Webserver("0.0.0.0", 8080)

    @server.get("/")
    async def index():
        return "Hello, World!"

    @server.get("/myip")
    async def myip(request: Request):
        return f"Your IP is: {request.client_address[0]}"
    
    @server.get("/myip/raw")
    async def myip_raw(request: Request):
        return request.client_address[0]

    @server.post("/echo")
    async def echo(request: Request):
        return request.body

    server.start()
