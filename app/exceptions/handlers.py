from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.exceptions.base import AppException
from app.exceptions.codes import ErrorCode
from app.logger import logger

from http import HTTPStatus

def register_exception_handler(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ) -> JSONResponse:
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success" : False,
                "error" :{
                    "code" : exc.error_code,
                    "message" : exc.message,
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": ErrorCode.VALIDATION_ERROR,
                    "message": "Request validation failed.",
                    "details": jsonable_encoder(exc.errors()),
                },
            },
        )
    
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:

        logger.exception(
            "Unhandled exception while processing %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": ErrorCode.INTERNAL_SERVER_ERROR,
                    "message": "An unexpected error occurred.",
                },
            },
        )


