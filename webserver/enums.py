from enum import Enum
from dataclasses import dataclass, field


class Methods(Enum):
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


class ResponseCodes(Enum):
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
class Response:
    body: str
    headers: dict = field(default_factory=dict)
    status: ResponseCodes = ResponseCodes.OK

    def to_string(self):
        headers = "\r\n".join([f"{key}: {value}" for key, value in self.headers.items()])
        return f"HTTP/1.1 {self.status.value}\r\n{headers}\r\n\r\n{self.body}"


class HTMLResponse(Response):
    def __init__(self, body: str, headers: dict = {}, status: ResponseCodes = ResponseCodes.OK):
        super().__init__(body, headers, status)
        self.headers["Content-Type"] = "text/html"

class HTTPErrors:
    BAD_REQUEST = Response("Bad Request", {}, ResponseCodes.BAD_REQUEST)
    UNAUTHORIZED = Response("Unauthorized", {}, ResponseCodes.UNAUTHORIZED)
    PAYMENT_REQUIRED = Response("Payment Required", {}, ResponseCodes.PAYMENT_REQUIRED)
    FORBIDDEN = Response("Forbidden", {}, ResponseCodes.FORBIDDEN)
    NOT_FOUND = Response("Not Found", {}, ResponseCodes.NOT_FOUND)
    METHOD_NOT_ALLOWED = Response("Method Not Allowed", {}, ResponseCodes.METHOD_NOT_ALLOWED)
    NOT_ACCEPTABLE = Response("Not Acceptable", {}, ResponseCodes.NOT_ACCEPTABLE)
    PROXY_AUTHENTICATION_REQUIRED = Response("Proxy Authentication Required", {}, ResponseCodes.PROXY_AUTHENTICATION_REQUIRED)
    REQUEST_TIMEOUT = Response("Request Timeout", {}, ResponseCodes.REQUEST_TIMEOUT)
    CONFLICT = Response("Conflict", {}, ResponseCodes.CONFLICT)
    GONE = Response("Gone", {}, ResponseCodes.GONE)
    LENGTH_REQUIRED = Response("Length Required", {}, ResponseCodes.LENGTH_REQUIRED)
    PRECONDITION_FAILED = Response("Precondition Failed", {}, ResponseCodes.PRECONDITION_FAILED)
    PAYLOAD_TOO_LARGE = Response("Payload Too Large", {}, ResponseCodes.PAYLOAD_TOO_LARGE)
    URI_TOO_LONG = Response("URI Too Long", {}, ResponseCodes.URI_TOO_LONG)
    UNSUPPORTED_MEDIA_TYPE = Response("Unsupported Media Type", {}, ResponseCodes.UNSUPPORTED_MEDIA_TYPE)
    RANGE_NOT_SATISFIABLE = Response("Range Not Satisfiable", {}, ResponseCodes.RANGE_NOT_SATISFIABLE)
    EXPECTATION_FAILED = Response("Expectation Failed", {}, ResponseCodes.EXPECTATION_FAILED)
    IM_A_TEAPOT = Response("I'm a teapot", {}, ResponseCodes.IM_A_TEAPOT)
    MISDIRECTED_REQUEST = Response("Misdirected Request", {}, ResponseCodes.MISDIRECTED_REQUEST)
    UNPROCESSABLE_ENTITY = Response("Unprocessable Entity", {}, ResponseCodes.UNPROCESSABLE_ENTITY)
    LOCKED = Response("Locked", {}, ResponseCodes.LOCKED)
    FAILED_DEPENDENCY = Response("Failed Dependency", {}, ResponseCodes.FAILED_DEPENDENCY)
    TOO_EARLY = Response("Too Early", {}, ResponseCodes.TOO_EARLY)
    UPGRADE_REQUIRED = Response("Upgrade Required", {}, ResponseCodes.UPGRADE_REQUIRED)
    PRECONDITION_REQUIRED = Response("Precondition Required", {}, ResponseCodes.PRECONDITION_REQUIRED)
    TOO_MANY_REQUESTS = Response("Too Many Requests", {}, ResponseCodes.TOO_MANY_REQUESTS)
    REQUEST_HEADER_FIELDS_TOO_LARGE = Response("Request Header Fields Too Large", {}, ResponseCodes.REQUEST_HEADER_FIELDS_TOO_LARGE)
    UNAVAILABLE_FOR_LEGAL_REASONS = Response("Unavailable For Legal Reasons", {}, ResponseCodes.UNAVAILABLE_FOR_LEGAL_REASONS)
    INTERNAL_SERVER_ERROR = Response("Internal Server Error", {}, ResponseCodes.INTERNAL_SERVER_ERROR)
    NOT_IMPLEMENTED = Response("Not Implemented", {}, ResponseCodes.NOT_IMPLEMENTED)
    BAD_GATEWAY = Response("Bad Gateway", {}, ResponseCodes.BAD_GATEWAY)
    SERVICE_UNAVAILABLE = Response("Service Unavailable", {}, ResponseCodes.SERVICE_UNAVAILABLE)
    GATEWAY_TIMEOUT = Response("Gateway Timeout", {}, ResponseCodes.GATEWAY_TIMEOUT)
    HTTP_VERSION_NOT_SUPPORTED = Response("HTTP Version Not Supported", {}, ResponseCodes.HTTP_VERSION_NOT_SUPPORTED)
    VARIANT_ALSO_NEGOTIATES = Response("Variant Also Negotiates", {}, ResponseCodes.VARIANT_ALSO_NEGOTIATES)
    INSUFFICIENT_STORAGE = Response("Insufficient Storage", {}, ResponseCodes.INSUFFICIENT_STORAGE)
    LOOP_DETECTED = Response("Loop Detected", {}, ResponseCodes.LOOP_DETECTED)
    NOT_EXTENDED = Response("Not Extended", {}, ResponseCodes.NOT_EXTENDED)
    NETWORK_AUTHENTICATION_REQUIRED = Response("Network Authentication Required", {}, ResponseCodes.NETWORK_AUTHENTICATION_REQUIRED)