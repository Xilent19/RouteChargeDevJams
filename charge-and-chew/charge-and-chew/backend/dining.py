"""
Gemini-powered dining recommendations for a given charging stop location.
"""
import os
import json
import google.generativeai as genai

_MODEL_NAME = "gemini-1.5-flash"

_PROMPT_TEMPLATE = """You are a local food guide. A traveler is stopping near {location_name}
(lat {lat}, lon {lon}) for about {charge_minutes} minutes while their EV charges.

Recommend exactly 3 real, highly-rated restaurants within a short walk of this location.
For each, give one specific "must-try" dish that is a local specialty.

Respond ONLY with valid JSON, no markdown fences, no commentary, in this exact shape:
[
  {{"name": "...", "cuisine": "...", "must_try_dish": "...", "walk_time_min": <int>}},
  ...
]
"""


def _get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(_MODEL_NAME)


def get_dining_recommendations(
    location_name: str, lat: float, lon: float, charge_minutes: int
) -> list[dict]:
    """
    Returns [{"name", "cuisine", "must_try_dish", "walk_time_min"}, ...] — degrades to
    an empty list on any failure so the rest of the trip plan still renders.
    """
    try:
        model = _get_model()
        prompt = _PROMPT_TEMPLATE.format(
            location_name=location_name, lat=lat, lon=lon, charge_minutes=charge_minutes
        )
        response = model.generate_content(prompt)
        text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(text)
    except Exception as e:  # noqa: BLE001 — MVP: never let a Gemini hiccup crash the trip plan
        print(f"[dining.py] Gemini recommendation failed for {location_name}: {e}")
        return []
