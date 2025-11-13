from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date

from app.models.room import Room
from app.models.booking import Booking
from app.models.rental import Rental
from app.models.enums import RoomStatus, RoomCategory
from app.models.schemas import (
    RoomCreate, RoomResponse, BookingCreate, BookingResponse,
    RentalCreate, RentalResponse, StatisticsResponse
)


class HotelService:
    def __init__(self, db: Session):
        self.db = db

    def create_room(self, room_data: RoomCreate) -> RoomResponse:
        existing_room = self.db.query(Room).filter(Room.number == room_data.number).first()
        if existing_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Room number {room_data.number} already exists"
            )

        room = Room(
            number=room_data.number,
            category=room_data.category,
            status=RoomStatus.FREE
        )
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)

        return self._room_to_response(room)

    def get_room_by_number(self, room_number: int) -> Optional[Room]:
        return self.db.query(Room).filter(Room.number == room_number).first()

    def get_all_rooms(
        self,
        category: Optional[RoomCategory] = None,
        status_filter: Optional[RoomStatus] = None
    ) -> List[RoomResponse]:
        query = self.db.query(Room)

        if category:
            query = query.filter(Room.category == category)
        if status_filter:
            query = query.filter(Room.status == status_filter)

        rooms = query.all()
        return [self._room_to_response(room) for room in rooms]

    def get_free_rooms(self, category: Optional[RoomCategory] = None) -> List[RoomResponse]:
        query = self.db.query(Room).filter(Room.status == RoomStatus.FREE)

        if category:
            query = query.filter(Room.category == category)

        rooms = query.all()
        return [self._room_to_response(room) for room in rooms]

    def create_booking(self, booking_data: BookingCreate) -> BookingResponse:
        room = self.get_room_by_number(booking_data.room_number)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room number {booking_data.room_number} not found"
            )

        if room.status != RoomStatus.FREE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Room {booking_data.room_number} is not available (status: {room.status.value})"
            )

        booking = Booking(
            room_id=room.id,
            guest_name=booking_data.guest_name,
            start_date=booking_data.start_date,
            end_date=booking_data.end_date
        )

        room.status = RoomStatus.BOOKED

        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)

        return self._booking_to_response(booking, room)

    def delete_booking(self, booking_id: int) -> dict:
        booking = self.db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Booking {booking_id} not found"
            )

        room = self.db.query(Room).filter(Room.id == booking.room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room not found"
            )

        room.status = RoomStatus.FREE

        self.db.delete(booking)
        self.db.commit()

        return {"message": f"Booking {booking_id} deleted successfully", "room_number": room.number}

    def get_all_bookings(self) -> List[BookingResponse]:
        bookings = self.db.query(Booking).all()
        result = []
        for booking in bookings:
            room = self.db.query(Room).filter(Room.id == booking.room_id).first()
            if room:
                result.append(self._booking_to_response(booking, room))
        return result

    def create_rental(self, rental_data: RentalCreate) -> RentalResponse:
        room = self.get_room_by_number(rental_data.room_number)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room number {rental_data.room_number} not found"
            )

        if room.status != RoomStatus.FREE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Room {rental_data.room_number} is not available (status: {room.status.value})"
            )

        rental = Rental(
            room_id=room.id,
            guest_name=rental_data.guest_name,
            start_date=rental_data.start_date,
            end_date=rental_data.end_date
        )

        room.status = RoomStatus.RENTED

        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)

        return self._rental_to_response(rental, room)

    def complete_rental(self, rental_id: int) -> dict:
        rental = self.db.query(Rental).filter(Rental.id == rental_id).first()
        if not rental:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rental {rental_id} not found"
            )

        room = self.db.query(Room).filter(Room.id == rental.room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room not found"
            )

        days = rental.duration_days
        total_cost = days * room.price

        room.status = RoomStatus.FREE

        self.db.delete(rental)
        self.db.commit()

        return {
            "message": f"Rental {rental_id} completed successfully",
            "rental_id": rental_id,
            "room_number": room.number,
            "total_cost": total_cost
        }

    def get_all_rentals(self) -> List[RentalResponse]:
        rentals = self.db.query(Rental).all()
        result = []
        for rental in rentals:
            room = self.db.query(Room).filter(Room.id == rental.room_id).first()
            if room:
                result.append(self._rental_to_response(rental, room))
        return result

    def get_statistics(self) -> StatisticsResponse:
        total = self.db.query(Room).count()
        free = self.db.query(Room).filter(Room.status == RoomStatus.FREE).count()
        booked = self.db.query(Room).filter(Room.status == RoomStatus.BOOKED).count()
        rented = self.db.query(Room).filter(Room.status == RoomStatus.RENTED).count()

        occupancy_rate = 0.0
        if total > 0:
            occupancy_rate = ((booked + rented) / total) * 100

        return StatisticsResponse(
            total_rooms=total,
            free_rooms=free,
            booked_rooms=booked,
            rented_rooms=rented,
            occupancy_rate=round(occupancy_rate, 2)
        )

    def _room_to_response(self, room: Room) -> RoomResponse:
        return RoomResponse(
            id=room.id,
            number=room.number,
            category=room.category,
            status=room.status,
            price=room.price
        )

    def _booking_to_response(self, booking: Booking, room: Room) -> BookingResponse:
        estimated_cost = booking.duration_days * room.price
        return BookingResponse(
            id=booking.id,
            room_id=room.id,
            room_number=room.number,
            guest_name=booking.guest_name,
            start_date=booking.start_date,
            end_date=booking.end_date,
            duration_days=booking.duration_days,
            estimated_cost=estimated_cost
        )

    def _rental_to_response(self, rental: Rental, room: Room) -> RentalResponse:
        total_cost = rental.duration_days * room.price
        return RentalResponse(
            id=rental.id,
            room_id=room.id,
            room_number=room.number,
            guest_name=rental.guest_name,
            start_date=rental.start_date,
            end_date=rental.end_date,
            duration_days=rental.duration_days,
            total_cost=total_cost
        )
