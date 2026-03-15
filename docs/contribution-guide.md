# Contribution Guide

```
  ┌─────────────────────────────────────────────────────────┐
  │                   YOUR WORKFLOW                          │
  │                                                         │
  │   1. Fetch   ──→  Get latest changes from GitHub        │
  │   2. Edit    ──→  Add/modify POIs in your files         │
  │   3. Validate ─→  Check at geojsonlint.com              │
  │   4. Commit  ──→  Describe what you changed             │
  │   5. Push    ──→  Upload to GitHub                      │
  │                                                         │
  │                                                         │
  │   Live map: pann13223029.github.io/shanghai-trip-gis     │
  └─────────────────────────────────────────────────────────┘
```

A step-by-step guide for adding data and making changes to the Shanghai Trip GIS project. Written for beginners — no prior Git or GIS experience needed.

---

## Getting Started (One-Time Setup)

### 1. Install Tools

| Tool | Download | Purpose |
|------|----------|---------|
| GitHub Desktop | [desktop.github.com](https://desktop.github.com/) | Push/pull changes without command line |
| QGIS | [qgis.org/download](https://qgis.org/en/site/forusers/download.html) | Desktop GIS for analysis |
| VS Code | [code.visualstudio.com](https://code.visualstudio.com/) | Text editor for GeoJSON files |
| Chrome | Already have it | Testing the web map |

### 2. Clone the Repository

```
  GitHub Desktop:

  ┌─────────────────────────────────────────────┐
  │  File → Clone Repository                    │
  │                                             │
  │  ┌───────────────────────────────────────┐  │
  │  │ shanghai-trip-gis                     │  │
  │  └───────────────────────────────────────┘  │
  │                                             │
  │  Local path: /Users/you/shanghai-trip-gis   │
  │                                             │
  │              [Clone]                         │
  └─────────────────────────────────────────────┘
```

### 3. Open in VS Code

1. In GitHub Desktop, click **Open in Visual Studio Code**
2. VS Code will suggest recommended extensions — click **Install All**
3. The **GeoJSON Map Preview** extension lets you see your data on a map inside VS Code

---

## File Responsibility

```
  ┌───────────────────────────────────────────────────────┐
  │                                                       │
  │  Person 1 (Lead)           Person 2                   │
  │  primary files:            primary files:             │
  │  ┌────────────────────┐    ┌────────────────────┐     │
  │  │ landmarks.geojson  │    │ cultural.geojson   │     │
  │  │ food.geojson       │    │ shopping.geojson   │     │
  │  │ transport.geojson  │    │ nature.geojson     │     │
  │  │ accommodation      │    │ suzhou.geojson     │     │
  │  └────────────────────┘    └────────────────────┘     │
  │                                                       │
  │  Either person CAN edit any file.                     │
  │  Just use a clear commit message.                     │
  │                                                       │
  └───────────────────────────────────────────────────────┘
```

Each person is the **primary editor** for their assigned files. This means you're responsible for the quality and completeness of those files. But cross-editing is fine — if you find a great restaurant while researching nature POIs, just add it to `food.geojson` with a clear commit message.

---

## Allowed Values Reference

```
  Field              Allowed Values
  ──────────────────────────────────────────────────────────
  category           landmark | food | shopping | cultural
                     nature | transport | accommodation

  priority           must-visit | nice-to-have | optional

  day                1 | 2 | 3 | 4 | 5 | 6 | null

  weather_sensitive  true (outdoor) | false (indoor)

  mode (routes)      walking | metro | taxi | bus | train

  Sustainability scorecard (see sustainability-methodology.md):
  ──────────────────────────────────────────────────────────
  transit_access     0 | 1 | 2 | 3 | null
  heritage_value     0 | 1 | 2 | 3 | null
  community_impact   positive | mixed | negative | neutral | null
  walkability        0 | 1 | 2 | 3 | null
  env_sensitivity    0 | 1 | 2 | 3 | null
  sustainability_score  0-12 (computed sum) | null
```

Use these values exactly. Other values will break the map's filters.

---

## Adding a New POI

### Method A: Using geojson.io (Easiest)

```
  ┌─────────────────────────────────────────────────────────┐
  │  geojson.io                                             │
  │  ┌─────────────────────────┬──────────────────────────┐ │
  │  │                         │  {                       │ │
  │  │      MAP VIEW           │    "type": "Feature",   │ │
  │  │                         │    "properties": {      │ │
  │  │   Click to place a      │      "name_en": "...",  │ │
  │  │   marker ──→ ●          │      "name_cn": "...",  │ │
  │  │                         │      ...                │ │
  │  │                         │    }                    │ │
  │  │                         │  }                      │ │
  │  └─────────────────────────┴──────────────────────────┘ │
  │                                                         │
  │  1. Navigate to Shanghai                                │
  │  2. Click marker tool, place your point                 │
  │  3. Edit properties in the right panel                  │
  │  4. Save → GeoJSON → download                           │
  │  5. Copy the Feature into your category file            │
  └─────────────────────────────────────────────────────────┘
```

### Method B: Editing GeoJSON Directly

Open your file in VS Code and add a new Feature to the `"features"` array:

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [121.4925, 31.2272]
  },
  "properties": {
    "id": "food-012",
    "name_en": "Nanxiang Steamed Bun Restaurant",
    "name_cn": "南翔馒头店",
    "category": "food",
    "day": 2,
    "description": "Famous xiaolongbao since 1900, next to Yu Garden",
    "address": "85 Yuyuan Rd, Huangpu District",
    "est_duration_min": 45,
    "est_cost_cny": 30,
    "opening_hours": "9:00-21:00",
    "priority": "must-visit",
    "weather_sensitive": false,
    "added_by": "your_name",
    "last_verified": "2026-03",
    "sustainability_notes": "",
    "transit_access": null,
    "heritage_value": null,
    "community_impact": null,
    "walkability": null,
    "environmental_sensitivity": null,
    "sustainability_score": null,
    "photos": [],
    "notes": ""
  }
}
```

### How to Find Coordinates

```
  BEFORE THE TRIP (Google Maps):
  ┌──────────────────────────────────────────────┐
  │  1. Search for the place on Google Maps      │
  │  2. Right-click → coordinates appear         │
  │     e.g., 31.2272, 121.4925                  │
  │  3. SWAP THE ORDER for GeoJSON:              │
  │     [121.4925, 31.2272]                      │
  │      ↑ lng      ↑ lat                        │
  │                                              │
  │  ⚠ GeoJSON = [lng, lat]                     │
  │  ⚠ Google  = lat, lng    ← opposite!        │
  └──────────────────────────────────────────────┘

  IN CHINA (Google is blocked):
  Use Dianping (大众点评) for restaurants
  Use Amap (高德地图) for general places
```

### ID Assignment

```
  Check your file for the highest existing number:
  food-009, food-010, food-011
                              └──→ next is food-012
```

---

## Pushing Your Changes

### Step-by-Step

```
  GitHub Desktop:

  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  1. Click [Fetch origin]     ← get latest changes       │
  │                                                         │
  │  2. (edit your files)                                   │
  │                                                         │
  │  3. See changed files        ← left panel               │
  │     in GitHub Desktop                                   │
  │                                                         │
  │  4. Write a summary:                                    │
  │     ┌─────────────────────────────────────────────┐     │
  │     │ Add 5 food POIs in Huangpu district         │     │
  │     └─────────────────────────────────────────────┘     │
  │     Good: "Add 5 food POIs in Huangpu district"         │
  │     Bad:  "update"                                      │
  │                                                         │
  │  5. Click [Commit to main]                              │
  │                                                         │
  │  6. Click [Push origin]                                 │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

### Before You Push — Checklist

```
  ☐  Every POI has a unique id in the correct format
  ☐  Coordinates are [longitude, latitude] order
  ☐  Coordinates place the marker correctly (check geojson.io satellite view)
  ☐  name_cn is filled in
  ☐  category matches the filename
  ☐  priority is: must-visit | nice-to-have | optional
  ☐  day is 1-6 or null
  ☐  added_by has your name
  ☐  File passes validation at geojsonlint.com
  ☐  Commit message describes what you changed
```

### If Something Goes Wrong

```
  PROBLEM                          FIX
  ─────────────────────────────    ──────────────────────────────
  "Conflict" message               Person 1 (Lead) resolves it.
                                   Person 2: don't try to fix.

  Red X on your commit             GeoJSON syntax error. Paste
  in GitHub                        file into geojsonlint.com,
                                   fix the error, commit again.

  Accidentally edited the          Right-click the file in
  wrong file                       GitHub Desktop → Discard changes
```

---

## Responsibilities

```
  ┌─────────────────────────────────────────────────────────┐
  │  PERSON 1 (Lead)                                        │
  │                                                         │
  │  · Web map development (Leaflet.js)                     │
  │  · Git & GitHub deployment                              │
  │  · Spatial analysis in QGIS (buffers, distances)        │
  │  · Architecture & technical decisions                   │
  │  · Creates QGIS print layout template                   │
  │  · Resolves any Git conflicts                           │
  ├─────────────────────────────────────────────────────────┤
  │  PERSON 2                                               │
  │                                                         │
  │  · POI research & curation                              │
  │  · QGIS cartography & layer styling                     │
  │  · Sustainability analysis (transport modes, CO2)       │
  │  · Exports daily PDF maps using print template          │
  │  · Story map narrative writing                          │
  │  · Tests web map on mobile, reviews Chinese labels      │
  ├─────────────────────────────────────────────────────────┤
  │  BOTH                                                   │
  │                                                         │
  │  · Itinerary planning (day assignments)                 │
  │  · Learning modules (pair sessions)                     │
  │  · Trip data collection (photos, notes, GPS)            │
  │  · Final review & polish                                │
  └─────────────────────────────────────────────────────────┘
```

Both people participate in all phases through pair sessions. The above lists who **leads** each activity, not who does it alone.

---

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| POI data | `data/poi/{category}.geojson` | `data/poi/food.geojson` |
| Route data | `data/routes/day-{n}.geojson` | `data/routes/day-1.geojson` |
| Area data | `data/areas/{name}.geojson` | `data/areas/districts.geojson` |
| Offline PDFs | `offline/day-{n}.pdf` | `offline/day-1.pdf` |
| Photos | `web/assets/photos/{day}/{name}.jpg` | `web/assets/photos/day-1/bund-sunset.jpg` |

---

## Getting Help

```
  QUESTION                          WHERE TO LOOK
  ─────────────────────────────    ──────────────────────────────
  GeoJSON syntax error?             geojsonlint.com
  Can't find coordinates?           Google Maps (pre-trip)
                                    Amap / Dianping (in China)
  Git conflict?                     Person 1 (Lead) handles it
  QGIS confusing?                   docs/qgis-quickstart.md
  Leaflet question?                 leafletjs.com/examples.html
  Need Chinese name?                Dianping or Baidu Maps
  Unfamiliar GIS term?              docs/glossary.md
  Sustainability scoring?           docs/sustainability-methodology.md
  Transit analysis (QGIS)?          docs/transit-analysis-guide.md
  CO2 calculator?                   tools/co2-calculator.py
```
