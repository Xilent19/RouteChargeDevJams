"""
Charge & Chew — Streamlit entry point.
Owned by: UI & Map Designer (Member 2)
"""
import streamlit as st
from dotenv import load_dotenv

from backend.trip_planner import plan_trip, VEHICLE_PROFILES

load_dotenv()

st.set_page_config(page_title="Charge & Chew", page_icon="⚡", layout="wide")
st.title("⚡🍽️ Charge & Chew")
st.caption("Range confidence meets good food. Plan your EV road trip stop by stop.")

with st.form("trip_form"):
    col1, col2 = st.columns(2)
    origin = col1.text_input("Origin", placeholder="Seattle, WA")
    destination = col2.text_input("Destination", placeholder="San Francisco, CA")

    col3, col4 = st.columns(2)
    vehicle_model = col3.selectbox("Vehicle model", list(VEHICLE_PROFILES.keys()))
    start_soc = col4.slider("Starting battery %", 0, 100, 90)

    submitted = st.form_submit_button("Plan my trip")

if submitted:
    with st.spinner("Charting your route and scouting food along the way..."):
        try:
            trip = plan_trip(origin, destination, vehicle_model, start_soc)
        except Exception as e:
            st.error(f"Couldn't plan this trip: {e}")
            st.stop()

    map_col, info_col = st.columns([2, 1])

    with map_col:
        st.subheader("Route")
        # TODO: render with frontend/map_view.py (Folium + streamlit-folium)
        st.write("Map goes here.")

    with info_col:
        st.subheader("Trip Summary")
        summary = trip["trip_summary"]
        st.metric("Total drive + charge time", f"{summary['total_trip_time_min']:.0f} min")
        st.metric("Total charging cost", f"${summary['total_charging_cost_usd']:.2f}")
        st.metric("Charging stops", summary["num_charging_stops"])

        st.subheader("Stops")
        for stop in trip["charging_stops"]:
            with st.container(border=True):
                st.markdown(f"**Stop {stop['stop_number']}: {stop['location_name']}**")
                st.write(f"🔌 {stop['charger_name']} — ~{stop['estimated_charge_time_min']:.0f} min, ${stop['cost_usd']:.2f}")
                for dish in stop["dining_options"]:
                    st.write(f"🍽️ **{dish['name']}** — try the *{dish['must_try_dish']}* ({dish['walk_time_min']} min walk)")
