class ReflectionAgent:

    def review_plan(self, weather, budget, days):

        review = []

        if weather["Condition"] == "Rainy":
            review.append("🌧 Carry an umbrella.")

        elif weather["Condition"] == "Sunny":
            review.append("☀ Carry sunscreen.")

        if budget["Status"]:

            review.append(
                f"💰 Estimated Budget : {budget['Total Budget']}"
            )

        if days >= 5:
            review.append(
                "📅 Long trip. Carry extra clothes."
            )

        review.append("✅ Have a safe journey!")

        return review