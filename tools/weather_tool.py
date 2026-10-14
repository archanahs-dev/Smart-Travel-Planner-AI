import random


class WeatherTool:

    def get_weather(self, destination):

        weather = random.choice(
            [
                "Sunny",
                "Cloudy",
                "Rainy"
            ]
        )

        temperature = random.randint(18, 35)

        return {
            "Condition": weather,
            "Temperature": f"{temperature}°C"
        }