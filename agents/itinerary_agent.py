from services.destination_service import DestinationService


class ItineraryAgent:

    def __init__(self):
        self.destination_service = DestinationService()

    def generate_itinerary(self, destination, days):

        places = self.destination_service.get_places(destination)
        foods = self.destination_service.get_foods(destination)
        activities = self.destination_service.get_activities(destination)
        tips = self.destination_service.get_local_tips(destination)

        itinerary = []

        for i in range(days):

            morning = places[i % len(places)]

            afternoon = activities[i % len(activities)]

            evening = places[(i + 1) % len(places)]

            food = foods[i % len(foods)]

            tip = tips[0] if tips else "Enjoy your trip."

            itinerary.append({
                "Day": i + 1,
                "Morning": morning,
                "Afternoon": afternoon,
                "Evening": evening,
                "Food": food,
                "Tip": tip
            })

        return itinerary