"""Makes the itinerary react to the live forecast (rain -> indoor plan)."""

INDOOR = {
    "Goa": ["Basilica of Bom Jesus and Se Cathedral in Old Goa", "Museum of Goa and cafes in Panjim"],
    "Manali": ["Tibetan monastery visit and Tibetan food on Mall Road", "Shopping for woollens and cafe hopping on Mall Road"],
    "Mysore": ["Mysore Palace interior tour", "Jaganmohan Palace art gallery and Devaraja Market"],
    "Ooty": ["Tea factory and tea museum visit", "Homemade chocolate shops and cafe hopping"],
    "Coorg": ["Coffee processing-unit tour and tasting", "Omkareshwara Temple and a Kodava meal"],
    "Bengaluru": ["Visvesvaraya Industrial & Technological Museum", "Bangalore Palace interior and Commercial Street cafes"],
    "Varanasi": ["Kashi Vishwanath darshan and Bharat Kala Bhavan museum", "Banarasi silk weaving workshop visit"],
    "Vijayawada": ["Kanaka Durga Temple darshan", "Victoria Jubilee Museum"],
    "Hyderabad": ["Salar Jung Museum", "Chowmahalla Palace and an Irani cafe stop"],
    "Jaipur": ["City Palace museum", "Block-print shopping at Johari Bazaar"],
}
DEFAULT_INDOOR = ["Local museum visit", "Cafe and local-market hopping"]


def adapt_for_weather(destination, itinerary, forecast):
    """Return (new_itinerary, changes). The input itinerary is not modified."""
    options = INDOOR.get(destination, DEFAULT_INDOOR)
    new_itinerary, changes = [], []
    for i, day in enumerate(itinerary):
        day = dict(day)
        if i < len(forecast) and forecast[i]["rainy"]:
            replacement = options[i % len(options)]
            old = day.get("Afternoon", "")
            day["Afternoon"] = f"{replacement} (indoor plan)"
            day["Tip"] = (f"Rain expected ({forecast[i]['rain_prob']}% chance). "
                          f"Afternoon changed to an indoor plan. {day.get('Tip', '')}").strip()
            changes.append(f"Day {day.get('Day', i + 1)}: '{old}' replaced with '{replacement}'")
        new_itinerary.append(day)
    return new_itinerary, changes


def add_rain_packing(packing, forecast):
    if any(f["rainy"] for f in forecast):
        extras = ["Umbrella / raincoat", "Waterproof cover for bags", "Quick-dry clothes"]
        return list(packing) + [e for e in extras if e not in packing]
    return list(packing)
