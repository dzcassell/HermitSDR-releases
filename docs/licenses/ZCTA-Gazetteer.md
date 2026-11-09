# US Census ZCTA Gazetteer (ZIP code centroids)

`HermitSDR/Resources/zcta-centroids.bin` is a compact table of the
internal-point latitude and longitude of every 2020 ZIP Code Tabulation
Area (ZCTA), used by the FM DX Catalog to turn a US ZIP code into a home
location for distance filtering (`docs/FMDXScanner.md`).

- **Source**: US Census Bureau, 2024 Gazetteer Files, *ZIP Code Tabulation
  Areas* — <https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/2024_Gaz_zcta_national.zip>
  (file dated 2024-08-21, 33,791 ZCTAs).
- **Retrieved**: 2026-11-09.
- **License**: a work of the United States Government, in the public domain
  (17 U.S.C. § 105); the Census Bureau places no restriction on reuse.
- **Conversion**: `python3 -I tools/build-zcta-centroids.py <gazetteer .txt> HermitSDR/Resources/zcta-centroids.bin`
  keeps only GEOID, INTPTLAT and INTPTLONG as little-endian records
  (`uint32 zcta, int32 lat × 1e5, int32 lon × 1e5`, sorted by ZCTA, 405 KB).
  Nothing else from the Gazetteer is shipped.

A ZCTA is the Census Bureau's generalisation of a USPS ZIP code; a few
ZIP codes (PO-box-only and some unique ZIPs) have no ZCTA and are not
found. The lookup is approximate by design — the internal point of the
area, not the operator's house.
