from datetime import date

from fastapi import APIRouter, Depends

from app.hotels.dao import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date):
    return await HotelDAO.get_all(location=location, date_from=date_from, date_to=date_to)