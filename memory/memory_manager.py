import json
import os


class MemoryManager:

    def __init__(self):

        self.file_path = os.path.join(
            "memory",
            "user_memory.json"
        )

        # Create file if it doesn't exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

    # ---------------------------
    # Save Trip
    # ---------------------------

    def save_trip(
        self,
        destination,
        days,
        people,
        budget_type,
        total_budget
    ):

        trip = {
            "Destination": destination,
            "Days": days,
            "People": people,
            "Budget Type": budget_type,
            "Total Budget": total_budget
        }

        # Read existing trips
        with open(self.file_path, "r", encoding="utf-8") as file:
            trips = json.load(file)

        # Add new trip
        trips.append(trip)

        # Keep only the latest 4 trips
        if len(trips) > 4:
            trips = trips[-4:]

        # Save back to file
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(trips, file, indent=4)

    # ---------------------------
    # Get Previous Trips
    # ---------------------------

    def get_previous_trips(self):

        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    # ---------------------------
    # Compatibility Function
    # ---------------------------

    def get_history(self):
        return self.get_previous_trips()

    # ---------------------------
    # Clear History (Optional)
    # ---------------------------

    def clear_history(self):

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)