import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENWEATHERMAP_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"


def get_weather_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        forecast = []
        for item in data['list']:
            date = item['dt_txt']
            weather_description = item['weather'][0]['description']
            temperature = item['main']['temp']
            forecast.append(f"{date}: {weather_description}. Температура: {temperature}°C")
        return forecast
    else:
        return "К сожалению, в данный момент не удалось получить прогноз погоды."


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)
    return response.json()


@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        message_text = data['message']['text']
        if message_text.startswith('/weather'):
            city = message_text.split(' ', 1)[1]
            weather_forecast = get_weather_forecast(city)
            for forecast_day in weather_forecast:
                send_message(chat_id, forecast_day)
    return {'ok': True}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)