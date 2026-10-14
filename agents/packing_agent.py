from tools.packing_tool import PackingTool


class PackingAgent:

    def __init__(self):
        self.packing_tool = PackingTool()

    def generate_packing(
        self,
        destination,
        days,
        weather_condition
    ):

        return self.packing_tool.generate_packing_list(
            destination,
            days,
            weather_condition
        )