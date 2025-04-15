from enum import Enum
from dataclasses import dataclass, field


class HTTPMethod(Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"


@dataclass
class ResponseCode:
    code: int
    message: str

    def __str__(self):
        return f"{self.code} {self.message}"


class HTTPVersion(Enum):
    HTTP_1_0 = "HTTP/1.0"
    HTTP_1_1 = "HTTP/1.1"
    HTTP_2 = "HTTP/2"
    HTTP_3 = "HTTP/3"


class HTTPResponseCode(Enum):
    CONTINUE = ResponseCode(100, "Continue")
    SWITCHING_PROTOCOLS = ResponseCode(101, "Switching Protocols")
    PROCESSING = ResponseCode(102, "Processing")
    EARLY_HINTS = ResponseCode(103, "Early Hints")
    OK = ResponseCode(200, "OK")
    CREATED = ResponseCode(201, "Created")
    ACCEPTED = ResponseCode(202, "Accepted")
    NON_AUTHORITATIVE_INFORMATION = ResponseCode(
        203, "Non-Authoritative Information")
    NO_CONTENT = ResponseCode(204, "No Content")
    RESET_CONTENT = ResponseCode(205, "Reset Content")
    PARTIAL_CONTENT = ResponseCode(206, "Partial Content")
    MULTI_STATUS = ResponseCode(207, "Multi-Status")
    ALREADY_REPORTED = ResponseCode(208, "Already Reported")
    IM_USED = ResponseCode(226, "IM Used")
    MULTIPLE_CHOICES = ResponseCode(300, "Multiple Choices")
    MOVED_PERMANENTLY = ResponseCode(301, "Moved Permanently")
    FOUND = ResponseCode(302, "Found")
    SEE_OTHER = ResponseCode(303, "See Other")
    NOT_MODIFIED = ResponseCode(304, "Not Modified")
    TEMPORARY_REDIRECT = ResponseCode(307, "Temporary Redirect")
    PERMANENT_REDIRECT = ResponseCode(308, "Permanent Redirect")
    BAD_REQUEST = ResponseCode(400, "Bad Request")
    UNAUTHORIZED = ResponseCode(401, "Unauthorized")
    PAYMENT_REQUIRED = ResponseCode(402, "Payment Required")
    FORBIDDEN = ResponseCode(403, "Forbidden")
    NOT_FOUND = ResponseCode(404, "Not Found")
    METHOD_NOT_ALLOWED = ResponseCode(405, "Method Not Allowed")
    NOT_ACCEPTABLE = ResponseCode(406, "Not Acceptable")
    PROXY_AUTHENTICATION_REQUIRED = ResponseCode(
        407, "Proxy Authentication Required")
    REQUEST_TIMEOUT = ResponseCode(408, "Request Timeout")
    CONFLICT = ResponseCode(409, "Conflict")
    GONE = ResponseCode(410, "Gone")
    LENGTH_REQUIRED = ResponseCode(411, "Length Required")
    PRECONDITION_FAILED = ResponseCode(412, "Precondition Failed")
    PAYLOAD_TOO_LARGE = ResponseCode(413, "Payload Too Large")
    URI_TOO_LONG = ResponseCode(414, "URI Too Long")
    UNSUPPORTED_MEDIA_TYPE = ResponseCode(415, "Unsupported Media Type")
    RANGE_NOT_SATISFIABLE = ResponseCode(416, "Range Not Satisfiable")
    EXPECTATION_FAILED = ResponseCode(417, "Expectation Failed")
    IM_A_TEAPOT = ResponseCode(418, "I'm a teapot")
    MISDIRECTED_REQUEST = ResponseCode(421, "Misdirected Request")
    UNPROCESSABLE_ENTITY = ResponseCode(422, "Unprocessable Entity")
    LOCKED = ResponseCode(423, "Locked")
    FAILED_DEPENDENCY = ResponseCode(424, "Failed Dependency")
    TOO_EARLY = ResponseCode(425, "Too Early")
    UPGRADE_REQUIRED = ResponseCode(426, "Upgrade Required")
    PRECONDITION_REQUIRED = ResponseCode(428, "Precondition Required")
    TOO_MANY_REQUESTS = ResponseCode(429, "Too Many Requests")
    REQUEST_HEADER_FIELDS_TOO_LARGE = ResponseCode(
        431, "Request Header Fields Too Large")
    UNAVAILABLE_FOR_LEGAL_REASONS = ResponseCode(
        451, "Unavailable For Legal Reasons")
    INTERNAL_SERVER_ERROR = ResponseCode(500, "Internal Server Error")
    NOT_IMPLEMENTED = ResponseCode(501, "Not Implemented")
    BAD_GATEWAY = ResponseCode(502, "Bad Gateway")
    SERVICE_UNAVAILABLE = ResponseCode(503, "Service Unavailable")
    GATEWAY_TIMEOUT = ResponseCode(504, "Gateway Timeout")
    HTTP_VERSION_NOT_SUPPORTED = ResponseCode(
        505, "HTTP Version Not Supported")
    VARIANT_ALSO_NEGOTIATES = ResponseCode(506, "Variant Also Negotiates")
    INSUFFICIENT_STORAGE = ResponseCode(507, "Insufficient Storage")
    LOOP_DETECTED = ResponseCode(508, "Loop Detected")
    NOT_EXTENDED = ResponseCode(510, "Not Extended")
    NETWORK_AUTHENTICATION_REQUIRED = ResponseCode(
        511, "Network Authentication Required")


@dataclass
class HTTPRequest:
    http_version: HTTPVersion
    method: HTTPMethod
    path: str
    headers: dict
    cookies: dict
    body: str
    client_address: tuple
    query_params: dict | None = None

    @classmethod
    def from_string(cls, request: str, client_address: tuple):
        lines = request.split("\r\n")
        method, path, http_version = lines[0].split(" ")
        query_params = None
        if "?" in path:
            path, query_string = path.split("?")
            query_params = {}
            for param in query_string.split("&"):
                key, value = param.split("=")
                query_params[key] = value
        headers = {}
        cookies = {}
        for line in lines[1:]:
            if not line:
                break
            key, value = line.split(": ")
            headers[key] = value
            if key == "Cookie":
                for cookie in value.split("; "):
                    key, value = cookie.split("=")
                    cookies[key] = value
        
        body = lines[-1]

        # Content-Length should match body length
        if headers.get("Content-Length") is not None:
            content_length = int(headers["Content-Length"])
            if len(body) != content_length:
                raise ValueError("Content-Length does not match body length")
        
        # Check for forwarded headers
        if headers.get("X-Forwarded-For") is not None:
            client_address = (headers["X-Forwarded-For"], client_address[1])
        if headers.get("X-Forwarded-Port") is not None:
            client_address = (client_address[0], int(headers["X-Forwarded-Port"]))
        if headers.get("X-Forwarded-Proto") is not None:
            http_version = headers["X-Forwarded-Proto"]
        if headers.get("X-Real-IP") is not None:
            client_address = (headers["X-Real-IP"], client_address[1])
        
        return cls(HTTPVersion(http_version), HTTPMethod(method), path, headers, cookies, body, client_address, query_params)
    
    def __str__(self):
        return f"""HTTPRequest(
    http_version={self.http_version},
    method={self.method},
    path={self.path},
    headers={self.headers},
    cookies={self.cookies},
    body={self.body},
    client_address={self.client_address},
    query_params={self.query_params}
)"""


@dataclass
class HTTPResponse:
    body: str = ""
    headers: dict = field(default_factory=dict)
    status: HTTPResponseCode = HTTPResponseCode.OK

    # TODO: Add support for Set-Cookie header

    def to_string(self):
        if self.headers.get("Server") is None:
            self.headers["Server"] = "alec-jensen/webserver"

        headers = "\r\n".join([f"{key}: {value}" for key, value in self.headers.items()])
        return f"HTTP/1.1 {self.status.value}\r\n{headers}\r\n\r\n{self.body}"


class HTMLResponse(HTTPResponse):
    def __init__(self, body: str, headers: dict = {}, status: HTTPResponseCode = HTTPResponseCode.OK):
        super().__init__(body, headers, status)
        self.headers["Content-Type"] = "text/html"

class HTTPError:
    BAD_REQUEST = HTTPResponse("Bad Request", {}, HTTPResponseCode.BAD_REQUEST)
    UNAUTHORIZED = HTTPResponse("Unauthorized", {}, HTTPResponseCode.UNAUTHORIZED)
    PAYMENT_REQUIRED = HTTPResponse("Payment Required", {}, HTTPResponseCode.PAYMENT_REQUIRED)
    FORBIDDEN = HTTPResponse("Forbidden", {}, HTTPResponseCode.FORBIDDEN)
    NOT_FOUND = HTTPResponse("Not Found", {}, HTTPResponseCode.NOT_FOUND)
    METHOD_NOT_ALLOWED = HTTPResponse("Method Not Allowed", {}, HTTPResponseCode.METHOD_NOT_ALLOWED)
    NOT_ACCEPTABLE = HTTPResponse("Not Acceptable", {}, HTTPResponseCode.NOT_ACCEPTABLE)
    PROXY_AUTHENTICATION_REQUIRED = HTTPResponse("Proxy Authentication Required", {}, HTTPResponseCode.PROXY_AUTHENTICATION_REQUIRED)
    REQUEST_TIMEOUT = HTTPResponse("Request Timeout", {}, HTTPResponseCode.REQUEST_TIMEOUT)
    CONFLICT = HTTPResponse("Conflict", {}, HTTPResponseCode.CONFLICT)
    GONE = HTTPResponse("Gone", {}, HTTPResponseCode.GONE)
    LENGTH_REQUIRED = HTTPResponse("Length Required", {}, HTTPResponseCode.LENGTH_REQUIRED)
    PRECONDITION_FAILED = HTTPResponse("Precondition Failed", {}, HTTPResponseCode.PRECONDITION_FAILED)
    PAYLOAD_TOO_LARGE = HTTPResponse("Payload Too Large", {}, HTTPResponseCode.PAYLOAD_TOO_LARGE)
    URI_TOO_LONG = HTTPResponse("URI Too Long", {}, HTTPResponseCode.URI_TOO_LONG)
    UNSUPPORTED_MEDIA_TYPE = HTTPResponse("Unsupported Media Type", {}, HTTPResponseCode.UNSUPPORTED_MEDIA_TYPE)
    RANGE_NOT_SATISFIABLE = HTTPResponse("Range Not Satisfiable", {}, HTTPResponseCode.RANGE_NOT_SATISFIABLE)
    EXPECTATION_FAILED = HTTPResponse("Expectation Failed", {}, HTTPResponseCode.EXPECTATION_FAILED)
    IM_A_TEAPOT = HTTPResponse("I'm a teapot", {}, HTTPResponseCode.IM_A_TEAPOT)
    MISDIRECTED_REQUEST = HTTPResponse("Misdirected Request", {}, HTTPResponseCode.MISDIRECTED_REQUEST)
    UNPROCESSABLE_ENTITY = HTTPResponse("Unprocessable Entity", {}, HTTPResponseCode.UNPROCESSABLE_ENTITY)
    LOCKED = HTTPResponse("Locked", {}, HTTPResponseCode.LOCKED)
    FAILED_DEPENDENCY = HTTPResponse("Failed Dependency", {}, HTTPResponseCode.FAILED_DEPENDENCY)
    TOO_EARLY = HTTPResponse("Too Early", {}, HTTPResponseCode.TOO_EARLY)
    UPGRADE_REQUIRED = HTTPResponse("Upgrade Required", {}, HTTPResponseCode.UPGRADE_REQUIRED)
    PRECONDITION_REQUIRED = HTTPResponse("Precondition Required", {}, HTTPResponseCode.PRECONDITION_REQUIRED)
    TOO_MANY_REQUESTS = HTTPResponse("Too Many Requests", {}, HTTPResponseCode.TOO_MANY_REQUESTS)
    REQUEST_HEADER_FIELDS_TOO_LARGE = HTTPResponse("Request Header Fields Too Large", {}, HTTPResponseCode.REQUEST_HEADER_FIELDS_TOO_LARGE)
    UNAVAILABLE_FOR_LEGAL_REASONS = HTTPResponse("Unavailable For Legal Reasons", {}, HTTPResponseCode.UNAVAILABLE_FOR_LEGAL_REASONS)
    INTERNAL_SERVER_ERROR = HTTPResponse("Internal Server Error", {}, HTTPResponseCode.INTERNAL_SERVER_ERROR)
    NOT_IMPLEMENTED = HTTPResponse("Not Implemented", {}, HTTPResponseCode.NOT_IMPLEMENTED)
    BAD_GATEWAY = HTTPResponse("Bad Gateway", {}, HTTPResponseCode.BAD_GATEWAY)
    SERVICE_UNAVAILABLE = HTTPResponse("Service Unavailable", {}, HTTPResponseCode.SERVICE_UNAVAILABLE)
    GATEWAY_TIMEOUT = HTTPResponse("Gateway Timeout", {}, HTTPResponseCode.GATEWAY_TIMEOUT)
    HTTP_VERSION_NOT_SUPPORTED = HTTPResponse("HTTP Version Not Supported", {}, HTTPResponseCode.HTTP_VERSION_NOT_SUPPORTED)
    VARIANT_ALSO_NEGOTIATES = HTTPResponse("Variant Also Negotiates", {}, HTTPResponseCode.VARIANT_ALSO_NEGOTIATES)
    INSUFFICIENT_STORAGE = HTTPResponse("Insufficient Storage", {}, HTTPResponseCode.INSUFFICIENT_STORAGE)
    LOOP_DETECTED = HTTPResponse("Loop Detected", {}, HTTPResponseCode.LOOP_DETECTED)
    NOT_EXTENDED = HTTPResponse("Not Extended", {}, HTTPResponseCode.NOT_EXTENDED)
    NETWORK_AUTHENTICATION_REQUIRED = HTTPResponse("Network Authentication Required", {}, HTTPResponseCode.NETWORK_AUTHENTICATION_REQUIRED)
