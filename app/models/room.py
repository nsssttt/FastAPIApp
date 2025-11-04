from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.enums import RoomStatus, RoomCategory


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, nullable=False, index=True)
    category = Column(SQLEnum(RoomCategory), nullable=False)
    status = Column(SQLEnum(RoomStatus), default=RoomStatus.FREE, nullable=False)

    bookings = relationship("Booking", back_populates="room", cascade="all, delete-orphan")
    rentals = relationship("Rental", back_populates="room", cascade="all, delete-orphan")

    @property
    def price(self) -> float:
        return self.category.price

    def __repr__(self):
        return f"<Room(number={self.number}, category={self.category.value}, status={self.status.value})>"
