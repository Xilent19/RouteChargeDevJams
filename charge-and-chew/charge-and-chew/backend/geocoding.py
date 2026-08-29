"""
GeoPy-based geocoding: turn a city/address string into (lat, lon).
"""
from geopy.geocoders import Nominatim

_geolocator = Nominatim(user_agent="charge_and_chew")


def geocode(place_name: str) -> tuple[float, float]:
    """
    Convert a place name (e.g. "Seattle, WA") into (lat, lon).

    Raises:
        ValueError: if the place could not be geocoded.
    """
    location = _geolocator.geocode(place_name)
    if location is None:
        raise ValueError(f"Could not geocode location: {place_name!r}")
    return (location.latitude, location.longitude)
