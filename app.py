from flask import Flask, jsonify, request, render_template
from weather_service import get_weather
from database import save_search, get_history
import requests
from config import API_KEY

app = Flask(__name__)


# Home page (UI)
@app.route("/")
def home():
    return render_template("index.html")


# Weather by city
@app.route("/weather", methods=["GET"])
def weather():

    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter required"}), 400

    save_search(city)

    weather_data = get_weather(city)

    return jsonify(weather_data)


# Weather by GPS location
@app.route("/weather-location", methods=["GET"])
def weather_location():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400

    url = f"your_api_url?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    result = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }

    return jsonify(result)


# Search history
@app.route("/history", methods=["GET"])
def history():
    return jsonify(get_history())


if __name__ == "__main__":
    app.run(debug=True)