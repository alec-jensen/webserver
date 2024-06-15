I was bored so I wrote a webserver in python.

    from webserver import Webserver, Request, HTMLResponse, html, head, title, link, body, h1, p, div, a

    # Start the server on 0.0.0.0 (all interfaces) on port 8080
    server = Webserver("0.0.0.0", 8080)
    # Set the directory to serve static files from (default is None)
    server.static_files_dir = "static"

    # Get request to the root path
    @server.get("/")
    async def index():
        # Return an HTML response
        return HTMLResponse(
            # These functions will directly translate to HTML tags
            # All HTML tags are supported
            html(
                head(
                    title("Index"),
                    # Link the CSS file from the static directory
                    link(attr={"rel": "stylesheet", "href": "/style.css"})
                ),
                body(
                    h1("Index"),
                    p("This is the index page"),
                    div(
                        a("GitHub repo", attr={"href": "https://github.com/alec-jensen/webserver", "target": "_blank"}),
                        a("What's My IP?", attr={"href": "/myip"}),
                        attr={"id": "links"}
                    )
                )
            )
        )

    # To get the Request object, add it as an argument
    @server.get("/myip")
    async def myip(request: Request):
        return f"Your IP is: {request.client_address[0]}"

    # All types of requests are supported
    @server.post("/echo")
    async def echo(request: Request):
        return request.body

    # Once this is called, the server will start listening for requests
    server.start()