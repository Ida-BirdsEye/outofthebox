"""
Bron: geen kant-en-klare dataset (zie PRD) - handmatig/via OpenStreetMap.

De PRD noemt expliciet Scheveningen, Kijkduin en Lange Voorhout als
boulevard-achtige locaties (voor spiegelpakketkluis en seizoensgebonden
pakketpunt). Dit zijn drie bestaande, met naam geverifieerde straten in
OpenStreetMap:
  - Strandweg      -> boulevard Scheveningen
  - Deltaplein      -> boulevard/plein Kijkduin
  - Lange Voorhout  -> laan in het centrum (expliciet genoemd bij
                        spiegelpakketkluis)

Elke straat bestaat in OSM uit veel korte way-segmenten; deze worden
verdicht tot enkele representatieve punten per straat (~100m raster) in
plaats van elk wegdeel apart te tonen.
"""

import common
from shapely.geometry import Point

BBOX = "52.0148,4.1850,52.1350,4.4225"
GRID_DECIMALS = 3  # ~100m verdichting

STRATEN = {
    "Strandweg": "boulevard Scheveningen",
    "Deltaplein": "boulevard Kijkduin",
    "Lange Voorhout": "laan, centrum",
}

QUERY = f"""
[out:json][timeout:60];
(
  {"".join(f'way["name"="{naam}"]({BBOX});' for naam in STRATEN)}
);
out center tags;
"""


def main():
    print("Boulevards ophalen (OpenStreetMap: Strandweg, Deltaplein, Lange Voorhout)...")
    r = common.session().post(
        "https://overpass-api.de/api/interpreter", data={"data": QUERY}, timeout=90
    )
    r.raise_for_status()
    elements = r.json()["elements"]
    print(f"  {len(elements)} straatsegmenten gevonden")

    boundary = common.get_denhaag_boundary()
    seen_cells = set()
    features = []
    for el in elements:
        tags = el.get("tags", {})
        naam = tags.get("name")
        categorie = STRATEN.get(naam)
        if not categorie:
            continue
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue
        if not boundary.contains(Point(lon, lat)):
            continue
        cell = (naam, round(lon, GRID_DECIMALS), round(lat, GRID_DECIMALS))
        if cell in seen_cells:
            continue
        seen_cells.add(cell)
        features.append(
            common.make_point_feature(lon, lat, {"naam": naam, "categorie": categorie})
        )

    common.write_geojson(
        features,
        "boulevards",
        "© OpenStreetMap contributors (ODbL) - handmatig geselecteerde straten "
        "(Strandweg/Scheveningen, Deltaplein/Kijkduin, Lange Voorhout), zie PRD",
    )


if __name__ == "__main__":
    main()
