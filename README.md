# Shanghai Trip GIS Project

```
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │    🗺  SHANGHAI & SUZHOU TRIP PLANNER                        │
  │                                                             │
  │    GIS-powered travel planning with a sustainability lens   │
  │                                                             │
  │    Plan  →  Analyze  →  Navigate  →  Tell Stories           │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

A collaborative GIS project for planning, visualizing, and navigating a 5-6 day group trip to Shanghai and Suzhou. Built by 2 sustainability and tourism students as both a practical travel tool and a hands-on introduction to Geographic Information Systems, with a focus on sustainable urban tourism analysis.

This project connects GIS skills to sustainable tourism through spatial analysis of transport modes, walkability, and responsible travel planning — aligning with **SDG 11** (Sustainable Cities and Communities) and **SDG 12** (Responsible Consumption and Production).

## How It Works

```
  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
  │          │     │          │     │          │     │          │
  │  PLAN    │────▶│ ANALYZE  │────▶│ NAVIGATE │────▶│  STORY   │
  │          │     │          │     │          │     │   MAP    │
  └──────────┘     └──────────┘     └──────────┘     └──────────┘
   Collect POIs     QGIS buffers     Web map on       Photos +
   in GeoJSON       distances        phones           reflections
                    clusters         PDF fallbacks     portfolio
                    CO2 analysis     Amap in China     SDG analysis
```

## What This Project Does

- **Plan** — Curate and organize points of interest across categories (food, landmarks, culture, shopping, nature)
- **Visualize** — Interactive web map with themed layers, day-by-day itineraries, and route visualization
- **Navigate** — Mobile-friendly map for on-the-ground use in Shanghai and Suzhou
- **Analyze** — Walking distances, spatial clustering, transport mode sustainability analysis
- **Tell Stories** — Post-trip story map combining photos, notes, and sustainability reflections into a portfolio piece

## Tech Stack

```
  ┌─────────────────────────────────────────────────────────┐
  │                     TOOLS WE USE                         │
  ├─────────────┬───────────────────────────┬───────────────┤
  │  DESKTOP    │  WEB                      │  DATA         │
  │             │                           │               │
  │  QGIS       │  Leaflet.js (map library) │  GeoJSON      │
  │  (analysis, │  GitHub Pages (hosting)   │  (all our     │
  │   styling,  │  HTML/CSS/JS (vanilla)    │   spatial     │
  │   PDF maps) │                           │   data)       │
  ├─────────────┼───────────────────────────┼───────────────┤
  │  FREE       │  FREE                     │  FREE         │
  └─────────────┴───────────────────────────┴───────────────┘

  Base map tiles:  OpenStreetMap via CartoDB Voyager
  Data editor:     geojson.io (visual) or VS Code (text)
  OSM queries:     Overpass Turbo
```

## Project Structure

```
  shanghai-trip-gis/
  │
  ├── README.md                      ← you are here
  ├── .github/
  │   ├── workflows/validate.yml     CI: auto-validates GeoJSON
  │   └── ISSUE_TEMPLATE/            POI + bug report templates
  │
  ├── docs/                          Planning & learning docs
  │   ├── requirements.md            What we're building
  │   ├── roadmap.md                 When we're building it
  │   ├── architecture.md            How it all fits together
  │   ├── learning-journey.md        7-module GIS curriculum
  │   ├── contribution-guide.md      How to add data & push
  │   ├── glossary.md                GIS terms in plain English
  │   ├── qgis-quickstart.md         Visual guide to QGIS
  │   └── overpass-queries.md        Ready-to-use OSM queries
  │
  ├── data/                          All spatial data (GeoJSON)
  │   ├── poi/                       Points of interest (8 files)
  │   │   ├── landmarks.geojson      The Bund, Shanghai Tower...
  │   │   ├── food.geojson           Dumplings, hot pot...
  │   │   ├── shopping.geojson       Nanjing Rd, Tianzifang...
  │   │   ├── cultural.geojson       Yu Garden, museums...
  │   │   ├── nature.geojson         Parks, riverside...
  │   │   ├── transport.geojson      Airports, metro hubs...
  │   │   ├── accommodation.geojson  Hotel (anchor point)
  │   │   └── suzhou.geojson         Day trip POIs
  │   ├── routes/                    Daily walking routes
  │   └── areas/                     District boundaries
  │
  ├── web/                           Interactive web map
  │   ├── index.html                 Leaflet.js starter template
  │   ├── css/style.css              Responsive styles
  │   ├── story-template.html        Post-trip story map
  │   └── sw.js                      Service worker (offline)
  │
  ├── offline/                       QGIS-exported daily PDFs
  └── qgis/                          QGIS project files
```

## Quick Start

```
  New here?  Follow this path:
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  1. Read the Contribution Guide ──→ Get tools set up    │
  │  2. Read the Learning Journey   ──→ Start Module 1      │
  │  3. Check the QGIS Quickstart   ──→ When you open QGIS  │
  │  4. Check the Glossary          ──→ When terms confuse   │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

- [Contribution Guide](docs/contribution-guide.md) — get set up and start adding data
- [Learning Journey](docs/learning-journey.md) — 7-module GIS curriculum
- [QGIS Quickstart](docs/qgis-quickstart.md) — visual guide to desktop GIS
- [Glossary](docs/glossary.md) — GIS terms in plain English

> **China note:** GitHub Pages, Google Maps, and many tools are blocked in mainland China. See [Architecture — China Tech Constraints](docs/architecture.md#china-tech-constraints) for mitigation strategies.

## Team

```
  ┌───────────────────────────────────────────────────────┐
  │  Person 1 (Lead)          Person 2                    │
  │  ─────────────────        ──────────────────          │
  │  Web development          POI research & curation     │
  │  Git & deployment         QGIS cartography & styling  │
  │  Spatial analysis         Sustainability analysis     │
  │  Architecture decisions   Story map narrative         │
  │                                                       │
  │  Primary files:           Primary files:              │
  │  · landmarks.geojson      · cultural.geojson          │
  │  · food.geojson           · shopping.geojson          │
  │  · transport.geojson      · nature.geojson            │
  │  · accommodation.geojson  · suzhou.geojson            │
  │                                                       │
  │  Either person can edit any file with communication.  │
  └───────────────────────────────────────────────────────┘
```

Both people participate in all phases through pair learning sessions. The Lead drives technical work; Person 2 drives data, sustainability, and narrative work.
