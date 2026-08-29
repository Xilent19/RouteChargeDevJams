"""
OSRM-based routing: fetch route geometry, distance, and drive time between two points.
"""
import os
import requests

OSRM_BASE_URL = os.getenv("OSRM_BASE_URL", "https://router.project-osrm.org")


def get_route(origin: tuple[float, float], destination: tuple[float, float]) -> dict:
    """
    Args:
        origin: (lat, lon)
        destination: (lat, lon)

    Returns:
        {
            "geometry": [[lat, lon], ...],
            "distance_km": float,
            "duration_min": float,
        }
    """
    # OSRM expects lon,lat order in the URL
    coords = f"{origin[1]},{origin[0]};{destination[1]},{destination[0]}"
    url = f"{OSRM_BASE_URL}/route/v1/driving/{coords}"
    params = {"overview": "full", "geometries": "geojson"}

    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get("code") != "Ok" or not data.get("routes"):
        raise RuntimeError(f"OSRM routing failed: {data.get('code')}")

    route = data["routes"][0]
    # GeoJSON coords are [lon, lat] — flip to [lat, lon] for Folium
    geometry = [[lat, lon] for lon, lat in route["geometry"]["coordinates"]]

    return {
        "geometry": geometry,
        "distance_km": route["distance"] / 1000,
        "duration_min": route["duration"] / 60,
    }
