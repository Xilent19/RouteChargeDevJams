"""
OpenChargeMap integration: find compatible fast chargers near a given point.
"""
import os
import requests

OCM_BASE_URL = "https://api.openchargemap.io/v3/poi/"


def find_chargers_near(
    lat: float,
    lon: float,
    max_results: int = 5,
    distance_km: int = 10,
    connector_types: list[str] | None = None,
) -> list[dict]:
    """
    Returns a list of nearby charging stations:
        [{"name": ..., "lat": ..., "lon": ..., "connector_types": [...], "operator": ...}, ...]
    """
    api_key = os.getenv("OPENCHARGEMAP_API_KEY")
    params = {
        "output": "json",
        "latitude": lat,
        "longitude": lon,
        "distance": distance_km,
        "distanceunit": "KM",
        "maxresults": max_results,
        "key": api_key,
        # Level 3 = DC fast charging
        "levelid": 3,
    }

    resp = requests.get(OCM_BASE_URL, params=params, timeout=15)
    resp.raise_for_status()
    results = resp.json()

    chargers = []
    for poi in results:
        connections = poi.get("Connections", []) or []
        conn_types = [c.get("ConnectionType", {}).get("Title", "Unknown") for c in connections]

        if connector_types and not any(ct in connector_types for ct in conn_types):
            continue

        chargers.append({
            "name": poi.get("AddressInfo", {}).get("Title", "Unknown Station"),
            "lat": poi.get("AddressInfo", {}).get("Latitude"),
            "lon": poi.get("AddressInfo", {}).get("Longitude"),
            "connector_types": conn_types,
            "operator": (poi.get("OperatorInfo") or {}).get("Title", "Unknown"),
        })

    return chargers
