class BudgetTool:

    def __init__(self):

        self.food_cost = {
            "Budget": 500,
            "Standard": 1000,
            "Luxury": 2000
        }

        self.transport_cost = {
            "Budget": 300,
            "Standard": 700,
            "Luxury": 1500
        }

        self.activity_cost = {
            "Budget": 500,
            "Standard": 1200,
            "Luxury": 2500
        }

    def calculate_budget(self, hotel_price, days, people, budget_type):

        hotel_total = hotel_price * days

        food_total = self.food_cost[budget_type] * people * days

        transport_total = self.transport_cost[budget_type] * people * days

        activity_total = self.activity_cost[budget_type] * people

        total = hotel_total + food_total + transport_total + activity_total

        return {
            "Hotel": hotel_total,
            "Food": food_total,
            "Transport": transport_total,
            "Activities": activity_total,
            "Total": total
        }

    def get_budget_status(self, total):

        if total <= 20000:
            return "💚 Budget Friendly"

        elif total <= 50000:
            return "🟡 Standard Trip"

        return "💎 Luxury Trip"