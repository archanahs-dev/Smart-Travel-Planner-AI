import json
import os


class HotelService:

    def __init__(self):
        file_path = os.path.join("data", "hotels.json")

        with open(file_path, "r", encoding="utf-8") as file:
            self.hotels = json.load(file)

    def get_hotels(self, destination):
        return self.hotels.get(destination, [])

    def get_hotel_by_category(self, destination, category):

        hotels = self.get_hotels(destination)

        for hotel in hotels:

            if hotel["category"].lower() == category.lower():
                return hotel

        return None

    def get_best_hotel(self, destination):

        hotels = self.get_hotels(destination)

        if len(hotels) == 0:
            return None

        return max(hotels, key=lambda x: x["rating"])