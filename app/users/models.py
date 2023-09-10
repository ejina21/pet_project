from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.email}"
