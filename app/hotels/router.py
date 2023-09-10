from datetime import date, datetime

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelAll

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
@cache(expire=20)
async def get_hotels(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}")
) -> list[SHotelAll]:
    return await HotelDAO.get_all(location=location, date_from=date_from, date_to=date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotel:
    return await HotelDAO.find_by_id(model_id=hotel_id)