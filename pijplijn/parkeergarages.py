"""
Bron: OpenStreetMap via Overpass API.
De PRD noemt de 'Parkeergarages'-dataset op dataplatform.nl, aangevuld met
RDW Open Parkeerdata. dataplatform.nl was tijdens het bouwen van deze
pijplijn niet bereikbaar, en de parkeergarages-dataset op het
opendatasoft-portaal van dezelfde gemeente bleek leeg (0 records). Daarom
wordt hier, net als bij de bruggenlaag, OpenStreetMap gebruikt: node/way
met amenity=parking en parking=multi-storey of underground.

Alleen objecten met een naam-tag worden meegenomen: naamloze kleine
(inpandige) garages zijn doorgaans besloten garages bij
kantoren/woongebouwen en geen bruikbare pakketgarage-locatie.
"""

import common
from shapely.geometry import Point

BBOX = "52.0148,4.1850,52.1350,4.4225"  # ruim rond Den Haag; exacte grensfilter volgt client-side

QUERY = f"""
[out:json][timeout:90];
(
  node["amenity"="parking"]["parking"~"multi-storey|underground"]({BBOX});
  way["amenity"="parking"]["parking"~"multi-storey|underground"]({BBOX});
);
out center tags;
"""


def main():
    print("Parkeergarages ophalen (Overpass API, amenity=parking multi-storey/underground)...")
    r = common.session().post(
        "https://overpass-api.de/api/interpreter", data={"data": QUERY}, timeout=120
    )
    r.raise_for_status()
    elements = r.json()["elements"]
    print(f"  {len(elements)} garages gevonden in zoekgebied (voor grens- en naamfilter)")

    boundary = common.get_denhaag_boundary()
    features = []
    for el in elements:
        tags = el.get("tags", {})
        naam = tags.get("name")
        if not naam:
            continue
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue
        if not boundary.contains(Point(lon, lat)):
            continue
        features.append(
            common.make_point_feature(
                lon,
                lat,
                {
                    "naam": naam,
                    "type": tags.get("parking"),
                    "capaciteit": tags.get("capacity"),
                },
            )
        )

    common.write_geojson(
        features,
        "parkeergarages",
        "© OpenStreetMap contributors (ODbL) - amenity=parking, via Overpass API",
    )


if __name__ == "__main__":
    main()
