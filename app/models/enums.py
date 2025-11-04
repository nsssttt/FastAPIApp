from enum import Enum


class RoomStatus(str, Enum):
    FREE = "вільний"
    BOOKED = "заброньований"
    RENTED = "зданий"


class RoomCategory(str, Enum):
    STANDARD = "стандарт"
    COMFORT = "комфорт"
    LUX = "люкс"
    PRESIDENT = "президентський"

    @property
    def price(self) -> float:
        prices = {
            self.STANDARD: 500.0,
            self.COMFORT: 800.0,
            self.LUX: 1200.0,
            self.PRESIDENT: 2000.0
        }
        return prices[self]
