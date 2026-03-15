# Roadmap

```
  ┌─────────────────────────────────────────────────────────┐
  │                    PROJECT TIMELINE                      │
  │                                                         │
  │  Week 1-2  ████████░░░░░░░░  Phase 0: Setup             │
  │  Week 3-4  ░░░░████████░░░░  Phase 1: Data Collection   │
  │  Week 4-5  ░░░░░░████████░░  Phase 2: Analysis & PDFs   │
  │  Week 5-7  ░░░░░░░░████████  Phase 3: Web Map           │
  │  Week 7-8  ░░░░░░░░░░░░████  Phase 4: Polish            │
  │  Trip      ░░░░░░░░░░░░░░██  Phase 5: Live Use          │
  │  After     ░░░░░░░░░░░░░░░█  Phase 6: Story Map         │
  │                                                         │
  │  Team: Person 1 (Lead)  +  Person 2 (Data/Sustainability)│
  └─────────────────────────────────────────────────────────┘
```

Total timeline: ~8 weeks before trip, plus during/after trip phases.

---

## Phase 0 -- Setup & GIS Foundations (Week 1-2)

**Goal:** Both people have tools installed, understand GIS basics, and can add a POI.

| Task | Owner | Deliverable |
|------|-------|-------------|
| Install QGIS + GitHub Desktop on both laptops | Both | Working installations |
| GitHub repo setup (already done) | Person 1 | Repo with validation workflow |
| Assign primary file responsibility | Both | Clear who curates which files |
| Practice push workflow: each person creates 1 test POI | Both | 2 test POIs pushed successfully |
| Set up shared QGIS project with base map + all layers | Person 1 | `qgis/shanghai-trip.qgz` |
| Complete Learning Module 1 (What is GIS?) | Both | Pair discussion |
| Complete Learning Module 2 (Coordinates & Projections) | Both | Can explain lat/lng and GCJ-02 |
| Decide on accommodation location | Both | Hotel POI added as anchor point |

**Milestone:** Both people can create a GeoJSON point and push it to GitHub.

---

## Phase 1 -- Data Collection (Week 3-4)

**Goal:** Build out the full POI dataset for Shanghai and Suzhou.

```
  Person 1 (Lead)                    Person 2
  researches & adds:                 researches & adds:
  ┌──────────────────────┐           ┌──────────────────────┐
  │  landmarks.geojson   │           │  cultural.geojson    │
  │  food.geojson        │           │  shopping.geojson    │
  │  transport.geojson   │           │  nature.geojson      │
  │  accommodation       │           │  suzhou.geojson      │
  └──────────────────────┘           └──────────────────────┘
  Target: 15-20 POIs                 Target: 15-20 POIs
```

| Task | Owner | Deliverable |
|------|-------|-------------|
| Add POIs to landmarks, food, transport, accommodation | Person 1 | 15-20 POIs with full properties |
| Add POIs to cultural, shopping, nature, suzhou | Person 2 | 15-20 POIs with full properties |
| Download Shanghai district boundaries (Overpass Turbo) | Person 1 | `data/areas/districts.geojson` |
| Download Shanghai metro lines (Overpass Turbo) | Person 1 | `data/routes/metro.geojson` |
| Complete Learning Module 3 (GeoJSON & Spatial Data) | Both | Can read and write GeoJSON |
| Load all data into QGIS, verify on map | Person 2 | All layers visible and correct |

**Closing checkpoint:** Both people review ALL POIs together — verify coordinates, Chinese names, and categories.

**Milestone:** 30-40 POIs across all categories, viewable in QGIS. All GeoJSON passes validation.

---

## Phase 2 -- Itinerary Planning & Analysis (Week 4-5)

**Goal:** Organize POIs into daily itineraries, optimize routes, create offline PDFs, run sustainability analysis.

| Task | Owner | Deliverable |
|------|-------|-------------|
| Assign POIs to trip days (Day 1-6) | Both (sprint session) | `day` field populated on all POIs |
| Create walking routes for each day in QGIS | Person 1 | `data/routes/day-{1-6}.geojson` |
| Calculate daily walking distances | Person 1 | Distance summary table |
| Buffer analysis — what's walkable from hotel? | Person 1 | Buffer layer in QGIS |
| **Sustainability analysis: transport mode audit** | **Person 2** | Mode mix per day, CO2 estimates |
| Create QGIS print layout template | Person 1 | Reusable template with title/legend/scale |
| Export daily PDF maps using template | Person 2 | `offline/day-1.pdf` through `day-6.pdf` |
| Plan Suzhou day trip with explicit time blocks | Both | Suzhou schedule with transit times |
| Complete Learning Module 4 (Spatial Analysis & Print Maps) | Both | Understands buffers, distances, print layouts |

```
  Suzhou Day Trip Planning Sprint:
  ┌─────────────────────────────────────────────────────┐
  │  Must include explicit time blocks:                 │
  │                                                     │
  │  08:00  Depart hotel → metro to Hongqiao            │
  │  09:00  Train to Suzhou                             │
  │  09:30  Arrive Suzhou → taxi to first garden        │
  │  10:00  POI 1: Humble Administrator's Garden        │
  │  11:30  Walk to POI 2: Suzhou Museum                │
  │  13:00  Lunch near Pingjiang Road                   │
  │  14:00  POI 3: Pingjiang Road Historic District     │
  │  15:30  Return to Suzhou Station                    │
  │  16:30  Train back to Shanghai                      │
  │  17:30  Arrive hotel                                │
  │                                                     │
  │  Maximum 3-4 POIs. Don't over-plan!                 │
  └─────────────────────────────────────────────────────┘
```

**Milestone:** Complete day-by-day itinerary backed by spatial analysis. Offline PDF maps ready. Sustainability analysis documented.

---

## Phase 3 -- Web Map Development (Week 5-7)

**Goal:** Build the interactive Leaflet.js web map and deploy it.

```
  Person 1 (Lead) builds:           Person 2 reviews:
  ┌──────────────────────┐           ┌──────────────────────┐
  │  Load all POI layers │           │  Test on mobile      │
  │  Add layer controls  │           │  Check Chinese names │
  │  Add day filter      │           │  Verify popups       │
  │  Add route lines     │           │  Check Amap links    │
  │  Mobile responsive   │           │  Review colors/style │
  │  Deploy to GitHub    │           │  Make 1+ modification│
  └──────────────────────┘           └──────────────────────┘
```

| Task | Owner | Deliverable |
|------|-------|-------------|
| Complete Module 5a: both explore the starter template | Both | Understand how the web map works |
| Load all POI categories as separate layers | Person 1 | All categories visible and clickable |
| Add day-by-day route lines | Person 1 | Route lines with day selector |
| Add layer toggle controls (by category, by day) | Person 1 | Working filter UI |
| Add Chinese labels in popups + "Open in Amap" link | Person 1 | Bilingual popups with navigation handoff |
| Mobile-responsive layout and touch controls | Person 1 | Works on phone screens |
| Style and polish (colors, fonts, legend) | Person 2 | Portfolio-quality appearance |
| Person 2 makes at least one hands-on code modification | Person 2 | e.g., change a color, modify popup layout |
| Deploy to GitHub Pages | Person 1 | Live URL accessible |
| Complete Module 5b (Building Features & Deploying) | Both | Understands layers, controls, deployment |

**Milestone:** Live, mobile-friendly web map deployed.

---

## Phase 4 -- Pre-Trip Polish (Week 7-8)

**Goal:** Final QA, offline prep, China-readiness.

| Task | Owner | Deliverable |
|------|-------|-------------|
| Test web map on both phones | Both | Bug list resolved |
| Verify offline PDF maps are readable on phones | Both | PDFs accessible without internet |
| Install China apps: Amap, Dianping, WeChat, Alipay | Both | Apps set up and tested |
| Test VPN access (if available) | Both | VPN confirmed working |
| Download Shanghai + Suzhou offline maps in Amap | Both | Offline navigation ready |
| Print pocket card with hotel address in Chinese | Both | Physical backup |
| Pair review: critique the web map design together | Both | 3+ improvements identified and applied |
| Final itinerary review — is every day realistic? | Both | Approved itinerary |
| Complete Learning Module 6 (Cartographic Design) | Both | Can critique and improve map design |

**Milestone:** Trip-ready. Multiple offline fallbacks prepared. China apps installed.

---

## Phase 5 -- During Trip (Trip Week)

**Goal:** Use the map, collect real-world data.

| Task | Owner | Deliverable |
|------|-------|-------------|
| Use **Amap** for primary navigation | Both | -- |
| Use web map (via VPN or cache) as reference | Both | -- |
| Use PDF maps as offline fallback | Both | -- |
| Take geotagged photos at POIs | Both | Photos folder |
| Record GPS traces (phone app) | Person 2 | GPX files |
| Jot trip notes per location | Both | Notes in shared doc |
| Note actual transport modes used per leg | Person 2 | For post-trip sustainability comparison |

---

## Phase 6 -- Post-Trip Story Map (Week after trip)

**Goal:** Transform the trip into a portfolio-quality story map.

```
  Person 1 handles:                  Person 2 handles:
  ┌──────────────────────┐           ┌──────────────────────┐
  │  Photo upload &      │           │  Day-by-day          │
  │  geotagging          │           │  narrative writing    │
  │                      │           │                      │
  │  GPS trace layers    │           │  Sustainability      │
  │  (actual vs planned) │           │  reflection          │
  │                      │           │  (SDG 11/12)         │
  │  Deployment &        │           │                      │
  │  final polish        │           │  GIS methodology     │
  │                      │           │  reflection          │
  └──────────────────────┘           └──────────────────────┘
```

| Task | Owner | Deliverable |
|------|-------|-------------|
| Upload and geotag trip photos | Person 1 | Photos linked to POIs |
| Add trip notes/journal entries to POIs | Both | Enriched GeoJSON |
| Add GPS traces as actual-route layers | Person 1 | Actual vs. planned comparison |
| Write day-by-day story map narrative | Person 2 | Story map content |
| Write sustainability reflection (SDG 11/12) | Person 2 | Sustainability section |
| Write GIS methodology reflection | Person 1 | Technical reflection |
| Final cartographic polish | Both | Screenshot exports |
| Complete Module 7 (Story Map) | Both | Narrative cartography skills |

**Milestone:** Completed portfolio piece showcasing GIS skills and sustainable tourism analysis.
