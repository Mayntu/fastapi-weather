from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.exceptions import WeatherException


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_errors = []
    for error in exc.errors():
        field_path = " - ".join([str(x) for x in error.get("loc")])
        
        custom_errors.append({
            "field": field_path,
            "message": error.get("msg"),
            "type": error.get("type"),
            "input": error.get("input")
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "status": "validation_error",
            "message": "Введенные данные содержат ошибки",
            "errors": custom_errors
        },
    )

async def weather_exception_handler(request: Request, exc: WeatherException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "code": exc.__class__.__name__
        },
    )