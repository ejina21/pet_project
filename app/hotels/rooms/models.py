from app.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey


class Rooms(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(ForeignKey("hotels.id"))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    services = Column(JSON)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)