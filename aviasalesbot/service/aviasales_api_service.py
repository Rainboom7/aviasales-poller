import json
import os
import string

import aiohttp

from dto.avia_response_item import AviaResponseItem
from dto.destinations import Destination
from dto.period_type import PeriodType
from dto.sorting import Sorting


class AviasalesApiService:

    def __init__(self, period_type: PeriodType):
        self.air_tickets_url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
        self.currency = "RUB"
        self.token = os.getenv("API_TOKEN")
        self.period_type = period_type
        self.trip_class = 0  # Econom

    async def fetch_latest_prices(self,
                                  destination_from: Destination,
                                  destination_to: Destination,
                                  departure_at: string,
                                  one_way: bool = True,
                                  sorting: Sorting = Sorting.PRICE,
                                  trip_duration: int = 0,
                                  direct: bool = True) -> list[AviaResponseItem]:
        params = {
            'origin': destination_from.value,
            'destination': destination_to.value,
            'departure_at': departure_at,
            'currency': self.currency,
            'token': self.token,
            'period_type': self.period_type.value,
            'one_way': json.dumps(one_way),
            'trip_duration': str(trip_duration),
            "trip_class": self.trip_class,
            "sorting": sorting.value,
            'direct': json.dumps(direct),
            'limit': str(10),
            'page': str(1)
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.air_tickets_url, params=params) as response:
                response_json = await response.json()
                return self._map_response(response_json['data'])

    def _map_response(self, response_json):
        response = []
        for element in response_json:
            response.append(
                AviaResponseItem(
                    price=int(element['price']),
                    departure_at=element['departure_at'],
                    return_at=element.get('return_at'),
                    transfers=int(element['transfers']),
                    destination=element['destination'],
                    origin=element['origin'],
                    origin_airport=element['origin_airport'],
                    destination_airport=element['destination_airport'],
                    airline=element['airline'],
                    flight_number=element['flight_number'],
                    duration_to_min=int(element['duration_to']),
                    duration_back_min=int(element['duration_back']),
                    link=element['link']
                ))
            return response
