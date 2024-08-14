from webserver import Webserver

server = Webserver("0.0.0.0", 8080)

# Variables can be added to the path
@server.get("/{name}/greet")
async def hello(request, name: str):
    return f"Hello, {name}!"

# Once this is called, the server will start listening for requests
server.start()