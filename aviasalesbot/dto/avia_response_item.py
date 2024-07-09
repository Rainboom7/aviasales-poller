import string
from dataclasses import dataclass


@dataclass
class AviaResponseItem:
    price: int
    departure_at: string
    return_at: string
    transfers: int
    destination: string
    origin: string
    origin_airport: string
    destination_airport: string
    airline: string
    flight_number: string
    duration_to_min: int
    duration_back_min: int
    link: string
