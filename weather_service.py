import requests
from config import API_KEY, BASE_URL


def get_weather(city):

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:

        data = response.json()

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }

        return weather_data

    else:
        return {"error": "City not found"}