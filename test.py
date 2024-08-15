from webserver import Webserver, Request

server = Webserver("0.0.0.0", 8080)

@server.get("/{test}/fetch_one")
def fetch_one(request: Request, test: str):
    return request.body

server.start()