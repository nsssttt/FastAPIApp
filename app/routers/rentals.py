from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.hotel_service import HotelService
from app.models.schemas import RentalCreate, RentalResponse

router = APIRouter(prefix="/rentals", tags=["Rentals"])


@router.post("/", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
def create_rental(
    rental_data: RentalCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new rental (rent out a room to a guest).
    - **room_number**: Room number to rent
    - **guest_name**: Guest name
    - **start_date**: Check-in date (cannot be in the past)
    - **end_date**: Check-out date (must be after start_date)
    """
    service = HotelService(db)
    return service.create_rental(rental_data)


@router.get("/", response_model=List[RentalResponse])
def get_all_rentals(db: Session = Depends(get_db)):
    """Get all active rentals."""
    service = HotelService(db)
    return service.get_all_rentals()


@router.put("/{rental_id}/complete", status_code=status.HTTP_200_OK)
def complete_rental(
    rental_id: int,
    db: Session = Depends(get_db)
):
    """
    Complete a rental by ID.
    - **rental_id**: ID of the rental to complete
    """
    service = HotelService(db)
    return service.complete_rental(rental_id)
