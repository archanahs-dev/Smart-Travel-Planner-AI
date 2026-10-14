from services.hotel_service import HotelService


class HotelTool:

    def __init__(self):
        self.hotel_service = HotelService()

    def recommend_hotel(self, destination, budget_type):

        hotel = self.hotel_service.get_hotel_by_category(
            destination,
            budget_type
        )

        if hotel is None:

            return {
                "status": False,
                "message": "No hotel found."
            }

        result = {
            "status": True,
            "Hotel Name": hotel["name"],
            "Category": hotel["category"],
            "Price": f"₹{hotel['price_per_night']} / Night",
            "Rating": f"{hotel['rating']} ⭐",
            "Location": hotel["location"]
        }

        if "amenities" in hotel:
            result["Amenities"] = ", ".join(hotel["amenities"])

        if budget_type == "Budget":
            result["Reason"] = "Affordable stay with good facilities."

        elif budget_type == "Standard":
            result["Reason"] = "Best balance between comfort and price."

        else:
            result["Reason"] = "Premium stay with luxury facilities."

        return result

    def show_all_hotels(self, destination):
        return self.hotel_service.get_hotels(destination)