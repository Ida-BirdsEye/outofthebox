"""
Bron: Open Data Den Haag (opendatasoft) - dataset 'evenementendenhaag'
(exacte match met de PRD-dataset-id 'evenementendenhaag' op ckan.dataplatform.nl,
hier via het gelijknamige opendatasoft-portaal van dezelfde gemeente).

De brondataset bevat evenementenvergunningen sinds ~2008, dus met veel
herhaalde evenementen op dezelfde locatie (jaarlijkse kermis, strandfeesten,
etc). Voor de kansenkaart is een lijst van unieke evenementenlocaties nodig,
niet elk vergunningsdossier. Er wordt daarom verdicht tot 1 punt per locatie
(gegroepeerd op naam + positie, ~10m nauwkeurig), met het meest recente
evenement als representatieve naam.

Westbroekpark (De Parade) komt uit deze bron vanzelf mee als 'lokatie'
bevat 'Westbroekpark'.
"""

import common
from shapely.geometry import Point

DATASET = "evenementendenhaag"
GRID_DECIMALS = 4  # ~10m verdichting: zelfde locatie, niet zelfde vak


def main():
    print(f"Evenementenlocaties ophalen (dataset '{DATASET}')...")
    r = common.session().get(
        f"{common.OPENDATASOFT_BASE}/{DATASET}/exports/geojson",
        params={"limit": -1},
        timeout=180,
    )
    r.raise_for_status()
    raw = r.json()["features"]
    print(f"  {len(raw)} evenementendossiers opgehaald")

    boundary = common.get_denhaag_boundary()

    by_cell = {}
    for feat in raw:
        geom = feat.get("geometry")
        if not geom:
            continue
        lon, lat = geom["coordinates"]
        props = feat["properties"]
        lokatie = (props.get("lokatie") or "").strip()
        if not lokatie:
            continue
        cell = (round(lon, GRID_DECIMALS), round(lat, GRID_DECIMALS))
        datum = props.get("ingangsdatum") or ""
        bestaand = by_cell.get(cell)
        if bestaand is None or datum > bestaand["datum"]:
            by_cell[cell] = {
                "lon": lon,
                "lat": lat,
                "naam": lokatie,
                "datum": datum,
                "stadsdeel": props.get("stadsdeel"),
            }

    features = []
    for cell, info in by_cell.items():
        pt = Point(info["lon"], info["lat"])
        if not boundary.contains(pt):
            continue
        features.append(
            common.make_point_feature(
                info["lon"],
                info["lat"],
                {"naam": info["naam"], "stadsdeel": info["stadsdeel"]},
            )
        )

    heeft_westbroekpark = any("westbroekpark" in f["properties"]["naam"].lower() for f in features)
    print(f"  Westbroekpark aanwezig: {heeft_westbroekpark}")

    common.write_geojson(
        features,
        "evenementenlocaties",
        "Open Data Den Haag - Evenementen Den Haag, gemeente Den Haag "
        "(https://den-haag-opendata.opendatasoft.com/explore/dataset/evenementendenhaag/); "
        "verdicht tot unieke locaties",
    )


if __name__ == "__main__":
    main()
