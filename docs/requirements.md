# Requirements

## 1. Functional Requirements

### 1.1 Trip Planning (Pre-Trip)

| ID | Requirement | Priority |
|----|------------|----------|
| F-01 | Add, edit, and delete points of interest (POI) with id, name, category, description, coordinates, and Chinese label | Must |
| F-02 | Organize POIs into categories: Landmarks, Food, Shopping, Cultural/Historical, Nature/Parks, Transport Hubs, Accommodation | Must |
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
| F-14 | Offline fallback via QGIS-exported daily PDF maps and service worker app caching | Should |
| F-15 | Record GPS traces during the trip for post-trip visualization | Could |

> **Note on F-11/F-14:** The custom web map is a **reference tool**, not a primary navigation app in China. GitHub Pages may be blocked by the Great Firewall. Use Amap or Baidu Maps for actual turn-by-turn navigation. See [architecture.md — China Tech Constraints](architecture.md#china-tech-constraints).

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
| F-20 | All 4 members can add/edit POI data (within their owned files) | Must |
| F-21 | Version history of all data changes (via Git) | Must |
| F-22 | Each member has a rotating role assignment per project phase | Should |
| F-23 | Simple contribution workflow that beginners can follow | Must |
| F-24 | Strict file ownership to prevent merge conflicts | Must |

### 1.5 Analysis & Learning

| ID | Requirement | Priority |
|----|------------|----------|
| F-25 | Calculate total walking distance per day | Should |
| F-26 | Buffer analysis — what's within 500m of our hotel? | Should |
| F-27 | Visualize POI clusters to assess geographic efficiency of daily plans | Could |

### 1.6 Sustainability (Optional Enrichment)

For the team member pursuing sustainability analysis:

| ID | Requirement | Priority |
|----|------------|----------|
| F-28 | Record transport mode per route segment (walking, metro, taxi) | Could |
| F-29 | Calculate daily transport CO2 estimates by mode | Could |
| F-30 | Add sustainability_notes to POIs where relevant | Could |

> These are optional enrichment tasks, not required of all team members. They connect the project to SDG 11 (Sustainable Cities) and SDG 12 (Responsible Consumption).

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
| NF-08 | WGS84 coordinates only — no Chinese tile providers in the web map (GCJ-02 avoidance) | Must |
| NF-09 | GeoJSON validation on every push (automated via GitHub Action) | Should |

## 3. Data Requirements

### 3.1 POI Schema

Each point of interest will have these attributes:

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
    "sustainability_notes": "",
    "photos": [],
    "notes": ""
  }
}
```

### 3.2 Allowed Values (Enums)

These fields must use only the values listed below. See also the [Contribution Guide](contribution-guide.md#allowed-values-reference).

| Field | Allowed Values |
|-------|---------------|
| `category` | `landmark`, `food`, `shopping`, `cultural`, `nature`, `transport`, `accommodation` |
| `priority` | `must-visit`, `nice-to-have`, `optional` |
| `day` | `1`, `2`, `3`, `4`, `5`, `6`, or `null` (if undecided) |
| `weather_sensitive` | `true` (outdoor/exposed) or `false` (indoor/covered) |

### 3.3 ID Format

Every feature must have a unique `id` in the format `{category}-{nnn}`:

| Category | ID Range | Example |
|----------|----------|---------|
| Landmarks | `landmark-001` to `landmark-999` | `landmark-001` |
| Food | `food-001` to `food-999` | `food-012` |
| Shopping | `shopping-001` to `shopping-999` | `shopping-003` |
| Cultural | `cultural-001` to `cultural-999` | `cultural-007` |
| Nature | `nature-001` to `nature-999` | `nature-002` |
| Transport | `transport-001` to `transport-999` | `transport-015` |
| Accommodation | `accommodation-001` to `accommodation-999` | `accommodation-001` |
| Suzhou | `suzhou-001` to `suzhou-999` | `suzhou-004` |

When adding a new POI, use the next available number in your category file.

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

| Category | Icon Color | Example POIs |
|----------|-----------|-------------|
| Landmark | Red | The Bund, Oriental Pearl Tower, Shanghai Tower |
| Food | Orange | Nanxiang Steamed Buns, street markets, local restaurants |
| Shopping | Purple | Nanjing Road, Tianzifang, fabric markets |
| Cultural/Historical | Blue | Yu Garden, Jade Buddha Temple, Shanghai Museum |
| Nature/Parks | Green | People's Park, Zhujiajiao Water Town, Suzhou gardens |
| Transport | Gray | Pudong Airport, Hongqiao Station, Metro stations |
| Accommodation | Yellow | Hotel/hostel location(s) |

## 5. Suzhou Day Trip Constraints

Day 6 (Suzhou) requires special planning due to significant transit time:

| Segment | Estimated Time |
|---------|---------------|
| Hotel to Shanghai Hongqiao Station (metro) | 30-60 min |
| Hongqiao to Suzhou Station (high-speed rail) | 25-30 min |
| Suzhou Station to first garden (taxi/bus) | 20-30 min |
| **Total one-way transit** | **75-120 min** |

**Constraints:**
- Maximum 3-4 POIs in Suzhou (after subtracting ~3 hours round-trip transit)
- Plan POIs geographically close to each other (Suzhou's gardens are spread across the city)
- Book high-speed rail tickets in advance (can sell out on weekends)
- Budget time for lunch near one of the gardens

## 6. General Constraints

- All team members are GIS beginners — tooling must have gentle learning curves
- No server-side infrastructure — static hosting only (GitHub Pages)
- GitHub Pages may be blocked in China — see [architecture.md — China Tech Constraints](architecture.md#china-tech-constraints)
- WGS84 coordinates only — Chinese tile providers introduce GCJ-02 offset issues
- Strict file ownership — each member edits only their assigned category files
- Project timeline: ~2 months to trip date
