from datetime import date

from fastapi import APIRouter, Depends, status
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingInfo, SNewBooking
from app.config import settings
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingDAO.get_all(user_id=user.id)


@router.get("/{booking_id}")
async def get_booking(booking_id: int) -> SBooking:
    result = await BookingDAO.find_by_id(booking_id)
    return result


@router.post("", status_code=201)
async def add_booking(
    booking: SNewBooking, user: Users = Depends(get_current_user)
) -> SBooking:
    booking = await BookingDAO.add_row(user.id, booking.room_id, booking.date_from, booking.date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, settings.SMTP_USER)
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    return await BookingDAO.delete(id=booking_id)
