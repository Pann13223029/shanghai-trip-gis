# Shanghai Trip GIS Project

A collaborative GIS project for planning, visualizing, and navigating a 5-6 day group trip to Shanghai and Suzhou. Built by 4 sustainability and tourism students as both a practical travel tool and a hands-on introduction to Geographic Information Systems.

This project connects GIS skills to sustainable tourism through spatial analysis of transport modes, walkability, and responsible travel planning — aligning with **SDG 11** (Sustainable Cities and Communities) and **SDG 12** (Responsible Consumption and Production).

## What This Project Does

- **Plan** — Curate and organize points of interest across categories (food, landmarks, culture, shopping, nature)
- **Visualize** — Interactive web map with themed layers, day-by-day itineraries, and route visualization
- **Navigate** — Mobile-friendly map for on-the-ground use in Shanghai and Suzhou
- **Analyze** — Route optimization, walking distance calculations, spatial clustering of activities
- **Tell Stories** — Post-trip story map combining photos, notes, and GPS traces into a portfolio piece

## Tech Stack

| Tool | Purpose | Cost |
|------|---------|------|
| [QGIS](https://qgis.org/) | Desktop GIS for analysis and cartography | Free |
| [Leaflet.js](https://leafletjs.com/) | Interactive web map library | Free |
| [OpenStreetMap](https://www.openstreetmap.org/) | Base map tiles | Free |
| [GitHub Pages](https://pages.github.com/) | Web map hosting | Free |
| [geojson.io](https://geojson.io/) | Visual GeoJSON editor | Free |
| [Overpass Turbo](https://overpass-turbo.eu/) | Query OpenStreetMap data | Free |

## Project Structure

```
shanghai-trip-gis/
├── README.md
├── .github/workflows/       # CI: GeoJSON validation
├── docs/                    # Planning and architecture documents
│   ├── requirements.md
│   ├── roadmap.md
│   ├── architecture.md
│   ├── learning-journey.md
│   ├── contribution-guide.md
│   ├── glossary.md
│   └── qgis-quickstart.md
├── data/                    # All GeoJSON data files
│   ├── poi/                 # Points of interest by category
│   ├── routes/              # Walking/transit routes by day
│   └── areas/               # Neighborhood/district polygons
├── web/                     # Leaflet.js web map application
├── offline/                 # QGIS-exported daily PDF maps
└── qgis/                    # QGIS project files and styles
```

## Quick Start

See [docs/contribution-guide.md](docs/contribution-guide.md) to get set up, or start with the [Learning Journey](docs/learning-journey.md) if you're new to GIS. Check the [QGIS Quickstart](docs/qgis-quickstart.md) for a visual guide to desktop GIS, and the [Glossary](docs/glossary.md) for any unfamiliar terms.

> **China note:** GitHub Pages, Google Maps, and many tools are blocked in mainland China. See [Architecture — China Tech Constraints](docs/architecture.md#china-tech-constraints) for mitigation strategies.

## Team

| Member | Rotating Role |
|--------|---------------|
| TBD | Data Collector → Cartographer → Web Dev → Analyst |
| TBD | Cartographer → Analyst → Data Collector → Web Dev |
| TBD | Web Dev → Data Collector → Analyst → Cartographer |
| TBD | Analyst → Web Dev → Cartographer → Data Collector |

Roles rotate each phase so everyone learns every aspect of GIS work.
