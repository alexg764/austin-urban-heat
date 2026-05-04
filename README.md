
# Urban Heat Island Risk — Downtown Austin
### Heat Severity Index derived from Landsat 9 LST and NDVI

![Urban Heat Island Risk Map](https://github.com/alexg764/austin-urban-heat/raw/main/outputs/urbanheatrisk_austin.png)

---

## Overview

This project develops a **GIS-based Urban Heat Risk Model** for downtown Austin, TX, identifying areas most vulnerable to urban heat island effects based on land surface temperature and vegetation deficits. The output is a spatially prioritized **Heat Severity Index** designed to inform urban planning and green infrastructure decisions.

---

## Methodology

### Data Sources
- **Landsat 9 Multispectral Imagery** — USGS EarthExplorer (Band 10 for thermal, Bands 4/5 for NDVI)
- **City of Austin Open Data Portal** — Land use boundaries, building footprints
- **OpenStreetMap** — Road network and tree canopy data
- Digital elevation and contextual basemap layers for visualization

### Processing Steps

**1. Land Surface Temperature (LST)**
Land Surface Temperature was derived from the Landsat 9 Level-2 thermal product: `ST_B10`, which contains atmospherically corrected surface temperature values.

A Python workflow using `rasterio` and `numpy` was developed to convert raw thermal band values into Celsius temperatures.

USGS scaling factors for Landsat Collection 2 Level-2 products were applied:
`LST(K) = ST_B10 * 0.00341802 + 149.0`

Kelvin values were then converted to Celsius:
`LST(C) = LST(K) - 273.15`

The thermal raster was processed using `rasterio` and `numpy`, generating a resulting raster which represents the estimated land surface temperature values across downtown Austin.

**2. NDVI (Normalized Difference Vegetation Index)**
Normalized Difference Vegetation Index (NDVI) was calculated using spectral bands:
* Band 5 - Near Infrared (NIR)
* Band 4 - Red

NDVI Formula used:
`NDVI = (NIR - RED) / (NIR + RED)`

Higher NDVI values indicate denser vegetation; Lower NDVI values indicate sparse vegetation. Using a little bit of Python magic, the resulting NDVI raster highlighted vegetation density and canopy distribution throughout the study area.

**3. Heat Severity Index**
High-risk zones were identified by overlaying LST and NDVI layers to isolate areas with high surface temperatures and low vegetation cover.  I utilized QGIS to then get mean values from these high-risk zones.

To create a basic heat severity index, I weighed the normalized LST with the inverse NDVI values, then weighed area against that output. Each high-risk zone was then scored using a weighted index formula:

| Component | Weight |
|---|---|
| Mean LST & NDVI score within zone | 30% |
| Area of the high-risk zone | 70% |

The full formula is as follows:
`HSI = ((0.6 * mean_LST) + (0.4 * mean_NDVI))`
and, for the final index that includes area as a weighted factor:
`WHSI = (HSI * 0.3) + (((area - min_area)/(max_area - min_area)) * 0.7)`

The resulting index ranges from **0 to 1**, where higher scores indicate greater heat risk and prioritization need for green infrastructure intervention.

Resulting hotspot rasters were polygonized into vector layers to support:
-   Urban planning analysis
-   Green infrastructure prioritization
-   Spatial suitability assessment

---

## Tools Used

| Tool | Purpose |
|---|---|
| Python (rasterio, numpy) | Raster processing, band math, index calculation |
| QGIS | Spatial analysis, geoprocessing, cartographic output |
| Landsat 9 | Source multispectral imagery |
| OpenStreetMap | Road and canopy reference data |

---

## Outputs

- `outputs/urban_heat_map.pdf` — Full-resolution print layout
- `outputs/urban_heat_map.png` — Web-optimized map image

---

## Data Sources & Credits

- USGS Landsat 9 imagery via [EarthExplorer](https://earthexplorer.usgs.gov/)
- City of Austin Open Data Portal — Land Use & Buildings
- © OpenStreetMap contributors
- Map data © 2015 Google (basemap)

---

*Produced by Enrique Gonzalez, 2026. This is a personal GIS project I had a lot of fun doing.*
