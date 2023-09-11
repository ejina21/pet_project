import pytest
from httpx import AsyncClient
from datetime import datetime
from app.bookings.dao import BookingDAO


@pytest.mark.parametrize(
    "room_id,date_from,date_to,booked_rooms,status_code",
    [
        (4, "2030-05-01", "2030-05-15", 3, 201),
        (4, "2030-05-02", "2030-05-16", 4, 201),
        (4, "2030-05-03", "2030-05-17", 5, 201),
        (4, "2030-05-04", "2030-05-18", 6, 201),
        (4, "2030-05-05", "2030-05-19", 7, 201),
        (4, "2030-05-06", "2030-05-20", 8, 201),
        (4, "2030-05-07", "2030-05-21", 9, 201),
        (4, "2030-05-08", "2030-05-22", 10, 201),
        (4, "2030-05-09", "2030-05-23", 10, 409),
        (4, "2030-05-10", "2030-05-24", 10, 409),
    ],
)
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    booked_rooms,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/api/v1/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code

    response = await authenticated_ac.get("/api/v1/bookings")
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_booking(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/api/v1/bookings")
    existing_bookings = [booking["id"] for booking in response.json()]
    for booking_id in existing_bookings:
        response = await authenticated_ac.delete(
            f"/api/v1/bookings/{booking_id}",
        )

    response = await authenticated_ac.get("/api/v1/bookings")
    assert len(response.json()) == 0


@pytest.mark.parametrize(
    "user_id, room_id",
    [
        (2, 2),
        (2, 3),
        (1, 4),
        (1, 4),
    ],
)
async def test_booking_crud(user_id, room_id):
    # Добавление брони
    new_booking = await BookingDAO.add_row(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )

    assert new_booking["user_id"] == user_id
    assert new_booking["room_id"] == room_id

    # Проверка добавления брони
    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id)

    assert new_booking is not None

    # Удаление брони
    await BookingDAO.delete(
        id=new_booking["id"],
        user_id=user_id,
    )

    # Проверка удаления брони
    deleted_booking = await BookingDAO.find_one_or_none(id=new_booking["id"])
    assert deleted_booking is None
