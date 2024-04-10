import datetime

import pyowm
import telebot  
import os  
import time


owmToken = os.getenv('a7cdf5a1d7d50b47ae1783c147695e8b')  
owm = pyowm.OWM(owmToken, language='ru')
botToken = os.getenv('6743215652:AAGp0dV3PuLvVUyl8rmpBt_FQADx5tQQF_0')  
bot = telebot.TeleBot(botToken)


# Когда боту пишут текстовое сообщение вызывается эта функция
@bot.message_handler(content_types=['text'])
def send_message(message):
    """Send the message to user with the weather"""
    # Отдельно реагируем на сообщения /start и /help

    if message.text.lower() == "/start":
        bot.send_message(message.from_user.id, "Здравствуйте. Чтобы узнать список команд введите /help. "
                                               "Введите название города, а затем нужную команду для получения "
                                               "информации о погоде")
    elif message.text.lower() == '/help':
        bot.send.message(message.from_user.id, 'Вот список команд: /all - вся информация о погоде, /temp - температура,'
                                               '/hum - влажность, /press - давление, /wind - скорость ветра, '
                                               '/rise - время восхода солнца, /set - время заката солнца')
    else:
        # С помощью try заставляю пройти код, если функция observation не находит город
        # и выводит ошибку, то происходит переход к except
        try:
            city, command = message.text.split()
            # Имя города пользователь вводит в чат, после этого мы его передаем в функцию
            observation = owm.weather_at_place(city)
            weather = observation.get_weather()
            temp = weather.get_temperature("celsius")["temp"]  # Присваиваем переменной значение температуры из таблицы
            temp = round(temp)
            hum = weather.get_humidity['humidity']
            press = weather.get_pressure['pressure']
            wind = weather.get_wind['speed']
            rise_time = datetime.datetime.fromtimestamp(weather.get_sunrise['sunrise'])
            set_time = datetime.datetime.fromtimestamp(weather.get_sunset['sunset'])
            print(time.ctime(), "User id:", message.from_user.id)
            print(time.ctime(), "Message:", message.text.title(), temp, "C", weather.get_detailed_status())
            if command == '/all':
                print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                      f'Погода в городе {city}:\nТемпература:{temp}C°\n'
                      f'Влажность: {hum}%\n'
                      f'Давление: {press} мм рт.ст\n'
                      f'Ветер: {wind} м/c\n'
                      f'Восход солнца: {rise_time}\n'
                      f'Закат солнца: {set_time}\n'
                      f'Удачного вам дня!')
            elif command == '/temp':
                print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                      f'Температура в городе {city}: {temp} C°')
            elif command == '/hum':
                print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                      f'Влажность в городе {city}: {hum}%')
            elif command == '/press':
                print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                      f'Давление в городе {city}: {press}мм рт.ст.')
            elif command == '/wind':
                print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                      f'Ветер в городе {city}: {wind}м/c')
            elif command == '/rise':
                print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                      f'Восход солнца в городе {city} в {rise_time}')
            elif command == '/set':
                print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                      f'Закат солнца в городе {city} в {set_time}')
        except Exception:
            answer = "Не найден город, попробуйте ввести название снова.\n"
            print(time.ctime(), "User id:", message.from_user.id)
            print(time.ctime(), "Message:", message.text.title(), 'Error')

        bot.send_message(message.chat.id, answer)  # Ответить сообщением


# Запускаем бота
bot.polling(none_stop=True)