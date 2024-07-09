from dataclasses import dataclass


@dataclass
class LowestDto:
    price: int
    date: str
