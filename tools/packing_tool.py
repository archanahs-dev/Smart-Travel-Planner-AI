from services.destination_service import DestinationService


class PackingTool:

    def __init__(self):
        self.destination_service = DestinationService()

    def generate_packing_list(
        self,
        destination,
        days,
        weather_condition
    ):

        packing = self.destination_service.get_packing(destination)

        packing = packing.copy()

        if weather_condition == "Rainy":
            packing.append("Umbrella")

        if days >= 5:
            packing.append("Extra Clothes")

        return packing