# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                          │
│  geojson.io  ·  QGIS  ·  Overpass API  ·  Manual edit  │
└──────────────────────┬──────────────────────────────────┘
                       │ GeoJSON files
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   GIT REPOSITORY                         │
│                                                          │
│  data/                                                   │
│  ├── poi/           (Point features by category)         │
│  │   ├── landmarks.geojson                               │
│  │   ├── food.geojson                                    │
│  │   ├── shopping.geojson                                │
│  │   ├── cultural.geojson                                │
│  │   ├── nature.geojson                                  │
│  │   ├── transport.geojson                               │
│  │   ├── accommodation.geojson                           │
│  │   └── suzhou.geojson                                  │
│  ├── routes/        (LineString features)                │
│  │   ├── day-1.geojson  ...  day-6.geojson               │
│  │   └── metro.geojson                                   │
│  └── areas/         (Polygon features)                   │
│      ├── districts.geojson                               │
│      └── neighborhoods.geojson                           │
│                                                          │
│  web/               (Static web application)             │
│  ├── index.html                                          │
│  ├── css/style.css                                       │
│  ├── js/                                                 │
│  │   ├── app.js           (Main application logic)       │
│  │   ├── map.js           (Map initialization & layers)  │
│  │   ├── controls.js      (UI controls & filters)        │
│  │   └── popups.js        (Popup templates)              │
│  └── assets/                                             │
│      ├── icons/           (Category marker icons)        │
│      └── photos/          (Trip photos, post-trip)       │
│                                                          │
│  qgis/              (Desktop GIS project)                │
│  └── shanghai-trip.qgz                                   │
└──────────────────────┬──────────────────────────────────┘
                       │ git push
                       ▼
┌─────────────────────────────────────────────────────────┐
│               GITHUB PAGES (Hosting)                     │
│                                                          │
│  Static files served from /web directory                 │
│  URL: https://<user>.github.io/shanghai-trip-gis/        │
│                                                          │
│  ⚠ May be blocked/slow in mainland China (see below)    │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   END USERS                               │
│                                                          │
│  Desktop browser  ←→  Planning & analysis (pre-trip)     │
│  Mobile browser   ←→  Reference map (during trip)        │
│  Amap / Baidu     ←→  Primary navigation in China        │
└─────────────────────────────────────────────────────────┘
```

## Key Architecture Decisions

### 1. Static-Only Architecture (No Backend)

**Decision:** No server, no database. Everything is static files + GitHub Pages.

**Why:**
- Zero cost (free GitHub Pages hosting)
- No server maintenance or deployment complexity
- GeoJSON files in Git = built-in version control and collaboration
- Beginners don't need to learn backend development

**Trade-off:** No real-time collaboration (must push/pull via Git). Acceptable for a 4-person team.

### 2. GeoJSON as the Single Data Format

**Decision:** All spatial data stored as GeoJSON files in the repository.

**Why:**
- Human-readable (JSON) — beginners can edit in any text editor
- Git-friendly — diffs are meaningful, merge conflicts are resolvable
- Industry standard — works in QGIS, Leaflet, geojson.io, and every GIS tool
- No data conversion needed between tools

**Trade-off:** Large datasets can make files unwieldy. Not an issue at our scale (< 100 POIs).

### 3. Leaflet.js Over Alternatives

**Decision:** Use Leaflet.js for the web map, not MapLibre GL, Google Maps, or Mapbox.

**Why:**
- Simplest API for beginners — "Hello World" map in 10 lines of HTML
- Massive plugin ecosystem (marker clusters, routing, heatmaps)
- No API key required (with OSM tiles)
- Excellent documentation and tutorials
- Lightweight (~40KB)

**Trade-off:** No vector tiles or 3D. Not needed for this project.

### 4. OpenStreetMap Tiles with WGS84 Coordinates

**Decision:** Use free OSM-compatible tile servers (OSM Standard, CartoDB Positron/Dark Matter) with WGS84 coordinates only. Do NOT use Chinese tile providers (Gaode/Amap) in the web map.

**Why:**
- Free, no API key, no usage limits for small projects
- WGS84 coordinates (what Google Maps, geojson.io, and GPS use) align correctly with these tiles
- No coordinate conversion needed
- Multiple style options available

**See:** [China Tech Constraints](#china-tech-constraints) and [GCJ-02 Coordinate Offset](#8-gcj-02-coordinate-offset-strategy) for why we avoid Chinese tile providers.

### 5. QGIS for Desktop Analysis

**Decision:** Use QGIS (not ArcGIS or web-based tools) for spatial analysis.

**Why:**
- Free and open source — no license cost
- Industry standard — valuable skill for sustainability/tourism careers
- Full spatial analysis toolkit (buffers, distances, clustering)
- Can directly read/write GeoJSON
- Cross-platform (Windows, Mac, Linux)

### 6. One GeoJSON File Per Category with Strict Ownership

**Decision:** Split POIs into separate files by category. Each team member owns specific files and is the only person who edits them.

**Why:**
- Eliminates merge conflicts — the #1 cause of beginner Git frustration
- Maps cleanly to Leaflet layer groups (one layer per file)
- Natural ownership boundaries for team members
- Mirrors real-world data governance (you don't edit someone else's data layer)

**Ownership assignments:**

| Member | Owned Files |
|--------|-------------|
| Member A | `landmarks.geojson`, `accommodation.geojson` |
| Member B | `food.geojson`, `transport.geojson` |
| Member C | `shopping.geojson`, `cultural.geojson` |
| Member D | `nature.geojson`, `suzhou.geojson` |

If you discover a POI that belongs in someone else's file, tell the owner and they will add it. This is a feature, not a bug — it mirrors professional GIS team workflows.

### 7. GitHub for Collaboration

**Decision:** Use GitHub (not Google Drive, Notion, or shared folders) for all project files.

**Why:**
- Version control — every change is tracked with author and timestamp
- GitHub Pages — built-in free hosting for the web map
- Learning Git is a transferable professional skill
- Issues for task tracking

**Beginner accommodation:** We'll use GitHub Desktop (GUI) instead of command-line Git to lower the barrier.

### 8. GCJ-02 Coordinate Offset Strategy

**Decision:** Use WGS84 coordinates exclusively. Never use Chinese tile providers (Gaode/Amap/Baidu) in the web map. Use native Chinese map apps for actual on-the-ground navigation.

**The problem:** China mandates that all domestic map services use the GCJ-02 coordinate system, which applies a deliberate, non-linear offset of 200-400 meters to WGS84 coordinates. This means:
- Coordinates from Google Maps / geojson.io / GPS = WGS84 (correct on OSM tiles)
- Chinese map tiles (Gaode, Baidu) = GCJ-02 (shifted)
- If you display WGS84 markers on Chinese tiles, every marker will be 200-400m off — appearing in rivers, roads, or wrong buildings

**Our strategy:**
1. Store all coordinates in WGS84 (the GeoJSON standard per RFC 7946)
2. Use only WGS84-aligned tile providers in the web map (OSM, CartoDB)
3. For actual navigation in Shanghai, use Amap or Baidu Maps native apps (they handle GCJ-02 internally)
4. The custom web map is a **planning and portfolio tool**, not a primary navigation replacement in China

**Escape hatch:** If we ever need Chinese tiles in the web map, the [`gcoord`](https://github.com/hujiulong/gcoord) JavaScript library can convert WGS84 ↔ GCJ-02 on the fly. But this adds complexity we should avoid unless strictly necessary.

## China Tech Constraints

**This section is critical.** China's Great Firewall (GFW) blocks or degrades many tools this project depends on. Plan for this before the trip.

### Blocked or Unreliable in China

| Tool | Status in China | Impact | Mitigation |
|------|----------------|--------|------------|
| GitHub Pages | Intermittently blocked | Web map may not load | Prepare offline PDF maps; pre-cache via service worker before entering China |
| Google Maps | Blocked | Cannot find coordinates on the ground | Use **Amap** (高德地图) or **Baidu Maps** (百度地图) instead |
| Google services (Translate, Search) | Blocked | Cannot look things up | Use **Bing** or **Baidu** search; download offline translation packs |
| geojson.io | May be slow | Cannot create POIs visually | Do all data creation before the trip |
| Overpass Turbo | May be slow | Cannot query OSM | Download needed data before the trip |
| OpenStreetMap tiles | Slow but usually works | Map loads slowly | Service worker cache + PDF fallback |

### Required Preparation Before Entering China

1. **VPN** — Install and test a VPN before arrival (ExpressVPN, Astrill, or similar). Many VPNs are blocked; test before the trip.
2. **Offline maps** — Download Shanghai and Suzhou offline maps in **Amap** or **Organic Maps** (free, uses OSM data)
3. **Chinese map apps** — Install and set up before arrival:
   - **Amap / 高德地图** — navigation, walking directions, transit
   - **Dianping / 大众点评** — restaurant reviews (China's Yelp)
   - **WeChat / 微信** — communication (everyone in China uses it)
   - **Alipay / 支付宝** — mobile payments (set up international version)
4. **PDF maps** — Export daily itinerary maps from QGIS as PDFs (see Module 4)
5. **Service worker** — Pre-load the web map on your phone's browser while still on reliable internet (hotel WiFi with VPN)

### Recommended Workflow

- **Pre-trip (outside China):** Use Google Maps, geojson.io, GitHub, and the web map freely for planning
- **During trip (in China):** Use Amap for navigation, Dianping for food, the custom web map as reference (via VPN or service worker cache), and PDF maps as reliable fallback
- **Post-trip (outside China):** Use all tools freely for the story map

## Map Layer Architecture

```
Base Layer (pick one):
├── OpenStreetMap Standard
├── CartoDB Positron (light/minimal)  ← recommended for clean look
└── CartoDB Dark Matter (dark theme)

Overlay Layers (toggleable):
├── POI Layers (one per category)
│   ├── Landmarks (red markers)
│   ├── Food (orange markers)
│   ├── Shopping (purple markers)
│   ├── Cultural/Historical (blue markers)
│   ├── Nature/Parks (green markers)
│   ├── Transport (gray markers)
│   └── Accommodation (yellow markers)
│
├── Route Layers (one per day)
│   ├── Day 1 route (dashed line)
│   ├── Day 2 route
│   ├── ...
│   └── Day 6 route (Suzhou)
│
├── Area Layers
│   ├── District boundaries (thin outline)
│   └── Neighborhood highlights (semi-transparent fill)
│
└── Analysis Layers (generated in QGIS)
    ├── Hotel walking buffer (500m, 1km rings)
    └── POI clusters
```

## Popup Template

```
┌──────────────────────────────────────┐
│  The Bund                            │
│  外滩              [landmark] Day 1   │
│                                      │
│  Iconic waterfront promenade         │
│  with views of Pudong skyline        │
│                                      │
│  Duration: ~60 min   Cost: Free      │
│  Hours: 24/7                         │
│  ID: landmark-001                    │
│                                      │
│  [Open in Amap]                      │
└──────────────────────────────────────┘
```

The "Open in Amap" link uses the format `https://uri.amap.com/marker?position=lng,lat&name=外滩` to hand off navigation to a Chinese map app that works locally.

## Technology Versions

| Technology | Version | Notes |
|-----------|---------|-------|
| Leaflet.js | 1.9.x | Latest stable, loaded via CDN |
| QGIS | 3.36+ | LTR (Long Term Release) recommended |
| GeoJSON | RFC 7946 | Standard specification (WGS84 only) |
| GitHub Pages | -- | Served from `/web` directory |
| HTML/CSS/JS | Vanilla | No frameworks — keep it simple for beginners |

## Offline Strategy

The web map is primarily a **planning and portfolio tool**. For on-the-ground navigation in China, use native Chinese map apps (Amap, Baidu Maps). That said, we want the web map to be accessible during the trip as a reference.

### Tier 1: Service Worker (App Caching)

Cache the web app's static assets (HTML, CSS, JS, GeoJSON data files) via a service worker. This is ~200KB total and straightforward to implement. Once cached, the app shell and all POI data are available offline. The map tiles themselves will not be cached (see why below), but POI lists and popups will work.

**What works offline:** POI list, popup details, Chinese names, day filters
**What doesn't work offline:** Map tile background (gray/blank map)

### Tier 2: QGIS-Exported PDF Maps (Reliable Fallback)

Export daily itinerary maps from QGIS as print-ready PDFs. Each PDF shows one day's route with POIs labeled (English + Chinese). These work on any phone with zero internet. This is the **most reliable** offline option and should be prepared during Phase 2 (Week 4-5).

**Files:** `offline/day-1.pdf` through `offline/day-6.pdf`

### Why NOT Tile Pre-Download

Pre-downloading map tiles sounds ideal but is impractical:
- Shanghai at zoom 12-16 = ~50,000-100,000 tiles
- OpenStreetMap's Tile Usage Policy prohibits bulk downloading from their servers
- Packaging tiles into mbtiles requires tools beyond beginner scope
- Native apps (Amap, Organic Maps) already solve this problem better

### Summary

| Method | Reliability in China | Effort | Covers |
|--------|---------------------|--------|--------|
| Amap offline maps | High | Low (just download) | Full navigation |
| QGIS PDF exports | High | Medium (must create) | Daily itinerary reference |
| Service worker cache | Medium (needs initial load) | Medium (must implement) | App shell + POI data |
| VPN + GitHub Pages | Low (VPN may fail) | Low | Full web map |
