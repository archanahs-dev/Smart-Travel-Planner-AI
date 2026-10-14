from tools.budget_tool import BudgetTool
from services.hotel_service import HotelService


class BudgetAgent:

    def __init__(self):

        self.budget_tool = BudgetTool()
        self.hotel_service = HotelService()

    def generate_budget(
        self,
        destination,
        budget_type,
        days,
        people
    ):

        hotel = self.hotel_service.get_hotel_by_category(
            destination,
            budget_type
        )

        if hotel is None:

            return {
                "Status": False,
                "Message": "No hotel available."
            }

        hotel_price = hotel["price_per_night"]

        budget = self.budget_tool.calculate_budget(
            hotel_price,
            days,
            people,
            budget_type
        )

        total = budget["Total"]

        return {

            "Status": True,

            "Hotel Cost": f"₹ {budget['Hotel']}",

            "Food Cost": f"₹ {budget['Food']}",

            "Transport Cost": f"₹ {budget['Transport']}",

            "Activities Cost": f"₹ {budget['Activities']}",

            "Total Budget": f"₹ {total}",

            "Trip Type": self.budget_tool.get_budget_status(total),

            "Suggestions": [
                "Book hotels early for better prices.",
                "Keep emergency cash while travelling."
            ]
        }