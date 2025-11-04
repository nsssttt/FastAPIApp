from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    guest_name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    room = relationship("Room", back_populates="bookings")

    @property
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days

    def __repr__(self):
        return f"<Booking(id={self.id}, room_id={self.room_id}, guest={self.guest_name})>"
