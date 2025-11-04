from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.hotel_service import HotelService
from app.models.schemas import StatisticsResponse

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/", response_model=StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    """
    Get hotel statistics including:
    - Total number of rooms
    - Number of free rooms
    - Number of booked rooms
    - Number of rented rooms
    - Occupancy rate (percentage)
    """
    service = HotelService(db)
    return service.get_statistics()
