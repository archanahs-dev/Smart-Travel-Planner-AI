from tools.weather_tool import WeatherTool


class WeatherAgent:

    def __init__(self):
        self.weather_tool = WeatherTool()

    def analyze_weather(self, destination):

        weather = self.weather_tool.get_weather(destination)

        condition = weather["Condition"]

        if condition == "Sunny":
            advice = "Carry sunscreen and stay hydrated."

        elif condition == "Rainy":
            advice = "Carry an umbrella or raincoat."

        else:
            advice = "Pleasant weather for sightseeing."

        weather["Advice"] = advice

        return weather