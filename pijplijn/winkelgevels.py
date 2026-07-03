"""
Bron: PDOK BAG WFS (verblijfsobject), zoals in de PRD: BAG-panden met
gebruiksdoel winkelfunctie.

De WFS ondersteunt geen CQL_FILTER op deze publieke laag (server negeert
het) en staat geen startIndex > 50.000 toe. Er wordt daarom een quadtree
opgebouwd over de bounding box rond Den Haag: elk vak wordt gesplitst
totdat het minder dan 40.000 treffers bevat, en pas dan gepagineerd (in
stappen van 1000, ruim onder de 50.000-grens). Resultaat wordt client-side
gefilterd op gebruiksdoel='winkelfunctie' en woonplaats="'s-Gravenhage".
Coördinaten komen in RD New (EPSG:28992) en worden met pyproj naar WGS84
omgezet. Per pand (gebouw) wordt maximaal 1 punt bewaard: meerdere
winkeleenheden in hetzelfde pand leveren dus 1 marker op.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

import common
from pyproj import Transformer
from shapely.geometry import Point

WFS_URL = "https://service.pdok.nl/lv/bag/wfs/v2_0"
TYPE_NAME = "bag:verblijfsobject"
PAGE_SIZE = 1000
MAX_HITS_PER_TILE = 40000
MAX_SPLIT_DEPTH = 6
PROPERTY_NAMES = "gebruiksdoel,woonplaats,openbare_ruimte,huisnummer,pandidentificatie"


def rd_bbox_denhaag():
    boundary = common.get_denhaag_boundary()
    lon_min, lat_min, lon_max, lat_max = boundary.bounds
    t = Transformer.from_crs("EPSG:4326", "EPSG:28992", always_xy=True)
    corners = [
        t.transform(lon_min, lat_min),
        t.transform(lon_max, lat_min),
        t.transform(lon_min, lat_max),
        t.transform(lon_max, lat_max),
    ]
    xs = [c[0] for c in corners]
    ys = [c[1] for c in corners]
    margin = 500
    return min(xs) - margin, min(ys) - margin, max(xs) + margin, max(ys) + margin


def fetch_hits(bbox):
    r = common.session().get(
        WFS_URL,
        params={
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeName": TYPE_NAME,
            "resultType": "hits",
            "bbox": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},urn:ogc:def:crs:EPSG::28992",
        },
        timeout=30,
    )
    r.raise_for_status()
    import re

    m = re.search(r'numberMatched="(\d+)"', r.text)
    return int(m.group(1))


def split_into_tiles(bbox, depth=0):
    """Quadtree: splits bbox totdat elk vak <= MAX_HITS_PER_TILE treffers heeft."""
    hits = fetch_hits(bbox)
    if hits == 0:
        return []
    if hits <= MAX_HITS_PER_TILE or depth >= MAX_SPLIT_DEPTH:
        return [(bbox, hits)]
    xmin, ymin, xmax, ymax = bbox
    xmid, ymid = (xmin + xmax) / 2, (ymin + ymax) / 2
    quadrants = [
        (xmin, ymin, xmid, ymid),
        (xmid, ymin, xmax, ymid),
        (xmin, ymid, xmid, ymax),
        (xmid, ymid, xmax, ymax),
    ]
    tiles = []
    for q in quadrants:
        tiles.extend(split_into_tiles(q, depth + 1))
    return tiles


def fetch_page(bbox, start_index):
    r = common.session().get(
        WFS_URL,
        params={
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeName": TYPE_NAME,
            "outputFormat": "application/json",
            "bbox": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},urn:ogc:def:crs:EPSG::28992",
            "count": PAGE_SIZE,
            "startIndex": start_index,
            "propertyName": PROPERTY_NAMES,
        },
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["features"]


def main():
    bbox = rd_bbox_denhaag()
    print("Winkelgevels ophalen (PDOK BAG WFS): zoekgebied opdelen (quadtree, max 40.000 treffers/vak)...")
    tiles = split_into_tiles(bbox)
    total = sum(hits for _, hits in tiles)
    page_jobs = []
    for tile_bbox, hits in tiles:
        n_pages = (hits + PAGE_SIZE - 1) // PAGE_SIZE
        for i in range(n_pages):
            page_jobs.append((tile_bbox, i * PAGE_SIZE))
    print(f"  {len(tiles)} vakken, {total} verblijfsobjecten, {len(page_jobs)} pagina's...")

    all_raw = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch_page, tb, si): (tb, si) for tb, si in page_jobs}
        done = 0
        for fut in as_completed(futures):
            all_raw.extend(fut.result())
            done += 1
            if done % 50 == 0 or done == len(page_jobs):
                print(f"  pagina {done}/{len(page_jobs)}")

    boundary = common.get_denhaag_boundary()
    seen_panden = set()
    features = []
    for feat in all_raw:
        props = feat["properties"]
        if props.get("gebruiksdoel") != "winkelfunctie":
            continue
        if props.get("woonplaats") != "'s-Gravenhage":
            continue
        pand_id = props.get("pandidentificatie")
        if pand_id in seen_panden:
            continue
        x, y = feat["geometry"]["coordinates"]
        lon, lat = common.rd_to_wgs84(x, y)
        if not boundary.contains(Point(lon, lat)):
            continue
        seen_panden.add(pand_id)
        features.append(
            common.make_point_feature(
                lon,
                lat,
                {
                    "straat": props.get("openbare_ruimte"),
                    "huisnummer": props.get("huisnummer"),
                },
            )
        )

    common.write_geojson(
        features,
        "winkelgevels",
        "PDOK BAG WFS (verblijfsobject, gebruiksdoel=winkelfunctie), Kadaster / gemeente Den Haag",
    )


if __name__ == "__main__":
    main()
