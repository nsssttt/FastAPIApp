from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.hotel_service import HotelService
from app.models.schemas import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new booking.
    - **room_number**: Room number to book
    - **guest_name**: Guest name
    - **start_date**: Check-in date (cannot be in the past)
    - **end_date**: Check-out date (must be after start_date)
    """
    service = HotelService(db)
    return service.create_booking(booking_data)


@router.get("/", response_model=List[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    """Get all active bookings."""
    service = HotelService(db)
    return service.get_all_bookings()


@router.delete("/{booking_id}", status_code=status.HTTP_200_OK)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a booking by ID.
    - **booking_id**: ID of the booking to cancel
    """
    service = HotelService(db)
    return service.delete_booking(booking_id)
