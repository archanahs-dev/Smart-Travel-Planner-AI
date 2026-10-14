"""Live weather forecast using the free Open-Meteo API (no API key needed)."""
import datetime as dt

import requests

URL = "https://api.open-meteo.com/v1/forecast"

# (latitude, longitude) of each destination in the app
COORDS = {
    "Goa": (15.4989, 73.8278),
    "Manali": (32.2432, 77.1892),
    "Mysore": (12.2958, 76.6394),
    "Ooty": (11.4102, 76.6950),
    "Coorg": (12.4244, 75.7382),
    "Bengaluru": (12.9716, 77.5946),
    "Varanasi": (25.3176, 82.9739),
    "Vijayawada": (16.5062, 80.6480),
    "Hyderabad": (17.3850, 78.4867),
    "Jaipur": (26.9124, 75.7873),
}

RAIN_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99}

CODE_TEXT = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Fog", 51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain", 80: "Rain showers",
    81: "Rain showers", 82: "Violent showers", 95: "Thunderstorm", 96: "Thunderstorm", 99: "Thunderstorm",
}


def get_forecast(destination: str, start_date: dt.date, days: int):
    """Return (forecast_list, error). Each item: date, condition, max, min, rain_prob, rainy."""
    if destination not in COORDS:
        return [], f"No coordinates stored for {destination}."
    lat, lon = COORDS[destination]
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "start_date": start_date.isoformat(),
        "end_date": (start_date + dt.timedelta(days=days - 1)).isoformat(),
    }
    try:
        response = requests.get(URL, params=params, timeout=8)
        response.raise_for_status()
        daily = response.json()["daily"]
        codes = daily.get("weather_code") or daily.get("weathercode")
        forecast = []
        for i, date in enumerate(daily["time"]):
            code = codes[i]
            prob = daily["precipitation_probability_max"][i] or 0
            forecast.append({
                "date": date,
                "condition": CODE_TEXT.get(code, "Mixed weather"),
                "max": daily["temperature_2m_max"][i],
                "min": daily["temperature_2m_min"][i],
                "rain_prob": prob,
                "rainy": code in RAIN_CODES or prob >= 60,
            })
        return forecast, None
    except Exception as exc:  # no internet, API down, unexpected format
        return [], f"Live forecast unavailable ({exc.__class__.__name__}). Showing the standard plan."
