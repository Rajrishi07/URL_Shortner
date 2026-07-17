from app.exceptions.codes import ErrorCode
from app.exceptions.base import AppException
from http import HTTPStatus

class URLNotFoundException(AppException):

    def __init__(self, short_code: str):
        super().__init__(
            message=f"Short URL '{short_code}' does not exist.",
            error_code=ErrorCode.URL_NOT_FOUND,
            status_code=HTTPStatus.NOT_FOUND,
        )

class DuplicateAliasException(AppException):

    def __init__(self, short_code: str):
        super().__init__(
            message=f"Short URL '{short_code}' already exists.",
            error_code=ErrorCode.DUPLICATE_ALIAS,
            status_code=HTTPStatus.CONFLICT,
        )

class URLExpiredException(AppException):

    def __init__(self, short_code: str):
        super().__init__(
            message=f"Short URL '{short_code}' has expired.",
            error_code=ErrorCode.URL_EXPIRED,
            status_code=HTTPStatus.GONE,
        )

class InvalidURLException(AppException):

    def __init__(self, short_code: str):
        super().__init__(
            message=f"Short URL '{short_code}' is not a valid alias.",
            error_code=ErrorCode.INVALID_URL,
            status_code=HTTPStatus.BAD_REQUEST,
        )