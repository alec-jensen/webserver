from webserver import Webserver, Request, HTMLResponse, html, head, title, link, body, h1, p, div, a

# Start the server on 0.0.0.0 (all interfaces) on port 8080
server = Webserver("0.0.0.0", 8080)
# Set the directory to serve static files from (default is None)
server.static_files_dir = "static"

# Variables can be added to the path
@server.get("/{name}/hello")
async def hello(name: str):
    return f"Hello, {name}!"

# Once this is called, the server will start listening for requests
server.start()