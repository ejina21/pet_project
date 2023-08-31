from datetime import date

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels

from sqlalchemy import select, func, and_

from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_all(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_hotels = select(
                func.count(Bookings.id).label('booked'), Rooms.hotel_id
            ).join(
                Rooms, Rooms.id == Bookings.room_id, isouter=True
            ).where(
                and_(
                    Bookings.date_from <= date_to,
                    Bookings.date_to >= date_from,
                )
            ).group_by(Rooms.hotel_id).cte("booked_hotels")

            get_hotels = select(
                Hotels.id, Hotels.name, Hotels.location, Hotels.services, Hotels.rooms_quantity,
                Hotels.image_id, (Hotels.rooms_quantity - func.coalesce(booked_hotels.c.booked, 0)).label('rooms_left')
            ).select_from(Hotels).join(
                booked_hotels, booked_hotels.c.hotel_id == Hotels.id,
                isouter=True
            ).where(
                and_(
                    Hotels.rooms_quantity - func.coalesce(booked_hotels.c.booked, 0) > 0,
                    Hotels.location.like(f"%{location}%"),
                )
            )
            hotels = await session.execute(get_hotels)
            return hotels.mappings().all()