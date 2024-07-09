import string
from enum import Enum


class Destination(Enum):
    MOSCOW = "MOW"
    KALININGRAD = "KGD"
    KAZAN = "KZN"

    def convert_to_russian(self) -> string:
        if self == Destination.KALININGRAD:
            return "Калининград"
        if self == Destination.KAZAN:
            return "Казань"
        if self == Destination.MOSCOW:
            return "Москва"
