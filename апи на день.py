import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENWEATHERMAP_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather in {city} today: {weather_description}. Temperature: {temperature}°C"
    else:
        return "Sorry, could not fetch weather data at the moment."

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
            weather_data = get_weather(city)
            send_message(chat_id, weather_data)
    return {'ok': True}

if __name__ == "__main__":
    app.run(debug=True)