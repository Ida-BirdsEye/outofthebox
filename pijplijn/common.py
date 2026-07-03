"""Gedeelde hulpfuncties voor de datapijplijn: grensfilter, CRS-conversie, GeoJSON I/O."""

import json
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pyproj import Transformer
from shapely.geometry import Point, shape
from shapely.ops import transform as shapely_transform

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")

BOUNDARY_DATASET = "gemeentedenhaag"  # Open Data Den Haag (opendatasoft): Gemeentegrens Den Haag
OPENDATASOFT_BASE = "https://den-haag-opendata.opendatasoft.com/api/explore/v2.1/catalog/datasets"

_RD_TO_WGS84 = Transformer.from_crs("EPSG:28992", "EPSG:4326", always_xy=True)

USER_AGENT = "out-of-the-box-pakketpuntenviewer-pijplijn/1.0 (data-voorbereiding, eenmalig)"


def session():
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    retry = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def rd_to_wgs84(x, y):
    """Converteer een RD New (EPSG:28992) coördinaat naar WGS84 (EPSG:4326) lon/lat."""
    lon, lat = _RD_TO_WGS84.transform(x, y)
    return lon, lat


def get_denhaag_boundary():
    """Haal de gemeentegrens van Den Haag op (WGS84) en cache lokaal. Retourneert een shapely geometry."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, "grens_denhaag.geojson")
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            geom_json = json.load(f)
    else:
        r = session().get(
            f"{OPENDATASOFT_BASE}/{BOUNDARY_DATASET}/records",
            params={"limit": 1, "select": "geo_shape"},
            timeout=30,
        )
        r.raise_for_status()
        record = r.json()["results"][0]
        geom_json = record["geo_shape"]["geometry"] if "geometry" in record["geo_shape"] else record["geo_shape"]
        with open(cache_path, "w") as f:
            json.dump(geom_json, f)
    return shape(geom_json)


def filter_points_in_boundary(features, boundary):
    """Behoud alleen Point-features die binnen de Den Haag grens vallen."""
    kept = []
    for feat in features:
        geom = feat.get("geometry")
        if not geom:
            continue
        pt = Point(geom["coordinates"][0], geom["coordinates"][1]) if geom["type"] == "Point" else shape(geom).centroid
        if boundary.contains(pt):
            kept.append(feat)
    return kept


def write_geojson(features, laag_naam, bron):
    """Schrijf features weg als GeoJSON FeatureCollection in data/<laag_naam>.geojson."""
    os.makedirs(DATA_DIR, exist_ok=True)
    fc = {
        "type": "FeatureCollection",
        "name": laag_naam,
        "bron": bron,
        "features": features,
    }
    path = os.path.join(DATA_DIR, f"{laag_naam}.geojson")
    with open(path, "w") as f:
        json.dump(fc, f, ensure_ascii=False)
    print(f"  -> {path} ({len(features)} features)")
    return path


def make_point_feature(lon, lat, properties):
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": properties,
    }


def geocode_pdok(query):
    """Geocodeer een adres/plaatsnaam via de gratis PDOK Locatieserver. Retourneert (lon, lat) of None."""
    r = session().get(
        "https://api.pdok.nl/bzk/locatieserver/search/v3_1/free",
        params={"q": query, "rows": 1},
        timeout=15,
    )
    r.raise_for_status()
    docs = r.json()["response"]["docs"]
    if not docs:
        return None
    point_wkt = docs[0]["centroide_ll"]  # bv. "POINT(4.319 52.081)"
    lon, lat = point_wkt.replace("POINT(", "").replace(")", "").split()
    return float(lon), float(lat)
