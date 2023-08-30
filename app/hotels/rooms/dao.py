from datetime import date

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms

from sqlalchemy import select, and_, func


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_all(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = select(
                func.count(Bookings.id).label('booked'), Bookings.room_id
            ).where(
                and_(
                    Bookings.date_from <= date_to,
                    Bookings.date_to >= date_from,
                )
            ).group_by(Bookings.room_id).cte("booked_rooms")

            get_rooms = select(
                Rooms.id, Rooms.hotel_id, Rooms.name, Rooms.description, Rooms.services,
                Rooms.price, Rooms.quantity, Rooms.image_id,
                ((date_to - date_from) * Rooms.price).label('total_cost'),
                (Rooms.quantity - func.coalesce(booked_rooms.c.booked, 0)).label('rooms_left')
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id,
                isouter=True
            ).where(
                and_(
                    Rooms.quantity - func.coalesce(booked_rooms.c.booked, 0) > 0,
                    Rooms.hotel_id == hotel_id
                )
            )
            rooms = await session.execute(get_rooms)
            return rooms.mappings().all()