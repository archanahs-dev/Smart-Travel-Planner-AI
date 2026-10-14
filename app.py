import datetime as dt
import json

import streamlit as st

from agents.planner_agent import PlannerAgent
from agents.reflection_agent import ReflectionAgent
from memory.memory_manager import MemoryManager
from utils.pdf_generator import create_pdf

# NEW feature modules
from services.live_forecast import get_forecast
from services.itinerary_adapter import adapt_for_weather, add_rain_packing
from services.profiles import PROFILES, apply_profiles
from services.map_data import get_map_df
from services.trip_chat import ask_trip_assistant

# ---------------------------
# Page Configuration
# ---------------------------

st.set_page_config(page_title="Smart Travel Planner", page_icon="✈️", layout="wide")

planner = PlannerAgent()
reflection = ReflectionAgent()
memory = MemoryManager()

# ---------------------------
# Header
# ---------------------------

st.title("🌍 Smart Travel Planner")
st.markdown("### AI Powered Multi-Agent Travel Planner")
st.markdown("---")

# ---------------------------
# Sidebar
# ---------------------------

st.sidebar.header("Trip Details")

destination = st.sidebar.selectbox(
    "Select Destination",
    ["Goa", "Manali", "Mysore", "Ooty", "Coorg", "Bengaluru",
     "Varanasi", "Vijayawada", "Hyderabad", "Jaipur"]
)

days = st.sidebar.slider("Number of Days", 1, 7, 3)

people = st.sidebar.number_input("Number of People", min_value=1, max_value=10, value=2)

budget_type = st.sidebar.selectbox("Budget Type", ["Budget", "Standard", "Luxury"])

# NEW: start date (live forecast works up to ~2 weeks ahead) and traveller interests
today = dt.date.today()
start_date = st.sidebar.date_input(
    "Trip Start Date", value=today, min_value=today, max_value=today + dt.timedelta(days=9)
)

interests = st.sidebar.multiselect("Traveller Interests", list(PROFILES.keys()))

generate = st.sidebar.button("Generate Travel Plan")

# ---------------------------
# Build the plan ONCE and keep it in session_state.
# (Without this, any click on a checkbox or the chat box re-runs the script
#  and the whole plan disappears.)
# ---------------------------

if generate:

    result = planner.create_plan(destination, days, people, budget_type)

    weather = result["Weather"]
    hotel = result["Hotel"]
    budget = result["Budget"]
    itinerary = result["Itinerary"]
    packing = result["Packing"]

    # NEW: live forecast -> rain-aware itinerary -> interest profiles
    forecast, forecast_error = get_forecast(destination, start_date, days)
    itinerary, rain_changes = adapt_for_weather(destination, itinerary, forecast)
    packing = add_rain_packing(packing, forecast)
    itinerary, packing = apply_profiles(itinerary, packing, interests)

    review = []
    if budget["Status"]:
        review = reflection.review_plan(weather, budget, days)
        memory.save_trip(destination, days, people, budget_type, budget["Total Budget"])

    pdf = None
    if budget["Status"]:
        pdf = create_pdf(destination, weather, hotel, budget, itinerary, packing, review)

    summary = json.dumps({
        "destination": destination, "days": days, "people": people, "budget_type": budget_type,
        "interests": interests, "weather": weather, "hotel": hotel, "budget": budget,
        "itinerary": itinerary, "packing": packing, "live_forecast": forecast,
    }, default=str, ensure_ascii=False)

    st.session_state["plan"] = dict(
        id=st.session_state.get("plan", {}).get("id", 0) + 1,
        destination=destination, days=days, weather=weather, hotel=hotel, budget=budget,
        itinerary=itinerary, packing=packing, review=review, forecast=forecast,
        forecast_error=forecast_error, rain_changes=rain_changes, interests=interests,
        pdf=pdf, summary=summary, fresh=True,
    )
    st.session_state["chat"] = []

plan = st.session_state.get("plan")

if not plan:
    st.info("👈 Choose your trip details in the sidebar and click **Generate Travel Plan**.")

else:
    weather, hotel, budget = plan["weather"], plan["hotel"], plan["budget"]
    itinerary, packing, review = plan["itinerary"], plan["packing"], plan["review"]
    destination = plan["destination"]

    st.success("Travel Plan Generated Successfully!")

    # ---------------------------
    # Weather (original) + NEW live forecast
    # ---------------------------

    st.header("🌦 Weather Forecast")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Condition", weather["Condition"])
    with c2:
        st.metric("Temperature", weather["Temperature"])
    with c3:
        st.metric("Advice", weather["Advice"])

    st.subheader("📡 Live Forecast for your dates")
    if plan["forecast"]:
        st.dataframe(
            [{"Date": f["date"], "Condition": f["condition"], "Max °C": f["max"],
              "Min °C": f["min"], "Rain chance %": f["rain_prob"]} for f in plan["forecast"]],
            use_container_width=True, hide_index=True,
        )
        if plan["rain_changes"]:
            st.warning("☔ Itinerary adjusted for rain:")
            for change in plan["rain_changes"]:
                st.write("•", change)
        else:
            st.success("No heavy rain expected - the original itinerary is unchanged.")
    else:
        st.info(plan["forecast_error"])

    st.markdown("---")

    # ---------------------------
    # Hotel
    # ---------------------------

    st.header("🏨 Hotel Recommendation")

    if hotel["Status"]:
        st.write(f"### {hotel['Hotel Name']}")
        st.write("**Category:**", hotel["Category"])
        st.write("**Price:**", hotel["Price"])
        st.write("**Rating:**", hotel["Rating"])
        st.write("**Location:**", hotel["Location"])
        st.write("**Amenities:**", hotel["Amenities"])
        st.info(hotel["Reason"])
    else:
        st.error(hotel["Message"])

    st.markdown("---")

    # ---------------------------
    # Budget
    # ---------------------------

    st.header("💰 Estimated Budget")

    if budget["Status"]:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Hotel", budget["Hotel Cost"])
            st.metric("Food", budget["Food Cost"])
        with col2:
            st.metric("Transport", budget["Transport Cost"])
            st.metric("Activities", budget["Activities Cost"])

        st.success(f"Total Budget : {budget['Total Budget']}")
        st.info(budget["Trip Type"])

        st.subheader("Suggestions")
        for tip in budget["Suggestions"]:
            st.write("✔", tip)
    else:
        st.error(budget["Message"])

    st.markdown("---")

    # ---------------------------
    # Itinerary
    # ---------------------------

    st.header("📅 Daily Itinerary")
    if plan["interests"]:
        st.caption("Personalised for: " + ", ".join(plan["interests"]))

    for day in itinerary:
        with st.expander(f"Day {day['Day']}"):
            st.write("🌅 Morning :", day["Morning"])
            st.write("🏃 Afternoon :", day["Afternoon"])
            st.write("🌇 Evening :", day["Evening"])
            st.write("🍽 Food :", day["Food"])
            st.info(day["Tip"])

    st.markdown("---")

    # ---------------------------
    # NEW: Map of popular spots
    # ---------------------------

    st.header("🗺 Map of Popular Spots")
    map_df = get_map_df(destination)
    if not map_df.empty:
        st.map(map_df, latitude="lat", longitude="lon")
        st.caption("Spots: " + ", ".join(map_df["name"]) + " (approximate locations)")
    else:
        st.info("No map data available for this destination.")

    st.markdown("---")

    # ---------------------------
    # Packing Checklist
    # ---------------------------

    st.header("🎒 Packing Checklist")

    for i, item in enumerate(packing):
        st.checkbox(item, value=True, key=f"pack_{plan['id']}_{i}")

    st.markdown("---")

    # ---------------------------
    # Reflection
    # ---------------------------

    if budget["Status"]:
        st.header("🤖 AI Reflection")
        for tip in review:
            st.success(tip)

    st.markdown("---")

    # ---------------------------
    # NEW: Chat assistant
    # ---------------------------

    st.header("💬 Ask about your trip")
    st.caption("Example: 'What if it rains on day 2?' or 'Suggest a cheaper evening plan.'")

    with st.container():
        for m in st.session_state.get("chat", []):
            with st.chat_message(m["role"]):
                st.write(m["content"])

        question = st.chat_input("Ask something about this plan...")

    if question:
        history = st.session_state.get("chat", [])
        with st.spinner("Thinking..."):
            answer = ask_trip_assistant(question, plan["summary"], history)
        history = history + [{"role": "user", "content": question},
                             {"role": "assistant", "content": answer}]
        st.session_state["chat"] = history
        st.rerun()

    st.markdown("---")

    # ---------------------------
    # Previous Trips
    # ---------------------------

    st.header("📜 Previous Trips")

    try:
        history_trips = memory.get_previous_trips()
    except AttributeError:
        history_trips = memory.get_history()

    if len(history_trips) == 0:
        st.info("No previous trips available.")
    else:
        for trip in reversed(history_trips):
            with st.expander(f"{trip['Destination']} ({trip['Budget Type']})"):
                st.write("📍 Destination :", trip["Destination"])
                st.write("📅 Days :", trip["Days"])
                st.write("👨‍👩‍👧 People :", trip["People"])
                st.write("💰 Budget :", trip["Total Budget"])

    st.markdown("---")

    # ---------------------------
    # Download PDF
    # ---------------------------

    if plan["pdf"] is not None:
        st.download_button(
            label="📄 Download Travel Plan (PDF)",
            data=plan["pdf"],
            file_name=f"{destination}_Travel_Plan.pdf",
            mime="application/pdf",
        )

    if plan["fresh"]:
        st.balloons()
        plan["fresh"] = False
