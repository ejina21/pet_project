from datetime import date

from fastapi import APIRouter, Depends, status
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingAll
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingAll]:
    return await BookingDAO.get_all(user_id=user.id)


@router.get("/{booking_id}")
async def get_booking(booking_id: int) -> SBooking:
    result = await BookingDAO.find_by_id(booking_id)
    return result


@router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)) -> SBooking:
    booking = await BookingDAO.add_row(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    return await BookingDAO.delete_by_id(model_id=booking_id)

