from datetime import date

from sqlalchemy import and_, func, insert, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add_row(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from,
                        Bookings.room_id == room_id,
                    )
                )
                .cte("booked_rooms")
            )
            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.id, booked_rooms.c.room_id)
            )
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            if rooms_left > 0:
                get_price = select(Rooms.price).where(Rooms.id == room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings.__table__.columns)
                )
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.mappings().one_or_none()
            else:
                return None

    @classmethod
    async def get_all(cls, user_id: int):
        async with async_session_maker() as session:
            get_bookings = (
                select(
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                .where(Bookings.user_id == user_id)
            )
            bookings = await session.execute(get_bookings)
            return bookings.mappings().all()
