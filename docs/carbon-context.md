# Carbon Context Comparison

```
  ┌─────────────────────────────────────────────────────────────┐
  │  PUTTING OUR TRIP'S CARBON FOOTPRINT IN CONTEXT             │
  │                                                             │
  │  Ground transport is what we can control.                   │
  │  But honest analysis requires acknowledging                 │
  │  where the real emissions are.                              │
  └─────────────────────────────────────────────────────────────┘
```

## Our Trip: Ground Transport CO2

Source: `tools/co2-calculator.py` using Shanghai-specific emission factors (see [methodology](sustainability-methodology.md)).

```
  DAY       DISTANCE    CO2         MODE MIX
  ─────────────────────────────────────────────────────
  Day 1     50.4 km     1,267g      87% metro, 13% walk
  Day 2      9.3 km       203g      75% metro, 25% walk
  Day 3      5.6 km       107g      66% metro, 34% walk
  Day 6    194.3 km     2,418g      87% train, 9% metro, 4% taxi
  ─────────────────────────────────────────────────────
  TOTAL    259.6 km     3,996g      = 4.0 kg CO2
```

## Comparison: Our Plan vs. All-Taxi

```
  ┌───────────────────────────────────────────────────────┐
  │                                                       │
  │  Our mixed-mode plan:   ██░░░░░░░░░░░░░░  4.0 kg     │
  │  Same trips, all taxi:  █████████████████  31.2 kg    │
  │                                                       │
  │  CO2 saved by choosing metro/walking/HSR:             │
  │  27.2 kg  =  87% reduction                           │
  │                                                       │
  └───────────────────────────────────────────────────────┘
```

## Comparison: Tourist vs. Local Commuter

```
  ┌───────────────────────────────────────────────────────┐
  │                                                       │
  │  Shanghai metro commuter (daily, 20km round trip):    │
  │  580g / day                                           │
  │                                                       │
  │  Our average daily ground transport:                  │
  │  999g / day                                           │
  │                                                       │
  │  Ratio: 1.7x a local commuter                        │
  │                                                       │
  │  Why higher? Tourists cover more distance per day     │
  │  than commuters, visiting dispersed POIs across       │
  │  the city rather than a single origin-destination.    │
  │  Day 6 (Suzhou, 194 km) heavily skews the average.   │
  │                                                       │
  │  Without Day 6: avg = 526g/day (0.9x a commuter)     │
  │                                                       │
  └───────────────────────────────────────────────────────┘
```

## The Elephant in the Room: Flight Emissions

```
  ┌───────────────────────────────────────────────────────┐
  │                                                       │
  │  International flight (one way, ~3,500 km):           │
  │                                                       │
  │  ██████████████████████████████████████████  250 kg   │
  │                                                       │
  │  Our ENTIRE trip ground transport:                    │
  │                                                       │
  │  █                                              4 kg  │
  │                                                       │
  │  One flight = 63x our entire trip's                   │
  │  ground transport emissions                           │
  │                                                       │
  │  Round trip flights = 500 kg                          │
  │  Ground transport   =   4 kg                          │
  │  Ratio: flights are 99.2% of total trip transport CO2 │
  │                                                       │
  └───────────────────────────────────────────────────────┘
```

## What This Means

```
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  1. GROUND TRANSPORT CHOICES MATTER AT THE MARGIN       │
  │     Choosing metro over taxi saved 27 kg — meaningful   │
  │     for local air quality and congestion, even if       │
  │     small relative to flights.                          │
  │                                                         │
  │  2. THE FLIGHT DOMINATES                                │
  │     Any honest analysis must acknowledge that the       │
  │     decision to fly internationally is the single       │
  │     largest carbon choice of the trip. Ground-level     │
  │     optimization cannot offset this.                    │
  │                                                         │
  │  3. HSR IS TRANSFORMATIVE                               │
  │     The Suzhou day trip (168 km by HSR) produced only   │
  │     1,008g CO2 — less than a single 8.4 km taxi ride   │
  │     at Shanghai rates. China's HSR network is one of    │
  │     the most carbon-efficient intercity transport       │
  │     systems in the world at 6 g/km/person.             │
  │                                                         │
  │  4. WALKABILITY IS THE BEST STRATEGY                    │
  │     Day 3 (Lujiazui) had the lowest emissions at       │
  │     107g because the Pudong skyscraper cluster is       │
  │     walkable. POI clustering = lower emissions.         │
  │     This is the core spatial planning insight.          │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

## Data Transparency

| Metric | Value | Source |
|--------|-------|--------|
| Trip ground CO2 | 4.0 kg | `tools/co2-calculator.py` output |
| Metro emission factor | 29 g/km | Sun et al. (2023); China Urban Rail Transit Association (2024) |
| HSR emission factor | 6 g/km | Lin et al. (2019); International Union of Railways (2011) |
| Taxi emission factor | 120 g/km | Avg petrol taxi, 1.5 passengers |
| Flight estimate | ~250 kg one way | ICAO (2024), economy class |
| Commuter baseline | 580 g/day | Shanghai Municipal Transportation Commission (2025) |
| Modal comparison data | — | Ritchie (2023), Our World in Data |

All emission factors and methodology details: [sustainability-methodology.md](sustainability-methodology.md)
For full reference list: [references.md](references.md)
