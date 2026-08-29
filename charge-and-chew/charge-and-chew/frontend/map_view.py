"""
Folium map rendering for the trip route + markers.
Owned by: UI & Map Designer (Member 2)
"""
import folium


def build_trip_map(trip: dict) -> folium.Map:
    geometry = trip["route"]["geometry"]
    center = geometry[len(geometry) // 2]

    m = folium.Map(location=center, zoom_start=6)

    folium.PolyLine(geometry, color="#2563eb", weight=4, opacity=0.8).add_to(m)

    folium.Marker(
        geometry[0], tooltip="Start", icon=folium.Icon(color="green", icon="play")
    ).add_to(m)
    folium.Marker(
        geometry[-1], tooltip="Destination", icon=folium.Icon(color="red", icon="flag")
    ).add_to(m)

    for stop in trip["charging_stops"]:
        popup_lines = [f"<b>{stop['charger_name']}</b>", f"{stop['estimated_charge_time_min']:.0f} min charge"]
        for dish in stop["dining_options"]:
            popup_lines.append(f"🍽️ {dish['name']} — {dish['must_try_dish']}")

        folium.Marker(
            [stop["lat"], stop["lon"]],
            tooltip=f"Stop {stop['stop_number']}",
            popup=folium.Popup("<br>".join(popup_lines), max_width=250),
            icon=folium.Icon(color="blue", icon="bolt", prefix="fa"),
        ).add_to(m)

    return m
