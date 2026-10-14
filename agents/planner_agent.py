from agents.weather_agent import WeatherAgent
from agents.hotel_agent import HotelAgent
from agents.budget_agent import BudgetAgent
from agents.itinerary_agent import ItineraryAgent
from agents.packing_agent import PackingAgent


class PlannerAgent:

    def __init__(self):

        self.weather_agent = WeatherAgent()

        self.hotel_agent = HotelAgent()

        self.budget_agent = BudgetAgent()

        self.itinerary_agent = ItineraryAgent()

        self.packing_agent = PackingAgent()

    def create_plan(
        self,
        destination,
        days,
        people,
        budget_type
    ):

        weather = self.weather_agent.analyze_weather(destination)

        hotel = self.hotel_agent.recommend_hotel(
            destination,
            budget_type
        )

        budget = self.budget_agent.generate_budget(
            destination,
            budget_type,
            days,
            people
        )

        packing = self.packing_agent.generate_packing(
            destination,
            days,
            weather["Condition"]
        )

        itinerary = self.itinerary_agent.generate_itinerary(
            destination,
            days
        )

        return {
            "Weather": weather,
            "Hotel": hotel,
            "Budget": budget,
            "Packing": packing,
            "Itinerary": itinerary
        }