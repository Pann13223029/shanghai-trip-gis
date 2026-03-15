# Sustainability Assessment Methodology

## Scope

This assessment evaluates the environmental and social sustainability dimensions of a 6-day urban tourism itinerary in Shanghai and Suzhou, China. The analysis uses Geographic Information Systems (GIS) to spatially assess three sustainability dimensions: **transport carbon emissions**, **transit accessibility**, and **heritage preservation impact**.

### What is measured
- Transport-related CO2 emissions across the trip itinerary, computed per route segment, per day, and as a trip total
- Transit accessibility of selected points of interest, measured as proximity to metro stations
- Heritage preservation approaches at cultural POIs, assessed through a structured scorecard

### What is NOT measured (known limitations)
- **International flight emissions** — by far the largest carbon component of any overseas trip, but outside the scope of this ground-transport assessment. We acknowledge this in our carbon context comparison.
- **Accommodation energy use** — hotel energy data is not publicly available at the property level in Shanghai
- **Food-related emissions** — life-cycle analysis of restaurant meals is beyond project scope
- **Waste generation** — no reliable per-tourist waste data available
- **Water consumption** — not measurable at this scale

We explicitly scope to ground transport and land-use decisions because these are the dimensions where tourist behavior has agency and where spatial analysis provides actionable insight.

## Frameworks Referenced

### SDG Indicators

| SDG Target | Indicator | How We Measure |
|-----------|-----------|---------------|
| **11.2** — Affordable and sustainable transport | Proportion of population with convenient access to public transport | % of itinerary POIs within 800m of a metro station |
| **11.4** — Protect cultural and natural heritage | Expenditure on preservation of cultural and natural heritage | Qualitative assessment of heritage preservation approaches at cultural POIs |
| **12.b** — Develop tools to monitor sustainable tourism | Monitoring tools for sustainable development impacts | This GIS methodology itself — demonstrating how spatial analysis supports sustainable tourism assessment |

### GSTC Criteria (Global Sustainable Tourism Council)
We reference GSTC-D (Destination) criteria where applicable:
- **D6** — Visitor management and destination planning (tourism concentration analysis)
- **D7** — Transport and climate change (CO2 calculations)
- **D10** — Cultural heritage protection (adaptive reuse assessment)

## Emission Factors

### Shanghai-Specific Transport Emissions

All emission factors are per person per kilometer unless noted.

| Mode | CO2 (g/km/person) | Source |
|------|-------------------|--------|
| Walking | 0 | — |
| Cycling / shared bike | 0 | — |
| Shanghai Metro | 29 | Shanghai Shentong Metro Group Annual Report 2024; national urban rail average from China Urban Rail Transit Association |
| City bus | 65 | Shanghai Bus Company fleet data; based on 30% electric bus penetration as of 2024 |
| Taxi (petrol) | 120 | Based on average Shanghai taxi fuel economy (8.5L/100km), 2.3kg CO2/L petrol, average 1.5 passengers |
| E-taxi / ride-hail (EV) | 45 | Based on Shanghai grid emission factor (0.42 kg CO2/kWh) × average EV consumption (15 kWh/100km), 1.5 passengers |
| Maglev (airport) | 95 | Shanghai Maglev high energy consumption offset by high speed; per NDRC rail energy data |
| High-speed rail (HSR) | 6 | China State Railway Group published figures; Shanghai-Suzhou G-series trains |

**Note on taxis:** Shanghai's ride-hail fleet (Didi) is transitioning to EVs. As of 2025, approximately 40% of active ride-hail vehicles in Shanghai are electric. Our calculations use the petrol taxi figure (120 g/km) as conservative default, with EV taxi (45 g/km) noted where the team specifically used an EV.

### Contextual Comparisons

| Scenario | CO2 per person |
|----------|---------------|
| Average Shanghai metro commuter (daily round trip, 20km) | ~580g/day |
| Same itinerary by taxi only (estimated) | Computed per-day |
| Same itinerary by our mixed-mode plan | Computed per-day |
| International flight (e.g., Bangkok-Shanghai, one way) | ~250 kg |

The flight comparison is included to provide honest context: a single international flight likely exceeds the entire trip's ground transport emissions by 50-100x. We include this not to excuse ground-level choices but to frame where the highest-impact decisions actually lie.

## Sustainability Scorecard

Each POI where sustainability is relevant receives a structured assessment across 5 dimensions. POIs where sustainability is not meaningfully applicable (e.g., metro stations, airports) receive `null` scores.

### Scoring Criteria

| Dimension | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| **Transit access** | >1.5km from any metro station | 800m-1.5km | 400-800m | <400m from metro |
| **Heritage value** | No heritage significance | Local heritage interest | City/provincial heritage listing | National or UNESCO heritage |
| **Community impact** | Negative (displacement, commodification) | Mixed (some benefit, some harm) | Neutral | Positive (supports local livelihoods, preserves community function) |
| **Walkability** | Car-dependent location | Some pedestrian access but car-oriented | Pedestrian-friendly area | Fully pedestrian zone or park |
| **Environmental sensitivity** | High-impact tourism area with no mitigation | Moderate impact with some management | Low-impact with active management | Minimal footprint / contributes to ecological value |

**Sustainability score** = sum of applicable dimensions (0-15 maximum). Dimensions scored `null` where not applicable are excluded from the denominator.

### Application Guidelines
- Score only dimensions where you have evidence or can observe
- Use `null` for dimensions you cannot assess rather than guessing
- Document your reasoning in the `sustainability_notes` field
- Acknowledge subjectivity — this is a structured assessment, not a precise measurement

## Analytical Methods

### Transit Accessibility Analysis (QGIS)
1. Create 800m buffers around all metro stations in the Shanghai metro GeoJSON
2. Spatial join: determine which trip POIs fall within an 800m buffer
3. Compute: % of POIs within walking distance of transit
4. Visualize: map showing POIs colored by transit accessibility
5. Reference: SDG indicator 11.2.1 measures 500m for bus and 1000m for rail; we use 800m as a practical walking threshold

### Tourism Concentration Analysis (QGIS)
1. Spatial join: assign each POI to its Shanghai district (using district boundary polygons)
2. Count POIs per district
3. Visualize: choropleth map showing POI density by district
4. Analysis: identify over-concentrated districts and assess whether the itinerary distributes visits or concentrates them

### Carbon Footprint Computation
1. For each route segment: `CO2 = distance_km × emission_factor_per_km`
2. Aggregate per day and per trip
3. Compare: mixed-mode plan vs. hypothetical all-taxi plan
4. Context: compare trip total to flight emissions and daily commuter baseline

## Limitations and Honest Assessment

1. **Emission factors are estimates.** Real-world emissions vary with occupancy, time of day, vehicle age, and driving conditions. Our figures represent reasonable averages, not precise measurements.

2. **The scorecard is subjective.** Two assessors may score the same POI differently. We mitigate this by documenting reasoning and using a structured rubric, but do not claim objectivity.

3. **We assess a planned itinerary, not actual behavior.** Post-trip, we compare planned vs. actual transport modes to measure the gap between intention and action.

4. **Heritage impact assessment requires local expertise we may lack.** As visiting tourists, our understanding of community impact at sites like Tianzifang or Xintiandi is necessarily surface-level. We note where our assessment may be incomplete.

5. **This is a case study, not a generalizable assessment.** Our findings apply to this specific itinerary. Different POI selections would produce different sustainability profiles.
