from enum import Enum
from dataclasses import dataclass

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