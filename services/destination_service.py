import json
import os


class DestinationService:

    def __init__(self):
        self.file_path = os.path.join("data", "destinations.json")
        self.destinations = self.load_destinations()

    def load_destinations(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print("Error:", e)
            return {}

    def get_all_destinations(self):
        return list(self.destinations.keys())

    def get_destination(self, destination):
        return self.destinations.get(destination, {})

    def get_places(self, destination):
        return self.get_destination(destination).get("places", [])

    def get_foods(self, destination):
        return self.get_destination(destination).get("foods", [])

    def get_activities(self, destination):
        return self.get_destination(destination).get("activities", [])

    def get_packing(self, destination):
        return self.get_destination(destination).get("packing", [])

    def get_budget(self, destination):
        return self.get_destination(destination).get("budget", {})

    def get_best_time(self, destination):
        return self.get_destination(destination).get("best_time", "")

    def get_transport(self, destination):
        return self.get_destination(destination).get("transport", [])

    def get_local_tips(self, destination):
        return self.get_destination(destination).get("local_tips", [])