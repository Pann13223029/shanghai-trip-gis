# Requirements

```
  Priority Legend:
  ┌──────────┬──────────────────────────────────────────────┐
  │  Must    │  Required for the project to function        │
  │  Should  │  Important — plan to include                 │
  │  Could   │  Nice-to-have — include if time allows       │
  └──────────┴──────────────────────────────────────────────┘
```

## 1. Functional Requirements

### 1.1 Trip Planning (Pre-Trip)

| ID | Requirement | Priority |
|----|------------|----------|
| F-01 | Add, edit, and delete POIs with id, name, category, description, coordinates, and Chinese label | Must |
| F-02 | Organize POIs into categories: Landmarks, Food, Shopping, Cultural/Historical, Nature/Parks, Transport, Accommodation | Must |
| F-03 | Assign POIs to specific trip days (Day 1-5 Shanghai, Day 6 Suzhou) | Must |
| F-04 | Visualize all POIs on an interactive map with category-based icons and colors | Must |
| F-05 | Toggle map layers on/off by category and by day | Must |
| F-06 | Calculate walking/transit distances between POIs | Should |
| F-07 | Suggest optimized routes for each day based on proximity | Should |
| F-08 | Display Shanghai district/neighborhood boundaries as reference polygons | Should |
| F-09 | Show transit lines (metro) as an overlay layer | Could |
| F-10 | Add estimated time and cost per POI visit | Could |

### 1.2 On-the-Ground Navigation (During Trip)

| ID | Requirement | Priority |
|----|------------|----------|
| F-11 | Mobile-responsive map that works on phone browsers | Must |
| F-12 | Show current day's itinerary with route lines between stops | Must |
| F-13 | Display Chinese name prominently for showing to taxi drivers / locals | Must |
| F-14 | Offline fallback via QGIS-exported daily PDF maps | Should |
| F-15 | Record GPS traces during the trip for post-trip visualization | Could |

> **Note:** The custom web map is a **reference tool**, not a primary navigation app in China. Use Amap or Baidu Maps for turn-by-turn navigation. See [architecture.md — China Tech Constraints](architecture.md#china-tech-constraints).

### 1.3 Post-Trip Story Map (After Trip)

| ID | Requirement | Priority |
|----|------------|----------|
| F-16 | Attach photos to POIs visited | Should |
| F-17 | Add trip notes/journal entries geotagged to locations | Should |
| F-18 | Populate a story map template with day-by-day narrative, photos, and map views | Should |
| F-19 | Export final map as a static image or PDF for portfolio | Should |

### 1.4 Collaboration

| ID | Requirement | Priority |
|----|------------|----------|
| F-20 | Both members can add/edit any POI data file | Must |
| F-21 | Version history of all data changes (via Git) | Must |
| F-22 | Primary file responsibility per person (not exclusive ownership) | Should |
| F-23 | Simple contribution workflow that beginners can follow | Must |

### 1.5 Analysis & Learning

| ID | Requirement | Priority |
|----|------------|----------|
| F-24 | Calculate total walking distance per day | Should |
| F-25 | Buffer analysis — what's within 500m of our hotel? | Should |
| F-26 | Visualize POI clusters to assess geographic efficiency of daily plans | Could |

### 1.6 Sustainability Analysis

```
  ┌─────────────────────────────────────────────────────────┐
  │  Person 2 leads sustainability analysis.                │
  │  Person 1 supports with route data and transport modes. │
  │                                                         │
  │  Connects to:                                           │
  │    SDG 11 — Sustainable Cities and Communities          │
  │    SDG 12 — Responsible Consumption and Production      │
  └─────────────────────────────────────────────────────────┘
```

| ID | Requirement | Priority |
|----|------------|----------|
| F-27 | Record transport mode per route segment (walking, metro, taxi) | Should |
| F-28 | Calculate daily transport CO2 estimates by mode | Should |
| F-29 | Add sustainability_notes to POIs where relevant | Should |

## 2. Non-Functional Requirements

| ID | Requirement | Priority |
|----|------------|----------|
| NF-01 | Zero cost — all tools and hosting must be free tier | Must |
| NF-02 | Works on modern mobile browsers (Chrome, Safari) without app install | Must |
| NF-03 | Page load under 3 seconds on 4G connection (outside China) | Should |
| NF-04 | Beginner-friendly — no prior GIS or coding experience required to contribute data | Must |
| NF-05 | All data stored as GeoJSON (human-readable, Git-friendly) | Must |
| NF-06 | Portfolio-quality visual design | Should |
| NF-07 | English UI with Chinese (中文) labels on place names | Must |
| NF-08 | WGS84 coordinates only — no Chinese tile providers in the web map | Must |
| NF-09 | GeoJSON validation on every push (automated via GitHub Action) | Should |

## 3. Data Requirements

### 3.1 POI Schema

```
  Required fields (must fill):     Optional fields (fill if known):
  ┌───────────────────────────┐    ┌───────────────────────────┐
  │  id                       │    │  est_cost_cny             │
  │  name_en                  │    │  opening_hours            │
  │  name_cn                  │    │  weather_sensitive        │
  │  category                 │    │  sustainability_notes     │
  │  day                      │    │  last_verified            │
  │  description              │    │  photos                   │
  │  address                  │    │  notes                    │
  │  est_duration_min         │    │                           │
  │  priority                 │    │  Sustainability scorecard │
  │  added_by                 │    │  (see methodology doc):   │
  │  coordinates [lng, lat]   │    │  transit_access (0-3)     │
  └───────────────────────────┘    │  heritage_value (0-3)     │
                                   │  community_impact (string)│
                                   │  walkability (0-3)        │
                                   │  environmental_sensitivity│
                                   │  sustainability_score     │
                                   └───────────────────────────┘
```

Full example:

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [121.4907, 31.2397]
  },
  "properties": {
    "id": "landmark-001",
    "name_en": "The Bund",
    "name_cn": "外滩",
    "category": "landmark",
    "day": 1,
    "description": "Iconic waterfront promenade with views of Pudong skyline",
    "address": "Zhongshan East 1st Rd, Huangpu District",
    "est_duration_min": 60,
    "est_cost_cny": 0,
    "opening_hours": "24/7",
    "priority": "must-visit",
    "weather_sensitive": true,
    "added_by": "member_name",
    "last_verified": "2026-03",
    "sustainability_notes": "Iconic waterfront promenade; fully pedestrian, high transit access via Line 2/10",
    "transit_access": 3,
    "heritage_value": 2,
    "community_impact": "positive",
    "walkability": 3,
    "environmental_sensitivity": 2,
    "sustainability_score": 10,
    "photos": [],
    "notes": ""
  }
}
```

Scorecard scoring criteria are defined in [sustainability-methodology.md](sustainability-methodology.md). Set scorecard fields to `null` for POIs where sustainability assessment isn't meaningful (airports, metro stations, generic restaurants).

### 3.2 Allowed Values (Enums)

| Field | Allowed Values |
|-------|---------------|
| `category` | `landmark`, `food`, `shopping`, `cultural`, `nature`, `transport`, `accommodation` |
| `priority` | `must-visit`, `nice-to-have`, `optional` |
| `day` | `1`, `2`, `3`, `4`, `5`, `6`, or `null` (if undecided) |
| `weather_sensitive` | `true` (outdoor/exposed) or `false` (indoor/covered) |
| `transit_access` | `0`, `1`, `2`, `3`, or `null` (see [methodology](sustainability-methodology.md)) |
| `heritage_value` | `0`, `1`, `2`, `3`, or `null` |
| `community_impact` | `positive`, `mixed`, `negative`, `neutral`, or `null` |
| `walkability` | `0`, `1`, `2`, `3`, or `null` |
| `environmental_sensitivity` | `0`, `1`, `2`, `3`, or `null` |
| `sustainability_score` | `0`-`12` (computed sum of numeric scores) or `null` |

### 3.3 ID Format

```
  Format:  {category}-{nnn}
  Example: food-001, landmark-012, suzhou-003

  When adding a new POI:
  1. Open your category file
  2. Find the highest existing number
  3. Use the next number (zero-padded to 3 digits)
```

### 3.4 Route Schema

```json
{
  "type": "Feature",
  "geometry": {
    "type": "LineString",
    "coordinates": [[121.4907, 31.2397], [121.4925, 31.2272]]
  },
  "properties": {
    "day": 1,
    "from_id": "landmark-001",
    "from_name": "The Bund",
    "to_id": "cultural-001",
    "to_name": "Yu Garden",
    "mode": "walking",
    "distance_km": 1.2,
    "duration_min": 15
  }
}
```

| Field | Allowed Values |
|-------|---------------|
| `mode` | `walking`, `metro`, `taxi`, `bus`, `train` |

### 3.5 Area Schema

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[121.44, 31.20], [121.48, 31.20], [121.48, 31.24], [121.44, 31.24], [121.44, 31.20]]]
  },
  "properties": {
    "name_en": "French Concession",
    "name_cn": "法租界",
    "type": "neighborhood",
    "description": "Tree-lined streets with cafes, boutiques, and colonial architecture"
  }
}
```

## 4. Categories

```
  Category          Color     Examples
  ─────────────────────────────────────────────────────
  Landmark          ■ Red     The Bund, Shanghai Tower
  Food              ■ Orange  Nanxiang Dumplings, Yang's
  Shopping          ■ Purple  Nanjing Rd, Tianzifang
  Cultural          ■ Blue    Yu Garden, Shanghai Museum
  Nature/Parks      ■ Green   People's Park, Fuxing Park
  Transport         ■ Gray    Pudong Airport, Metro hubs
  Accommodation     ■ Yellow  Hotel/hostel
```

## 5. Suzhou Day Trip Constraints

```
  ┌─────────────────────────────────────────────────────────┐
  │  SUZHOU DAY TRIP — TIME BUDGET                          │
  │                                                         │
  │  Hotel → Hongqiao Station (metro)     30-60 min         │
  │  Hongqiao → Suzhou (high-speed rail)  25-30 min         │
  │  Suzhou Station → first garden        20-30 min         │
  │  ──────────────────────────────────────────────         │
  │  Total one-way transit:               75-120 min        │
  │  Round trip transit:                  ~3 hours           │
  │                                                         │
  │  Available sightseeing time:          ~7-8 hours        │
  │  Maximum POIs:                        3-4               │
  │                                                         │
  │  Book high-speed rail tickets in advance!               │
  └─────────────────────────────────────────────────────────┘
```

## 6. Constraints

- 2-person team — one Lead (technical), one sustainability-focused student
- No server-side infrastructure — static hosting only (GitHub Pages)
- GitHub Pages may be blocked in China — see [architecture.md](architecture.md#china-tech-constraints)
- WGS84 coordinates only — Chinese tile providers introduce GCJ-02 offset
- Primary file responsibility — each person curates ~4 files, cross-editing OK
- Project timeline: ~2 months to trip date
