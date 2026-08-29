# ⚡🍽️ Charge & Chew

**Turn mandatory EV charging stops into memorable food stops.**

Charge & Chew is an all-in-one trip-planning dashboard for EV road-trippers. It solves the two biggest pain points of long-distance EV travel:

- **Range anxiety** — not knowing where to charge, how long it'll take, or what the trip will actually cost.
- **Charging boredom** — 30–45 minutes of dead time at a charger with nothing to do.

Instead of treating charging stops as passive dots on a map, Charge & Chew calculates exactly where you need to stop based on real-world battery buffers, then curates top-rated local restaurants and must-try dishes within walking distance — so every charge becomes a chance to eat somewhere great.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **Smart Range & Buffer Engine** | Calculates battery consumption using real-world State-of-Charge (SOC) buffers to plot optimal waypoints without ever draining the battery to zero. |
| **Charger & Cost Aggregator** | Identifies compatible fast chargers at each stop and projects total trip cost based on kWh needed. |
| **Time-Synced Culinary Curation** | Recommends restaurants within walking distance of each charging stop and uses AI to surface "must-try" dishes local to that region. |
| **Live Interactive Itinerary** | A side-by-side dashboard: interactive route map on one side, trip metrics (drive time, charge time, dining stops, total cost) on the other. |

---

## 🏗️ Tech Stack

| Layer | Tools |
|---|---|
| Frontend & Mapping | [Streamlit](https://streamlit.io/) + [Folium](https://python-visualization.github.io/folium/) (via `streamlit-folium`) |
| Routing & Distance | [GeoPy](https://geopy.readthedocs.io/) (geocoding) + [OSRM API](http://project-osrm.org/) (route geometry) |
| EV & AI Data | [OpenChargeMap API](https://openchargemap.org/site/develop/api) (charger metadata) + [Gemini 1.5 Flash API](https://ai.google.dev/) (restaurant/dish extraction) |

---

## 📐 Architecture

```
User Input (Streamlit form)
        │
        ▼
┌───────────────────┐      ┌──────────────────────┐
│   Backend Engine    │      │   Frontend / UI        │
│  (backend/)          │─────▶│  (frontend/)            │
│                      │ JSON │                         │
│  • geocode()         │      │  • Folium map render    │
│  • get_route()       │      │  • Metric cards         │
│  • plan_charging()   │      │  • Dining cards         │
│  • get_dining()      │      │                         │
│  • plan_trip()  ◀────┼──────┼─ single entry point     │
└───────────────────┘      └──────────────────────┘
```

`backend.plan_trip()` is the single contract between the two halves of the app — see [`docs/data_contract.md`](docs/data_contract.md).

---

## 🗂️ Project Structure

```
charge-and-chew/
├── backend/
│   ├── __init__.py
│   ├── geocoding.py       # GeoPy: city name → lat/lon
│   ├── routing.py         # OSRM: route geometry & drive time
│   ├── range_engine.py    # SOC/battery buffer math, waypoint calc
│   ├── chargers.py        # OpenChargeMap: find compatible fast chargers
│   ├── cost.py            # kWh & cost calculations
│   ├── dining.py          # Gemini: restaurant + dish recommendations
│   └── trip_planner.py    # Orchestrates all of the above → TripPlan
├── frontend/
│   ├── app.py              # Streamlit entry point
│   ├── map_view.py         # Folium map rendering
│   └── components.py       # Metric cards, dining cards, layout helpers
├── assets/                 # Icons, sample screenshots
├── docs/
│   └── data_contract.md    # Shared JSON schema between backend & frontend
├── .env.example
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone & set up environment
```bash
git clone https://github.com/<your-org>/charge-and-chew.git
cd charge-and-chew
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API keys
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```
```
OPENCHARGEMAP_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```
- Get an OpenChargeMap key: https://openchargemap.org/site/develop/api
- Get a Gemini API key: https://ai.google.dev/

### 3. Run the app
```bash
streamlit run frontend/app.py
```

---

## 👥 Team

| Role | Owner | Scope |
| :--- | :--- | :--- |
| **Data & Routing (Backend)** | Akshaj | Geocoding, OSRM routing, OpenChargeMap querying, Gemini dining recommendations |
| **UI & Map Design (Frontend)** | Sarthak | Streamlit UI, Folium map rendering, layout, dining/metric cards |
| **API & Services (Backend)** | Arsh | Fetch route coordinates, locate charging stations |

See [`docs/data_contract.md`](docs/data_contract.md) for how the two halves connect.

---

## 🗺️ Roadmap

- [ ] Geocoding + OSRM route fetch
- [ ] SOC-based range/buffer engine
- [ ] OpenChargeMap integration
- [ ] Cost calculator
- [ ] Gemini dining recommendation prompt + parsing
- [ ] Streamlit input form
- [ ] Folium map with route + markers
- [ ] Trip metrics + dining cards layout
- [ ] End-to-end integration
- [ ] Demo polish (cached fallback route, error handling)

---

## 📄 License

MIT — see [LICENSE](LICENSE).
