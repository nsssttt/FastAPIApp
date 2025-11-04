from typing import Generator
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.hotel_service import HotelService


def get_hotel_service(db: Session = None) -> Generator[HotelService, None, None]:
    if db is None:
        db_gen = get_db()
        db = next(db_gen)
        try:
            yield HotelService(db)
        finally:
            try:
                next(db_gen)
            except StopIteration:
                pass
    else:
        yield HotelService(db)
