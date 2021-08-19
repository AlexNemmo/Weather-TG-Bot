from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import datetime
from config import tg_api, weather_token
import requests

bot = Bot(token=tg_api)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("Привет! \U0001F600 Напиши мне название города, чтобы узнать погоду.")


@dp.message_handler()
async def weather_cmd(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Mist": "Туман \U0001F32B",
        "Fog": "Туман \U0001F32B",
        "Clouds": "Облачно \U00002601",
        "Snow": "Снег \U0001F328",
        "Rain": "Дождь \U0001F327",
        "Drizzle": "Мелкий дождь \U0001F327",
        "Thunderstorm": "Гроза \U000026C8"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric&lang=ru")
        data = r.json()
        city_name = data['name']
        main_weather = data['weather'][0]['main']
        if main_weather in code_to_smile:
            wd = code_to_smile[main_weather]
        else:
            wd = "Посмотри в окно, я не понимаю, что происходит"
        temp = data["main"]['temp']
        feels_temp = data['main']['feels_like']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        humidity = data['main']['humidity']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        await message.reply(
            f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***" + "\n" +
            f"Погода: {wd} \n" +
            f"Температура: {temp} C° \n" +
            f"Ощущаемая температура: {feels_temp} C° \n" +
            f"Ветер: {wind} м/с \n" +
            f"Давление: {pressure} мм.рт.ст \n" +
            f"Влажность: {humidity}% \n" +
            f"Восход: {sunrise} \n" +
            f"Закат: {sunset} \n" +
            "Хорошего вам дня! \U0001F600")
    except:
        await message.reply("Проверьте название города! \U0001F928")


if __name__ == "__main__":
    executor.start_polling(dp)
