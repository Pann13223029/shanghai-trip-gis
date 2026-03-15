# Overpass Turbo Queries for Shanghai GIS Data

A ready-to-use reference for downloading real OpenStreetMap data into your project.
Written for beginners — no prior Overpass experience needed.

---

## Table of Contents

1. [How to Use Overpass Turbo](#1-how-to-use-overpass-turbo)
2. [How to Export as GeoJSON](#2-how-to-export-as-geojson)
3. [Query Index — Which File Does Each Query Feed?](#3-query-index)
4. [Query 1 — Shanghai District Boundaries](#4-query-1--shanghai-district-boundaries)
5. [Query 2 — Metro Lines and Stations](#5-query-2--metro-lines-and-stations)
6. [Query 3 — Tourist Attractions](#6-query-3--tourist-attractions)
7. [Query 4 — Parks and Gardens](#7-query-4--parks-and-gardens)
8. [Query 5 — Shopping Areas](#8-query-5--shopping-areas)
9. [Shanghai Bounding Box Reference](#9-shanghai-bounding-box-reference)
10. [Tips and Troubleshooting](#10-tips-and-troubleshooting)

---

## 1. How to Use Overpass Turbo

Overpass Turbo is a free web tool that lets you search OpenStreetMap's database
using a query language called Overpass QL. Think of it as "Google for map data."

Website: https://overpass-turbo.eu/

### Interface Overview (ASCII diagram)

```
+------------------------------------------------------------------+
|  overpass turbo                              [Run] [Share] [Help]|
+------------------------------------------------------------------+
|  +---------------------------+  +------------------------------+ |
|  |                           |  |                              | |
|  |   QUERY EDITOR            |  |   MAP PREVIEW                | |
|  |   (left panel)            |  |   (right panel)              | |
|  |                           |  |                              | |
|  |  Type or paste your       |  |  Results appear here as      | |
|  |  Overpass QL query here   |  |  highlighted points/lines/   | |
|  |                           |  |  polygons on the map         | |
|  |                           |  |                              | |
|  +---------------------------+  +------------------------------+ |
|                                                                  |
|  [Export]  [Wizard]  [Save]  [Load]  [Settings]                  |
+------------------------------------------------------------------+
```

### Step-by-Step: Running Your First Query

```
Step 1: Open https://overpass-turbo.eu/ in your browser
        (Use Chrome or Firefox for best results)

Step 2: Clear the editor
        Click anywhere in the left panel
        Select All (Ctrl+A or Cmd+A) and Delete

Step 3: Paste your query
        Copy a query from this document and paste it into the editor

Step 4: Click [Run]  <-- the blue button at the top right of the editor

Step 5: Wait for results
        A progress bar appears at the top of the map
        Large queries may take 10-30 seconds — be patient!

Step 6: Inspect results
        Blue dots   = nodes (individual points)
        Blue lines  = ways (roads, rail lines, building edges)
        Pink areas  = relations (districts, metro lines as networks)
        Click any feature to see its tags/attributes

Step 7: Export as GeoJSON
        See Section 2 below
```

### Understanding Overpass QL (the query language)

Overpass QL looks intimidating at first but has a simple pattern:

```
[out:json][timeout:30];      <-- output format and max wait time
(
  node["key"="value"](bbox); <-- find NODES with this tag in this area
  way["key"="value"](bbox);  <-- find WAYS with this tag in this area
  relation["key"="value"](bbox); <-- find RELATIONS with this tag
);
out body;                    <-- output the main features
>;                           <-- also fetch child nodes (needed for shapes)
out skel qt;                 <-- output the geometry
```

**Key vocabulary:**
- `node` — a single point (e.g., a bus stop, a shop)
- `way` — a line or polygon made of connected nodes (e.g., a road, a park outline)
- `relation` — a group of nodes/ways forming a complex feature (e.g., a metro line with many segments, a district boundary)
- `bbox` — bounding box: the rectangular area to search within, written as `(south,west,north,east)`
- `tag` — a key=value label on a feature, like `"railway"="subway"` or `"tourism"="attraction"`

---

## 2. How to Export as GeoJSON

After running any query and seeing results on the map, follow these steps:

```
+-- After clicking [Run] and seeing results on the map --+

Step 1: Click [Export]  <-- in the toolbar above the query editor

         +------------------------------------------+
         |  Export                                   |
         |                                          |
         |  Data                                    |
         |    [GeoJSON]  <-- CLICK THIS              |
         |    [GPX]                                  |
         |    [KML]                                  |
         |    [raw OSM data]                         |
         |                                          |
         |  Map                                     |
         |    [Image]                               |
         |    [SVG]                                 |
         +------------------------------------------+

Step 2: Click [GeoJSON]
        Your browser will download a file called "export.geojson"

Step 3: Rename the file
        Rename it to match the project file it belongs to, e.g.:
        - export.geojson  ->  districts.geojson
        - export.geojson  ->  metro.geojson

Step 4: Move the file into your project
        Copy the renamed file into the correct data/ subfolder:

        data/
        ├── areas/
        │   └── districts.geojson    <-- district boundary queries go here
        ├── poi/
        │   ├── landmarks.geojson    <-- tourist attractions go here
        │   ├── nature.geojson       <-- parks and gardens go here
        │   └── shopping.geojson     <-- shopping areas go here
        └── routes/
            └── metro.geojson        <-- metro query goes here

Step 5: Open in QGIS or geojson.io to verify
        Drag and drop the file onto the QGIS canvas, or
        go to https://geojson.io and paste the file contents
```

**Important note about large exports:**
If Overpass Turbo warns "The result is very large — do you want to continue?",
click Yes for district/metro queries. For POI queries, this warning means you
may want to add more filters to reduce the result size first.

---

## 3. Query Index

This table shows which query feeds which project file:

```
Query                  -> Project File                     -> Layer in Web Map
---------------------     --------------------------------    ------------------
Query 1: Districts     -> data/areas/districts.geojson     -> District Boundaries
Query 2: Metro         -> data/routes/metro.geojson        -> Metro Lines & Stations
Query 3: Attractions   -> data/poi/landmarks.geojson       -> Tourist Attractions
Query 4: Parks         -> data/poi/nature.geojson          -> Parks & Gardens
Query 5: Shopping      -> data/poi/shopping.geojson        -> Shopping Areas
```

You can use the downloaded data to:
- Replace the existing hand-drawn/placeholder GeoJSON files with real OSM data
- Compare OSM data against your team's manually added features
- Run spatial analysis in QGIS (e.g., which attractions are near a metro station?)

---

## 4. Query 1 — Shanghai District Boundaries

### What this query does

Shanghai is divided into 16 administrative districts (区, qū). This query
fetches the boundary polygon for each district from OpenStreetMap. Each polygon
has attributes like the district name in English and Chinese.

These polygons are the foundation of your GIS project — they let you:
- Clip other data to a specific district
- Color-code the city by district
- Count how many POIs fall within each district

### The Query

Paste this entire block into Overpass Turbo:

```
/*
  Shanghai District Boundaries
  Fetches all admin_level=6 boundaries within Shanghai municipality.
  admin_level=6 = district level in China's OSM conventions.
  Shanghai municipality itself is admin_level=4.
*/

[out:json][timeout:60];

// First find Shanghai municipality to use as search area
area["name:en"="Shanghai"]["admin_level"="4"]->.shanghai;

// Find all district-level boundaries within that area
(
  relation["boundary"="administrative"]["admin_level"="6"](area.shanghai);
);

out body;
>;
out skel qt;
```

### What the results look like

```
Expected result: ~16 polygon features
Each feature has tags such as:
  name        = "浦东新区"
  name:en     = "Pudong"
  admin_level = "6"
  boundary    = "administrative"

Districts you should see:
  Huangpu (黄浦)     Xuhui (徐汇)      Changning (长宁)
  Jing'an (静安)     Putuo (普陀)      Hongkou (虹口)
  Yangpu (杨浦)      Minhang (闵行)    Baoshan (宝山)
  Jiading (嘉定)     Pudong (浦东新区)  Jinshan (金山)
  Songjiang (松江)   Qingpu (青浦)     Fengxian (奉贤)
  Chongming (崇明)
```

### Export filename
Save as: `data/areas/districts.geojson`

### Troubleshooting
- If you see 0 results: try changing `"admin_level"="6"` to `"admin_level"="5"`
  as OSM tagging conventions sometimes differ
- If the query times out: increase `[timeout:60]` to `[timeout:120]`

---

## 5. Query 2 — Metro Lines and Stations

### What this query does

Shanghai has one of the world's largest metro networks — 20 lines and over
500 stations. This query fetches:
- All subway/metro lines as line geometries (ways and relations)
- All individual metro stations as points (nodes)

The result lets you visualize which neighborhoods have good metro access,
calculate walking distances from your hotel to the nearest station, and
plan multi-day itineraries around transit.

### The Query

```
/*
  Shanghai Metro Lines and Stations
  Fetches subway lines (as route relations) and all station points.
  Bounding box covers the full Shanghai municipality area.
  (south, west, north, east) = (30.7, 120.8, 31.5, 121.9)
*/

[out:json][timeout:90];
(
  // Metro/subway route relations (the full lines)
  relation["route"="subway"](30.7,120.8,31.5,121.9);

  // Individual station nodes
  node["station"="subway"](30.7,120.8,31.5,121.9);
  node["railway"="subway_entrance"](30.7,120.8,31.5,121.9);

  // Metro tracks (the physical rail ways)
  way["railway"="subway"](30.7,120.8,31.5,121.9);
);

out body;
>;
out skel qt;
```

### What the results look like

```
Expected result:
  ~20 route relations  (one per metro line)
  ~500+ station nodes
  Hundreds of track segments (ways)

Example tags on a station node:
  name        = "人民广场"
  name:en     = "People's Square"
  railway     = "station"
  station     = "subway"
  line        = "1;2;8"     (served by Lines 1, 2, and 8)

Example tags on a route relation:
  name        = "上海地铁1号线"
  name:en     = "Shanghai Metro Line 1"
  route       = "subway"
  ref         = "1"
  colour      = "#c0392b"   (line color in hex)
```

### Tip: Query just one line

To fetch only Line 1 (useful for testing):

```
[out:json][timeout:30];
(
  relation["route"="subway"]["ref"="1"](30.7,120.8,31.5,121.9);
);
out body;
>;
out skel qt;
```

Change `"ref"="1"` to `"ref"="2"`, `"ref"="11"`, etc. for other lines.

### Export filename
Save as: `data/routes/metro.geojson`

### Note on file size
The full metro query may produce a 3-5 MB GeoJSON file. This is normal.
If your web map loads slowly, consider keeping only the station nodes
(removing the track ways) for the interactive map, and using the full
file only in QGIS for analysis.

---

## 6. Query 3 — Tourist Attractions

### What this query does

This query finds places tagged `tourism=attraction` in OSM — the sites that
tourists specifically come to Shanghai to visit. Examples include The Bund,
Yu Garden, the Shanghai Tower observation deck, and the French Concession area.

These points feed your `landmarks.geojson` layer — the "must-see" pins on
your trip map.

### The Query

```
/*
  Shanghai Tourist Attractions
  Fetches all OSM features tagged tourism=attraction or tourism=museum
  or tourism=viewpoint within Shanghai's bounding box.
  Also includes historic sites (historic=yes) and monuments.
*/

[out:json][timeout:45];
(
  // Tourism attractions (the primary tag for sights)
  node["tourism"="attraction"](30.7,120.8,31.5,121.9);
  way["tourism"="attraction"](30.7,120.8,31.5,121.9);
  relation["tourism"="attraction"](30.7,120.8,31.5,121.9);

  // Museums
  node["tourism"="museum"](30.7,120.8,31.5,121.9);
  way["tourism"="museum"](30.7,120.8,31.5,121.9);

  // Viewpoints (rooftop bars, observation decks, scenic overlooks)
  node["tourism"="viewpoint"](30.7,120.8,31.5,121.9);

  // Historic sites
  node["historic"="monument"](30.7,120.8,31.5,121.9);
  way["historic"="monument"](30.7,120.8,31.5,121.9);
  node["historic"="memorial"](30.7,120.8,31.5,121.9);
);

out body;
>;
out skel qt;
```

### What the results look like

```
Expected result: 100-300 features

Example features you should see:
  "The Bund" (外滩)              tourism=attraction
  "Yu Garden" (豫园)             tourism=attraction
  "Shanghai Museum" (上海博物馆)  tourism=museum
  "Oriental Pearl Tower" (东方明珠) tourism=attraction
  "Shanghai Tower" (上海中心大厦)   tourism=attraction
  "Jade Buddha Temple" (玉佛寺)   tourism=attraction / amenity=place_of_worship

Example tags on a feature:
  name        = "外滩"
  name:en     = "The Bund"
  tourism     = "attraction"
  description = "Historic waterfront promenade"
  website     = "https://..."
```

### Narrowing to the tourist core (optional)

If you want only the Puxi/downtown area (smaller bounding box):

```
[out:json][timeout:30];
(
  node["tourism"="attraction"](31.18,121.43,31.25,121.52);
  way["tourism"="attraction"](31.18,121.43,31.25,121.52);
);
out body;
>;
out skel qt;
```

This smaller box covers the Huangpu / Jing'an / Xuhui core — the main
tourist triangle most groups visit on Day 1-2.

### Export filename
Save as: `data/poi/landmarks.geojson`

---

## 7. Query 4 — Parks and Gardens

### What this query does

Green spaces are important for a sustainable tourism lens (SDG 11) and
for practical trip planning — parks are good rest spots between activities.
This query finds:
- Public parks (`leisure=park`)
- Botanical gardens and themed gardens (`leisure=garden`)
- Nature reserves and green areas (`landuse=green` / `landuse=recreation_ground`)

### The Query

```
/*
  Shanghai Parks and Gardens
  Fetches all major green spaces: parks, gardens, and recreation areas.
  Parks in Shanghai range from tiny neighborhood gardens to large
  nature areas like Gongqing Forest Park.
*/

[out:json][timeout:45];
(
  // Public parks (most common tag)
  node["leisure"="park"](30.7,120.8,31.5,121.9);
  way["leisure"="park"](30.7,120.8,31.5,121.9);
  relation["leisure"="park"](30.7,120.8,31.5,121.9);

  // Gardens (botanical, scenic, formal)
  node["leisure"="garden"](30.7,120.8,31.5,121.9);
  way["leisure"="garden"](30.7,120.8,31.5,121.9);
  relation["leisure"="garden"](30.7,120.8,31.5,121.9);

  // Nature reserves
  way["leisure"="nature_reserve"](30.7,120.8,31.5,121.9);
  relation["leisure"="nature_reserve"](30.7,120.8,31.5,121.9);
);

out body;
>;
out skel qt;
```

### What the results look like

```
Expected result: 200-500 features (Shanghai has many small neighborhood parks)

Notable parks you should see:
  Fuxing Park (复兴公园)             — French Concession rose garden
  Century Park (世纪公园)            — Pudong's largest park, 140 ha
  People's Square (人民广场)         — central plaza with gardens
  Zhongshan Park (中山公园)          — historic park in Changning
  Gongqing Forest Park (共青森林公园) — large nature area in Yangpu
  Zhujiajiao (朱家角)               — water town with garden areas
  Chenshan Botanical Garden          — large botanic garden in Songjiang

Example tags:
  name        = "复兴公园"
  name:en     = "Fuxing Park"
  leisure     = "park"
  access      = "yes"
  opening_hours = "06:00-18:00"
```

### Filtering to larger parks only (optional)

The full query returns hundreds of tiny neighborhood pocket parks.
To focus on named parks only, add a filter:

```
[out:json][timeout:45];
(
  way["leisure"="park"]["name"](30.7,120.8,31.5,121.9);
  relation["leisure"="park"]["name"](30.7,120.8,31.5,121.9);
);
out body;
>;
out skel qt;
```

Adding `["name"]` means "only return features that have a name tag" —
this removes the many unnamed green patches while keeping real parks.

### Export filename
Save as: `data/poi/nature.geojson`

---

## 8. Query 5 — Shopping Areas

### What this query does

Shanghai is famous for its shopping scene — from ultra-luxury malls in
Lujiazui to vintage street markets in the French Concession. This query
fetches:
- Major shopping malls (`shop=mall`)
- Shopping streets and pedestrian zones (`highway=pedestrian` combined with retail)
- Department stores (`shop=department_store`)
- Markets (`amenity=marketplace`)

### The Query

```
/*
  Shanghai Shopping Areas
  Fetches shopping malls, department stores, markets, and
  major pedestrian shopping streets.
*/

[out:json][timeout:45];
(
  // Shopping malls
  node["shop"="mall"](30.7,120.8,31.5,121.9);
  way["shop"="mall"](30.7,120.8,31.5,121.9);
  relation["shop"="mall"](30.7,120.8,31.5,121.9);

  // Department stores (e.g., Isetan, Parkson, Times Square)
  node["shop"="department_store"](30.7,120.8,31.5,121.9);
  way["shop"="department_store"](30.7,120.8,31.5,121.9);

  // Markets and bazaars (e.g., Yuyuan Bazaar, Dongtai Road Antique Market)
  node["amenity"="marketplace"](30.7,120.8,31.5,121.9);
  way["amenity"="marketplace"](30.7,120.8,31.5,121.9);

  // Pedestrian shopping streets (e.g., Nanjing Road East pedestrian section)
  way["highway"="pedestrian"]["name"](30.7,120.8,31.5,121.9);
);

out body;
>;
out skel qt;
```

### What the results look like

```
Expected result: 50-150 features

Notable shopping destinations you should see:
  Nanjing Road (南京路步行街)         — world's busiest shopping street
  IFC Mall (上海国金中心)             — luxury mall in Lujiazui
  Plaza 66 (恒隆广场)                 — high-end mall on Nanjing West
  K11 Art Mall                        — art-themed mall in Huangpu
  Xintiandi Style (新天地时尚)         — boutique mall in the French Concession
  Tianzifang (田子坊)                 — arts/crafts market in Xuhui
  Yuyuan Bazaar (豫园商城)            — traditional market near the Old City

Example tags on a mall:
  name        = "上海国金中心商场"
  name:en     = "IFC Mall Shanghai"
  shop        = "mall"
  opening_hours = "Mo-Su 10:00-22:00"
  website     = "https://..."
  addr:street = "陆家嘴环路"
```

### Query for Nanjing Road specifically (optional)

To fetch just the famous Nanjing Road pedestrian zone as a line:

```
[out:json][timeout:25];
(
  way["highway"="pedestrian"]["name"="南京路步行街"](31.22,121.45,31.24,121.49);
  way["highway"="pedestrian"]["name:en"="Nanjing Road Pedestrian Street"](31.22,121.45,31.24,121.49);
);
out body;
>;
out skel qt;
```

### Export filename
Save as: `data/poi/shopping.geojson`

---

## 9. Shanghai Bounding Box Reference

All queries in this document use a bounding box that covers the full Shanghai
municipality. Overpass Turbo expects bounding boxes in this order:

```
(south, west, north, east)
  |       |      |      |
  |       |      |      +-- rightmost longitude
  |       |      +--------- topmost latitude
  |       +---------------- leftmost longitude
  +------------------------ bottommost latitude
```

### Full Shanghai Municipality

```
(30.7, 120.8, 31.5, 121.9)

         121.9°E (east)
              |
  31.5°N -----+----------+  <- north
  (north)     |          |
              | SHANGHAI  |
              |  ~6,340   |
              | sq km     |
  30.7°N -----+----------+  <- south
  (south)     |
         120.8°W (west)
```

### Smaller Bounding Boxes for Specific Areas

```
Area                   BBox (S, W, N, E)              Use case
---------------------  ----------------------------   --------------------
Downtown Puxi core     31.18, 121.43, 31.25, 121.52   Day 1-2 tourist area
Pudong / Lujiazui      31.21, 121.48, 31.25, 121.54   Day 3 Pudong area
French Concession      31.20, 121.43, 31.22, 121.47   Day 2 exploration
Suzhou (day trip)      31.28, 120.53, 31.35, 120.65   Day 6 Suzhou trip
```

Using a smaller bounding box makes queries faster and returns fewer results —
useful when you know exactly which neighborhood you are working on.

---

## 10. Tips and Troubleshooting

### Query is slow or times out

```
Problem:  Query runs for more than 60 seconds and fails
Solution: 1. Increase timeout: change [timeout:30] to [timeout:120]
          2. Use a smaller bounding box (see section 9)
          3. Split the query — run nodes and ways separately
```

### "Too many features" warning

```
Problem:  Overpass Turbo warns about a very large result set
Solution: 1. Add a ["name"] filter to exclude unnamed minor features
          2. Use a smaller bounding box
          3. Click Yes anyway — it will still export correctly,
             it just loads slowly in the browser preview
```

### Results look wrong on the map

```
Problem:  Features appear in the wrong place, or outside Shanghai
Possible causes:
  - Bounding box coordinates are in wrong order
    WRONG: (121.9, 31.5, 120.8, 30.7)  <- longitude first
    RIGHT: (30.7, 120.8, 31.5, 121.9)  <- latitude first (S,W,N,E)

  - Coordinates are swapped (lat/lon reversed)
    Latitude  = the number around 30-31  (north-south)
    Longitude = the number around 120-122 (east-west)
```

### GeoJSON file has no geometry

```
Problem:  You export GeoJSON but polygons/lines have no shape data
Solution: Make sure your query ends with ALL THREE of these lines:
          out body;
          >;
          out skel qt;

          The middle ">" line tells Overpass to also download the
          nodes that make up the outline of each way/relation.
          Without it, polygons export as empty geometry.
```

### Checking data quality before using in QGIS

Before replacing your existing GeoJSON files with OSM data:

```
1. Open https://geojson.io
2. Drag your downloaded .geojson file onto the page
3. Verify features appear in the correct locations on the map
4. Click a few features and check the properties panel
5. If names are missing or features are misplaced, the OSM data
   in that area may be incomplete — keep your hand-drawn data instead
```

### Combining OSM data with your hand-drawn data

You do not have to choose one or the other. In QGIS you can load both layers
at the same time and use them together:

```
OSM districts layer  +  Your custom neighborhood annotations
       |                           |
       +------ QGIS project -------+
                     |
              merged analysis
              (e.g., which custom POIs fall in Pudong?)
```

---

*Queries tested against Overpass API v0.7 | OSM data copyright OpenStreetMap contributors (ODbL)*
*For OSM tagging conventions used in China: https://wiki.openstreetmap.org/wiki/China*
