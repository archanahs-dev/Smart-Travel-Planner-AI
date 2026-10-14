"""Approximate coordinates of popular spots, for the trip map (verify before real travel)."""
import pandas as pd

SPOTS = {
    "Goa": {"Baga Beach": (15.5553, 73.7517), "Basilica of Bom Jesus": (15.5009, 73.9116), "Fort Aguada": (15.4925, 73.7737)},
    "Manali": {"Hadimba Temple": (32.2482, 77.1773), "Solang Valley": (32.3160, 77.1580), "Mall Road": (32.2432, 77.1892)},
    "Mysore": {"Mysore Palace": (12.3052, 76.6552), "Chamundi Hill": (12.2724, 76.6700), "Brindavan Gardens": (12.4244, 76.5726)},
    "Ooty": {"Botanical Garden": (11.4181, 76.7114), "Ooty Lake": (11.4036, 76.6893), "Doddabetta Peak": (11.4024, 76.7359)},
    "Coorg": {"Abbey Falls": (12.4543, 75.7165), "Raja's Seat": (12.4208, 75.7389), "Dubare Elephant Camp": (12.3885, 75.9139)},
    "Bengaluru": {"Lalbagh": (12.9507, 77.5848), "Cubbon Park": (12.9763, 77.5929), "Bangalore Palace": (12.9988, 77.5921)},
    "Varanasi": {"Dashashwamedh Ghat": (25.3109, 83.0107), "Assi Ghat": (25.2886, 83.0060), "Sarnath": (25.3811, 83.0227)},
    "Vijayawada": {"Prakasam Barrage": (16.5063, 80.6086), "Kanaka Durga Temple": (16.5134, 80.6049), "Bhavani Island": (16.5225, 80.5936)},
    "Hyderabad": {"Charminar": (17.3616, 78.4747), "Golconda Fort": (17.3833, 78.4011), "Hussain Sagar": (17.4239, 78.4738)},
    "Jaipur": {"Hawa Mahal": (26.9239, 75.8267), "Amber Fort": (26.9855, 75.8513), "City Palace": (26.9258, 75.8237)},
}


def get_map_df(destination):
    spots = SPOTS.get(destination, {})
    return pd.DataFrame([{"name": n, "lat": lat, "lon": lon} for n, (lat, lon) in spots.items()])
