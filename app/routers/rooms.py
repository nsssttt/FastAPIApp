from fastapi import APIRouter, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.hotel_service import HotelService
from app.models.schemas import RoomCreate, RoomResponse
from app.models.enums import RoomCategory, RoomStatus

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    room_data: RoomCreate,
    db: Session = Depends(get_db)
):
    """Create a new room."""
    service = HotelService(db)
    return service.create_room(room_data)


@router.get("/", response_model=List[RoomResponse])
def get_all_rooms(
    category: Optional[RoomCategory] = None,
    status_filter: Optional[RoomStatus] = None,
    db: Session = Depends(get_db)
):
    """
    Get all rooms with optional filters.
    - **category**: Filter by room category (стандарт, комфорт, люкс, президентський)
    - **status_filter**: Filter by room status (вільний, заброньований, зданий)
    """
    service = HotelService(db)
    return service.get_all_rooms(category=category, status_filter=status_filter)


@router.get("/free", response_model=List[RoomResponse])
def get_free_rooms(
    category: Optional[RoomCategory] = None,
    db: Session = Depends(get_db)
):
    """
    Get all free rooms, optionally filtered by category.
    - **category**: Filter by room category (стандарт, комфорт, люкс, президентський)
    """
    service = HotelService(db)
    return service.get_free_rooms(category=category)


@router.get("/{room_number}", response_model=RoomResponse)
def get_room_by_number(
    room_number: int,
    db: Session = Depends(get_db)
):
    """Get a specific room by its number."""
    service = HotelService(db)
    room = service.get_room_by_number(room_number)

    if not room:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room number {room_number} not found"
        )

    return service._room_to_response(room)
