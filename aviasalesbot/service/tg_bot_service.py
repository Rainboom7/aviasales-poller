import string

from db.pg_service import PgService
from dto.LowestDto import LowestDto
from dto.avia_response_item import AviaResponseItem
from dto.desired_city import DesiredCity
from dto.period_type import PeriodType
from service.aviasales_api_service import AviasalesApiService

MAX_VALUE = 922337203


class TgBotService:
    def __init__(self, desired_cities: list[DesiredCity]):
        self.aviasales_service = AviasalesApiService(period_type=PeriodType.DAY)
        self.pg_service = PgService()
        self.desired_cities = desired_cities

    async def fetch_desired_cities(self) -> string:
        response = ""
        lowest_total = [LowestDto(MAX_VALUE, "") for i in range(len(self.desired_cities))]
        for i in range(len(self.desired_cities)):
            city = self.desired_cities[i]
            response += f"✈️{city.origin.convert_to_russian()} -> {city.destination.convert_to_russian()}\n"
            for date in city.departure_at:
                api_response = await self.aviasales_service.fetch_latest_prices(
                    destination_from=city.origin,
                    destination_to=city.destination,
                    departure_at=date
                )
                if api_response is None:
                    continue
                converted = self.__convertResponse(api_response)
                response += converted[0]
                if lowest_total[i].price > converted[1]:
                    lowest_total[i] = LowestDto(converted[1], converted[2])

            response += f" 💸 Лучшая цена:{lowest_total[i].price}₽ на дату 📅{lowest_total[i].date}\n"
            db_lowest = self.pg_service.calculate_min_by_key(self._map_to_key(city))
            if lowest_total[i].price < db_lowest:
                response += f" ❗ Эта цена меньше всех прошлых!!\n"
            response += "\n"
        total_price = sum(l.price for l in lowest_total)
        city_keys = [self._map_to_key(c) for c in self.desired_cities]
        total_min = self.pg_service.calculate_total_min(city_keys)
        response += f"\n💸Лучшая общая цена:{total_price}₽ \n"
        response += f"\n💸PG:Лучшая общая цена:{total_min}₽ \n"
        return response

    def __convertResponse(self, response: list[AviaResponseItem]):
        res = ""
        lowest = MAX_VALUE
        lowest_date = ""
        print(response)
        for item in response:
            res += f"   💸 Цена:{item.price}₽\n" \
                   f"   💸 На двоих:{2 * item.price}₽\n" \
                   f"   ✈️Вылет:{item.departure_at}\n" \
                   f"   ✈В полете:{item.duration_to_min} минут\n" \
                   f"   👩‍✈️Авиакомпания:{item.airline}\n" \
                   f"   ______________________\n"

            if item.price * 2 < lowest:
                lowest = item.price * 2
                lowest_date = item.departure_at
            self.pg_service.insert_price(item)

        return [res, lowest, lowest_date]

    def _map_to_key(self, city: DesiredCity):
        return city.origin.value + "->" + city.destination.value
