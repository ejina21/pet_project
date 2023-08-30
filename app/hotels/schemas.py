from pydantic import BaseModel


class SHotelAll(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int
    rooms_left: int


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int
