"""
Bron: OpenStreetMap via Overpass API — man_made=bridge / bridge=yes binnen
gemeente Den Haag, zoals aangegeven in de PRD.

De ruwe OSM-data bevat zeer veel kleine bruggen (voetbruggetjes over
sloten, etc). Er wordt verdicht op ~10m (afronden coördinaten) om
duplicaten/overlappende ways op dezelfde brug samen te voegen tot één punt.
"""

import common
from shapely.geometry import Point

BBOX = "52.0148,4.1850,52.1350,4.4225"
GRID_DECIMALS = 4  # ~10m verdichting

QUERY = f"""
[out:json][timeout:120];
(
  way["bridge"]({BBOX});
  way["man_made"="bridge"]({BBOX});
);
out center tags;
"""


def main():
    print("Bruggen en viaducten ophalen (Overpass API, man_made=bridge / bridge=yes)...")
    r = common.session().post(
        "https://overpass-api.de/api/interpreter", data={"data": QUERY}, timeout=150
    )
    r.raise_for_status()
    elements = r.json()["elements"]
    print(f"  {len(elements)} brug-ways gevonden in zoekgebied (voor grens- en verdichtingsfilter)")

    boundary = common.get_denhaag_boundary()
    seen_cells = set()
    features = []
    for el in elements:
        tags = el.get("tags", {})
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue
        if not boundary.contains(Point(lon, lat)):
            continue
        cell = (round(lon, GRID_DECIMALS), round(lat, GRID_DECIMALS))
        if cell in seen_cells:
            continue
        seen_cells.add(cell)
        features.append(
            common.make_point_feature(
                lon,
                lat,
                {
                    "naam": tags.get("name"),
                    "type": tags.get("bridge") or "man_made=bridge",
                    "highway": tags.get("highway"),
                },
            )
        )

    common.write_geojson(
        features,
        "bruggen",
        "© OpenStreetMap contributors (ODbL) - man_made=bridge / bridge=yes, via Overpass API",
    )


if __name__ == "__main__":
    main()
