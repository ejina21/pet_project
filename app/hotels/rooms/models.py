from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(ForeignKey("hotels.id"))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    services = Column(JSON)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="room")
    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")

    def __str__(self):
        return f"{self.name}"
