"""Traveller-interest profiles: extra day tips and packing items."""

PROFILES = {
    "Adventure": {
        "tips": ["Book any adventure activity with a licensed operator and check safety gear.",
                 "Start outdoor activities early in the day and keep a buffer for weather changes.",
                 "Carry a basic first-aid kit and a power bank."],
        "packing": ["Sports shoes / trekking shoes", "First-aid kit", "Power bank"],
    },
    "Food": {
        "tips": ["Ask locals for their favourite regional dish and try it at a busy, popular spot.",
                 "Plan one street-food walk, choosing stalls with high turnover.",
                 "Try one traditional thali or breakfast speciality of the region."],
        "packing": ["Reusable water bottle", "Antacids / digestive tablets"],
    },
    "Pilgrimage / Spiritual": {
        "tips": ["Check temple timings and dress code before visiting.",
                 "Go early to avoid long queues and heat.",
                 "Keep a small bag, since some temples do not allow phones or large bags."],
        "packing": ["Modest traditional clothes", "Socks (hot temple floors)", "Small cloth bag"],
    },
    "Family with kids": {
        "tips": ["Keep the schedule light and add a rest break after lunch.",
                 "Carry snacks and water for the children.",
                 "Pick child-friendly places for the afternoon and avoid late nights."],
        "packing": ["Kids' snacks", "Wet wipes", "Basic children's medicines (as advised by your doctor)"],
    },
    "Senior-friendly": {
        "tips": ["Choose places with easy access and limited walking.",
                 "Plan frequent rest stops and carry regular medicines.",
                 "Book transport with comfortable seating and avoid steep climbs."],
        "packing": ["Regular medicines and prescriptions", "Walking stick (if used)", "Comfortable footwear"],
    },
    "Solo traveller safety": {
        "tips": ["Share your live location and itinerary with someone you trust.",
                 "Prefer well-reviewed stays and plan to return before late night.",
                 "Save local emergency numbers and use registered taxis."],
        "packing": ["Portable power bank", "Photocopies of ID", "Emergency contact card"],
    },
}


def apply_profiles(itinerary, packing, interests):
    """Add interest-based tips to each day and extra packing items."""
    if not interests:
        return itinerary, list(packing)
    new_itinerary = []
    for i, day in enumerate(itinerary):
        day = dict(day)
        extra = []
        for interest in interests:
            tips = PROFILES[interest]["tips"]
            extra.append(f"[{interest}] {tips[i % len(tips)]}")
        day["Tip"] = (day.get("Tip", "") + " | " + " | ".join(extra)).strip(" |")
        new_itinerary.append(day)
    new_packing = list(packing)
    for interest in interests:
        for item in PROFILES[interest]["packing"]:
            if item not in new_packing:
                new_packing.append(item)
    return new_itinerary, new_packing
