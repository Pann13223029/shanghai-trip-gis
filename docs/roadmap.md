# Roadmap

Total timeline: ~8 weeks before trip, plus during/after trip phases.

## Phase 0 -- Setup & GIS Foundations (Week 1-2)

**Goal:** Everyone has tools installed, understands GIS basics, and can add a POI.

| Task | Owner | Deliverable |
|------|-------|-------------|
| Install QGIS on all laptops | Everyone | Working QGIS installation |
| Install GitHub Desktop on all laptops | Everyone | Working GitHub Desktop |
| GitHub repo setup + invite all members | Lead | Repo with `.gitignore` and validation workflow |
| Assign file ownership (2 category files per member) | Lead | Ownership table in contribution guide |
| Practice the push workflow: each member creates 1 test POI | Everyone | 4 test POIs pushed without conflicts |
| Complete Learning Module 1 (What is GIS?) | Everyone | Quiz/discussion |
| Complete Learning Module 2 (Coordinates & Projections) | Everyone | Can explain lat/lng and GCJ-02 |
| Decide on accommodation location | Everyone | Hotel POI added as anchor point |

**Milestone:** Every member can create a GeoJSON point and push it to their own file without conflicts.

---

## Phase 1 -- Data Collection (Week 3-4)

**Goal:** Build out the full POI dataset for Shanghai and Suzhou.

| Task | Owner | Deliverable |
|------|-------|-------------|
| Research & add Landmark + Accommodation POIs (10-15) | Member A (file owner) | `data/poi/landmarks.geojson`, `accommodation.geojson` |
| Research & add Food + Transport POIs (10-15) | Member B (file owner) | `data/poi/food.geojson`, `transport.geojson` |
| Research & add Shopping + Culture POIs (10-15) | Member C (file owner) | `data/poi/shopping.geojson`, `cultural.geojson` |
| Research & add Nature + Suzhou POIs (10-15) | Member D (file owner) | `data/poi/nature.geojson`, `suzhou.geojson` |
| Download Shanghai district boundaries (OSM) | Analyst | `data/areas/districts.geojson` |
| Download Shanghai metro lines (OSM) | Analyst | `data/routes/metro.geojson` |
| Complete Learning Module 3 (GeoJSON & Data) | Everyone | Can read and write GeoJSON |
| Load all data into QGIS, verify on map | Cartographer | QGIS project file with all layers |

**Milestone:** 50+ POIs across all categories, viewable in QGIS. All GeoJSON passes validation.

---

## Phase 2 -- Itinerary Planning & Analysis (Week 4-5)

**Goal:** Organize POIs into daily itineraries, optimize routes, create offline PDF maps.

| Task | Owner (Rotating) | Deliverable |
|------|-------------------|-------------|
| Assign POIs to trip days (Day 1-6) | Everyone | `day` field populated on all POIs |
| Create walking routes for each day in QGIS | Cartographer | `data/routes/day-{1-6}.geojson` |
| Calculate daily walking distances | Analyst | Distance summary table |
| Buffer analysis -- what's walkable from hotel? | Analyst | Buffer layer in QGIS |
| Cluster check -- are same-day POIs geographically grouped? | Analyst | Cluster visualization in QGIS |
| Review and rebalance itinerary based on analysis | Everyone | Final day assignments |
| **Plan Suzhou day trip with time blocks** | Everyone | Suzhou schedule with transit times |
| **Export daily PDF maps from QGIS** (Module 4) | Cartographer | `offline/day-1.pdf` through `day-6.pdf` |
| Complete Learning Module 4 (Spatial Analysis & Print Maps) | Everyone | Understands buffers, distances, QGIS print layout |

**Suzhou day trip planning must include:**
- Explicit transit time blocks (hotel -> Hongqiao: 30-60 min, train: 25 min, Suzhou station -> first garden: 20-30 min)
- Maximum 3-4 Suzhou POIs (after subtracting ~3 hours round-trip transit)
- POIs clustered geographically (don't zigzag across Suzhou)

**Milestone:** Complete day-by-day itinerary backed by spatial analysis. Offline PDF maps ready.

---

## Phase 3 -- Web Map Development (Week 5-7)

**Goal:** Build the interactive Leaflet.js web map and deploy it.

| Task | Owner (Rotating) | Deliverable |
|------|-------------------|-------------|
| Complete Module 5a: understand and customize the starter template | Everyone | Each member modifies at least one aspect |
| Load all POI categories as separate layers | Web Dev | All categories visible and clickable |
| Add day-by-day route lines | Web Dev | Route lines with day selector |
| Add layer toggle controls (by category, by day) | Web Dev | Working filter UI |
| Add Chinese labels in popups + "Open in Amap" link | Web Dev | Bilingual popups with navigation handoff |
| Mobile-responsive layout and touch controls | Web Dev | Works on phone screens |
| Style and polish (colors, fonts, legend) | Cartographer | Portfolio-quality appearance |
| Deploy to GitHub Pages | Web Dev | Live URL accessible |
| Complete Module 5b (Building Features & Deploying) | Everyone | Understands layers, controls, deployment |

**Milestone:** Live, mobile-friendly web map at `https://<username>.github.io/shanghai-trip-gis/`

---

## Phase 4 -- Pre-Trip Polish (Week 7-8)

**Goal:** Final QA, offline prep, China-readiness.

| Task | Owner | Deliverable |
|------|-------|-------------|
| Test web map on all members' phones | Everyone | Bug list resolved |
| Verify offline PDF maps are readable on phones | Everyone | PDFs accessible without internet |
| Install China apps: Amap, Dianping, WeChat, Alipay | Everyone | Apps set up and tested |
| Test VPN access (if available) | Everyone | VPN confirmed working |
| Download Shanghai + Suzhou offline maps in Amap | Everyone | Offline navigation ready |
| Pre-load web map via service worker on phones | Everyone | App shell cached |
| Print pocket card with hotel address in Chinese | Everyone | Physical backup |
| Final itinerary review -- is every day realistic? | Everyone | Approved itinerary |
| Complete Learning Module 6 (Cartographic Design) | Everyone | Can critique and improve map design |

**Milestone:** Trip-ready. Multiple offline fallbacks prepared. China apps installed.

---

## Phase 5 -- During Trip (Trip Week)

**Goal:** Use the map, collect real-world data.

| Task | Owner | Deliverable |
|------|-------|-------------|
| Use **Amap** for primary navigation in Shanghai/Suzhou | Everyone | -- |
| Use web map (via VPN or service worker cache) as reference | Everyone | -- |
| Use PDF maps as offline fallback | Everyone | -- |
| Take geotagged photos at POIs | Everyone | Photos folder |
| Record GPS traces (phone app, e.g., Strava or OsmAnd) | 1 volunteer | GPX files |
| Jot trip notes per location | Everyone | Notes in shared doc |
| Note any POIs discovered on-the-ground | Everyone | New POIs to add later |

---

## Phase 6 -- Post-Trip Story Map (Week after trip)

**Goal:** Transform the trip into a portfolio-quality story map.

| Task | Owner (Rotating) | Deliverable |
|------|-------------------|-------------|
| Upload and geotag trip photos | Data Collector | Photos linked to POIs |
| Add trip notes/journal entries to POIs | Everyone | Enriched GeoJSON |
| Add GPS traces as actual-route layers | Analyst | Actual vs. planned comparison |
| Populate story map template with day-by-day content | Web Dev | Story map page |
| Final cartographic polish for portfolio | Cartographer | Screenshot exports |
| Write project reflection/README | Everyone | Updated README |
| Complete Learning Module 7 (Story Map) | Everyone | Understands narrative cartography |

**Milestone:** Completed portfolio piece showcasing GIS skills applied to real-world travel.

---

## Summary Timeline

```
Week 1-2  ████████░░░░░░░░  Phase 0: Setup & Foundations
Week 3-4  ░░░░████████░░░░  Phase 1: Data Collection
Week 4-5  ░░░░░░████████░░  Phase 2: Itinerary, Analysis & PDFs
Week 5-7  ░░░░░░░░████████  Phase 3: Web Map
Week 7-8  ░░░░░░░░░░░░████  Phase 4: Polish & China Prep
Trip      ░░░░░░░░░░░░░░██  Phase 5: Live Use (Amap + web map)
Post-trip ░░░░░░░░░░░░░░░█  Phase 6: Story Map
```
