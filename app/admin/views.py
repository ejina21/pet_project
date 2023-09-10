from sqladmin import ModelView

from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import User
from app.bookings.models import Bookings


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingAdmin(ModelView, model=Bookings):
    column_list = '__all__'
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = '__all__'
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = '__all__'
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"
