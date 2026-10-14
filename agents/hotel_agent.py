from tools.hotel_tool import HotelTool


class HotelAgent:

    def __init__(self):
        self.hotel_tool = HotelTool()

    def recommend_hotel(self, destination, budget_type):

        hotel = self.hotel_tool.recommend_hotel(
            destination,
            budget_type
        )

        if hotel["status"] is False:

            return {
                "Status": False,
                "Message": hotel["message"]
            }

        return {
            "Status": True,
            "Hotel Name": hotel["Hotel Name"],
            "Category": hotel["Category"],
            "Price": hotel["Price"],
            "Rating": hotel["Rating"],
            "Location": hotel["Location"],
            "Amenities": hotel.get("Amenities", "Not Available"),
            "Reason": hotel["Reason"]
        }