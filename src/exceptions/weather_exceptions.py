from fastapi import status

class WeatherException(Exception):
    """Базовый класс для всех ошибок нашего приложения"""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class WeatherNotFoundException(WeatherException):
    """Погода не найдена"""
    def __init__(self, city: str = None):
        message = f"Weather data for {city} not found" if city else "Weather not found"
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)