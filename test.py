from webserver import Webserver
from webserver.enums import HTTPRequest
from webserver.error_handlers import ExceptionAwareErrorHandler

server = Webserver("0.0.0.0", 8080, error_handler=ExceptionAwareErrorHandler())

@server.get("/{collection}/find_one")
async def insert_one(request: HTTPRequest, collection: str):
    print(request.headers)
    return request.body

@server.get("/test")
async def test(request: HTTPRequest):
    return "Hello, World!"

server.start()