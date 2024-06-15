from webserver import Webserver, Request, HTMLResponse, html, head, title, link, body, h1, p, div, a

server = Webserver("0.0.0.0", 8080)
server.static_files_dir = "static"

@server.get("/")
async def index():
    return HTMLResponse(
        html(
            head(
                title("Index"),
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