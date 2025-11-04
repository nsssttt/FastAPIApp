from pydantic import BaseModel, field_validator, Field
from datetime import date
from typing import Optional
from app.models.enums import RoomStatus, RoomCategory


class RoomBase(BaseModel):
    number: int = Field(..., gt=0, description="Room number")
    category: RoomCategory


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    category: Optional[RoomCategory] = None
    status: Optional[RoomStatus] = None


class RoomResponse(RoomBase):
    id: int
    status: RoomStatus
    price: float

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    room_number: int = Field(..., gt=0, description="Room number to book")
    guest_name: str = Field(..., min_length=1, max_length=255, description="Guest name")
    start_date: date
    end_date: date

    @field_validator('guest_name')
    @classmethod
    def validate_guest_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Guest name cannot be empty")
        return v.strip()

    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v: date, info) -> date:
        if 'start_date' in info.data and v <= info.data['start_date']:
            raise ValueError("End date must be after start date")
        return v

    @field_validator('start_date')
    @classmethod
    def validate_start_date_not_past(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Start date cannot be in the past")
        return v


class BookingCreate(BookingBase):
    pass


class BookingResponse(BaseModel):
    id: int
    room_id: int
    room_number: int
    guest_name: str
    start_date: date
    end_date: date
    duration_days: int
    estimated_cost: float

    class Config:
        from_attributes = True


class RentalBase(BaseModel):
    room_number: int = Field(..., gt=0, description="Room number to rent")
    guest_name: str = Field(..., min_length=1, max_length=255, description="Guest name")
    start_date: date
    end_date: date

    @field_validator('guest_name')
    @classmethod
    def validate_guest_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Guest name cannot be empty")
        return v.strip()

    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v: date, info) -> date:
        if 'start_date' in info.data and v <= info.data['start_date']:
            raise ValueError("End date must be after start date")
        return v

    @field_validator('start_date')
    @classmethod
    def validate_start_date_not_past(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Start date cannot be in the past")
        return v


class RentalCreate(RentalBase):
    pass


class RentalResponse(BaseModel):
    id: int
    room_id: int
    room_number: int
    guest_name: str
    start_date: date
    end_date: date
    duration_days: int
    total_cost: float

    class Config:
        from_attributes = True


class RentalCompleteResponse(BaseModel):
    message: str
    rental_id: int
    room_number: int
    total_cost: float


class StatisticsResponse(BaseModel):
    total_rooms: int
    free_rooms: int
    booked_rooms: int
    rented_rooms: int
    occupancy_rate: float


class ErrorResponse(BaseModel):
    detail: str
