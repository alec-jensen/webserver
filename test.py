from webserver import Webserver, HTTPRequest

server = Webserver("0.0.0.0", 8080)

@server.post("/{collection}/find_one")
async def find_one(request: HTTPRequest, collection: str):
    print(request)
    
    return request.body

@server.get("/{collection}/find_one")
async def insert_one(request: HTTPRequest, collection: str):
    print(request.headers)
    return request.body

server.start()