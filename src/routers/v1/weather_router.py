from fastapi import APIRouter

router : APIRouter = APIRouter(prefix="/weather")

@router.get("")
async def weather_list() -> list:
    return []