# Shanghai Trip GIS Project

```
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │    🗺  SHANGHAI & SUZHOU TRIP PLANNER                        │
  │                                                             │
  │    GIS-powered trip planning + learning by doing            │
  │                                                             │
  │    Plan  →  Analyze  →  Navigate  →  Tell Stories           │
  │                                                             │
  │    Live map: https://pann13223029.github.io/shanghai-trip-gis│
  │    Repo:     https://github.com/Pann13223029/shanghai-trip-gis│
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

## What Is This?

A collaborative GIS project for planning a 5-6 day group trip to Shanghai and Suzhou. Two tourism students use Geographic Information Systems to organize, visualize, and navigate their trip — while learning GIS skills they can use in their careers.

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │   WHAT    A trip planner built with real GIS tools              │
  │           Interactive web map + offline PDFs + QGIS analysis    │
  │                                                                 │
  │   WHY     Learn GIS by building something real                  │
  │           Turn a real trip into a portfolio piece                │
  │                                                                 │
  │   HOW     Collect POIs in GeoJSON  ──→  Analyze in QGIS         │
  │           Build a web map          ──→  Use it on the ground    │
  │           Take photos + notes      ──→  Create a story map      │
  │                                                                 │
  │   GAIN    Hands-on GIS skills (QGIS, Leaflet, GeoJSON)         │
  │           A working map you can actually use while traveling    │
  │           A portfolio piece showcasing spatial analysis          │
  │           Sustainability analysis connecting GIS to SDGs        │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘
```

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
```

## What This Project Does

- **Plan** — Curate 50+ points of interest across 8 categories (food, landmarks, culture, shopping, nature, transport, accommodation, Suzhou)
- **Visualize** — Interactive web map with themed layers, day-by-day routes, and a sustainability scoring overlay
- **Navigate** — Mobile-friendly map + offline PDF backups for on-the-ground use in China
- **Analyze** — Walking distances, spatial clustering, transit accessibility, and transport CO2 analysis in QGIS
- **Tell Stories** — Post-trip story map combining photos, notes, and reflections into a portfolio piece

### Sustainability Analysis

The project files contain a deeper sustainability analytical layer (separate from the itinerary planning sheet):

- **CO2 transport analysis** — Shanghai-specific emission factors, per-day and trip-total (`tools/co2-calculator.py`)
- **Transit accessibility** — 800m metro buffer analysis measuring SDG 11.2 (`docs/transit-analysis-guide.md`)
- **Heritage preservation** — Comparative analysis of 6 adaptive reuse sites (`docs/adaptive-reuse-analysis.md`)
- **POI scorecards** — 5-dimension sustainability scores on all POIs in the GeoJSON data
- **Carbon context** — Trip CO2 vs flight/commuter comparisons (`docs/carbon-context.md`)
- **Web map toggle** — Sustainability score overlay layer on the interactive map

See [docs/sustainability-methodology.md](docs/sustainability-methodology.md) for full methodology, SDG indicator mapping, and limitations.

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
  ├── index.html                     Root redirect to web map
  ├── serve.sh                       Local dev server helper
  ├── .github/
  │   ├── workflows/validate-geojson.yml  CI: auto-validates GeoJSON
  │   └── ISSUE_TEMPLATE/                 POI + bug report templates
  │
  ├── docs/                          Planning & learning docs
  │   ├── requirements.md            What we're building
  │   ├── roadmap.md                 When we're building it
  │   ├── architecture.md            How it all fits together
  │   ├── learning-journey.md        7-module GIS curriculum
  │   ├── contribution-guide.md      How to add data & push
  │   ├── glossary.md                GIS terms in plain English
  │   ├── qgis-quickstart.md         Visual guide to QGIS
  │   ├── overpass-queries.md        Ready-to-use OSM queries
  │   ├── sustainability-methodology.md  Scoring criteria, emission factors
  │   ├── transit-analysis-guide.md  800m metro buffer analysis (QGIS)
  │   ├── adaptive-reuse-analysis.md 6-site heritage preservation comparison
  │   └── carbon-context.md          Trip CO2 vs commuter, taxi, flight
  │
  ├── data/                          All spatial data (GeoJSON)
  │   ├── poi/                       Points of interest (8 files, 50 POIs)
  │   ├── routes/                    Daily walking routes (24 segments)
  │   ├── areas/                     District boundaries
  │   └── analysis/                  Computed outputs (co2-summary.json)
  │
  ├── tools/                         Scripts
  │   ├── co2-calculator.py          Transport CO2 calculator
  │   ├── create-itinerary-sheet.py  Google Sheet initial builder
  │   ├── rebuild-day-sheets.py      Rebuild Day 1-6 tabs
  │   ├── rebuild-other-sheets.py    Rebuild Overview, All POIs, Checklist
  │   ├── reset-day-tabs.py          Reset day tabs to empty frames
  │   └── clear-day-tabs.py          Clear day tab data only
  │
  └── web/                           Interactive web map
      ├── index.html                 Leaflet.js map + sustainability toggle
      ├── css/style.css              Responsive styles
      ├── story-template.html        Post-trip story map
      └── sw.js                      Service worker (offline)
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
