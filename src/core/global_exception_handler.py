from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # exc.errors() содержит список всех ошибок
    custom_errors = []
    for error in exc.errors():
        custom_errors.append({
            "field": error.get("loc")[-1],
            "message": "Передан некорректный формат UUID или данные не валидны",
            "get": error.get("input")
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "status": "error",
            "message": "Ошибка валидации данных",
            "details": custom_errors
        },
    )