from datetime import date
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query, Depends

from app.bookings.router import router as booking_router
from app.users.router import router as user_router
from app.hotels.router import router as hotel_router
from app.hotels.rooms.router import router as room_router

app = FastAPI()
app.include_router(booking_router)
app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(room_router)


class SHotel(BaseModel):
    name: str
    address: str
    stars: int


class HotelSearchArgs:
    def __init__(
        self,
        location: str,
        date_from: date,
        date_to: date,
        stars: Optional[int] = Query(None, ge=1, le=5),
        has_spa: Optional[bool] = None,
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


@app.get('/hotels', response_model=list[SHotel])
def get_hotels(
    search_args: HotelSearchArgs = Depends()
):
    hotels = [
        {
            "name": "Grand resort",
            "address": "Sochi",
            "stars": 5,
        }
    ]
    return hotels


