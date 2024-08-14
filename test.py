from webserver import Webserver
# Set the directory to serve static files from (default is None)
server.static_files_dir = "static"

# Variables can be added to the path
@server.get("/{name}/hello")
async def hello(name: str):
    return f"Hello, {name}!"

# Once this is called, the server will start listening for requests
server.start()

class TestClass:
    server = Webserver("0.0.0.0", 8080)

    def __init__(self) -> None:
        self.server.start()