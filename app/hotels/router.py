from datetime import date

from fastapi import APIRouter, Depends

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelAll

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotelAll]:
    return await HotelDAO.get_all(location=location, date_from=date_from, date_to=date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotel:
    return await HotelDAO.find_by_id(model_id=hotel_id)