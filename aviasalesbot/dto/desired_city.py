import string
from dataclasses import dataclass

from dto.destinations import Destination


@dataclass
class DesiredCity:
    origin: Destination
    destination: Destination
    departure_at: list[string]
