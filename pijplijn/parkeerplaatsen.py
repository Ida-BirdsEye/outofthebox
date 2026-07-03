"""
Bron: Open Data Den Haag (opendatasoft) - dataset 'parkeerplekken'.
NB: het CKAN-portaal ckan.dataplatform.nl uit de PRD-tabel was tijdens het
bouwen van deze pijplijn niet bereikbaar (TCP-timeout). Open Data Den Haag
(den-haag-opendata.opendatasoft.com) is het officiele opendataportaal van
dezelfde gemeente en publiceert dezelfde brondata, inclusief deze dataset.

Filter: alleen type_parkeerplek = 'Parkeergelegenheid' (gewoon openbaar
parkeren; sluit gehandicaptenplekken, laad/losplekken, in/uitritten,
parkeerverboden e.d. uit).

De brondata is per parkeervak een polygoon (vakomtrek). Voor de kaart wordt
dit teruggebracht tot het middelpunt (centroid). Omdat er ruim 40.000
individuele parkeervakken zijn, wat te dicht is voor een overzichtelijke
kansenkaart, wordt er verdicht tot circa 1 punt per ~100m (afronden op 3
decimalen) zodat de kaart straten/blokken met parkeergelegenheid toont in
plaats van elk individueel vak.
"""

import common
from shapely.geometry import shape

DATASET = "parkeerplekken"
GRID_DECIMALS = 3  # ~100m verdichting


def main():
    print(f"Parkeerplaatsen ophalen (dataset '{DATASET}')...")
    r = common.session().get(
        f"{common.OPENDATASOFT_BASE}/{DATASET}/exports/geojson",
        params={"where": "type_parkeerplek='Parkeergelegenheid'", "limit": -1},
        timeout=180,
    )
    r.raise_for_status()
    raw = r.json()["features"]
    print(f"  {len(raw)} parkeervakken opgehaald")

    boundary = common.get_denhaag_boundary()
    seen_cells = set()
    features = []
    for feat in raw:
        centroid = shape(feat["geometry"]).centroid
        lon, lat = centroid.x, centroid.y
        if not boundary.contains(centroid):
            continue
        cell = (round(lon, GRID_DECIMALS), round(lat, GRID_DECIMALS))
        if cell in seen_cells:
            continue
        seen_cells.add(cell)
        props = feat["properties"]
        features.append(
            common.make_point_feature(
                lon,
                lat,
                {
                    "type_parkeerplek": props.get("type_parkeerplek"),
                    "capaciteit": props.get("capaciteit"),
                    "orientatie": props.get("orientatie"),
                },
            )
        )

    common.write_geojson(
        features,
        "parkeerplaatsen",
        "Open Data Den Haag - Parkeerplekken Den Haag, gemeente Den Haag "
        "(https://den-haag-opendata.opendatasoft.com/explore/dataset/parkeerplekken/)",
    )


if __name__ == "__main__":
    main()
