import os
import time

import telebot
import schedule
import asyncio
from dto.desired_city import DesiredCity
from dto.destinations import Destination
from service.tg_bot_service import TgBotService

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_TO_FETCH = os.getenv("USER_ID")
bot = telebot.TeleBot(BOT_TOKEN)

service = TgBotService(desired_cities=[
    DesiredCity(
        origin=Destination.MOSCOW,
        destination=Destination.KAZAN,
        departure_at=["2024-08-10", "2024-08-11", "2024-08-12", "2024-08-13"]
    ),
    DesiredCity(
        origin=Destination.KAZAN,
        destination=Destination.KALININGRAD,
        departure_at=["2024-08-15", "2024-08-16", "2024-08-17", "2024-08-18"]
    ),
    DesiredCity(
        origin=Destination.KALININGRAD,
        destination=Destination.MOSCOW,
        departure_at=["2024-08-22", "2024-08-23", "2024-08-24", "2024-08-25"]
    )
])


def send_info():
    response = asyncio.run(service.fetch_desired_cities())
    bot.send_message(chat_id=USER_TO_FETCH, text=response)


@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.reply_to(message, "Henlo")


schedule.every(2).hours.do(send_info)

while True:
    schedule.run_pending()
    time.sleep(1)
