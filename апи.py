import os
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='your_bot_token')
dp = Dispatcher(bot)

@dp.message.handler(commands=["start"])
async def start_command(message: types.Message):
	await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")

if __name__ == "__main__":
	# С помощью метода executor.start_polling опрашиваем
    # Dispatcher: ожидаем команду /start
	executor.start_polling(dp)

@dp.message_handler()
async def get_weather(message: types.Message):
	pass

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather? q=москва&lang=ru&units=metric&appid=your_token")
        data = response.json()
    except:
        await message.reply("Проверьте название города!")