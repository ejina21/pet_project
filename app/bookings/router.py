from datetime import date

from fastapi import APIRouter, Depends
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.get_all(user_id=user.id)


@router.get("/{booking_id}")
async def get_bookings(booking_id: int) -> SBooking:
    result = await BookingDAO.find_by_id(booking_id)
    return result


@router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add_row(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return booking
