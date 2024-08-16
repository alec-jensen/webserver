from webserver import Webserver, Request

server = Webserver("0.0.0.0", 8080)

@server.get("/{collection}/find_one")
async def find_one(request: Request, collection: str):
    print(request.headers)
    return request.body

@server.post("/{collection}/insert_one")
async def insert_one(request: Request, collection: str):
    print(request.headers)
    return request.body

server.start()