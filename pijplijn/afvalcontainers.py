"""
Bron: Open Data Den Haag (opendatasoft) - dataset 'bakken'
(komt overeen met PRD-link 'Bakken Den Haag' op het opendatasoft-portaal).

Filter: alleen type_container_omsc = 'Ondergrondse container' (ORAC's),
t.b.v. koppeling met de ondergrondse pakketkluis.
"""

import common

DATASET = "bakken"


def main():
    print(f"Ondergrondse afvalcontainers (ORAC's) ophalen (dataset '{DATASET}')...")
    r = common.session().get(
        f"{common.OPENDATASOFT_BASE}/{DATASET}/exports/geojson",
        params={"where": "type_container_omsc='Ondergrondse container'", "limit": -1},
        timeout=120,
    )
    r.raise_for_status()
    raw = r.json()["features"]
    print(f"  {len(raw)} containers opgehaald")

    boundary = common.get_denhaag_boundary()
    features = common.filter_points_in_boundary(raw, boundary)
    features = [
        common.make_point_feature(
            f["geometry"]["coordinates"][0],
            f["geometry"]["coordinates"][1],
            {
                "afvalfractie": f["properties"].get("afvalfractie_omsc"),
                "buurt": f["properties"].get("buurt_omsc"),
                "beheerder": f["properties"].get("beheerder_omsc"),
            },
        )
        for f in features
    ]

    common.write_geojson(
        features,
        "afvalcontainers",
        "Open Data Den Haag - Bakken Den Haag, gemeente Den Haag "
        "(https://den-haag-opendata.opendatasoft.com/explore/dataset/bakken/)",
    )


if __name__ == "__main__":
    main()
