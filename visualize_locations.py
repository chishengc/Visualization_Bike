import json
from pathlib import Path

import numpy as np


def load_geojson_points(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        geojson = json.load(handle)

    points = []
    for feature in geojson.get("features", []):
        geometry = feature.get("geometry") or {}
        if geometry.get("type") != "Point":
            continue

        lon, lat = geometry["coordinates"]
        properties = feature.get("properties") or {}
        points.append({
            "lat": float(lat),
            "lon": float(lon),
            "name": properties.get("NAME", "Bike station"),
            "bikes": float(properties.get("NUM_BIKES_AVAILABLE", 0) or 0),
        })

    if not points:
        raise ValueError(f"No Point features found in {path}")

    return points


def coordinates(points):
    return (
        np.asarray([point["lat"] for point in points], dtype=float),
        np.asarray([point["lon"] for point in points], dtype=float),
    )


def visualize_locations(geoplotlib, points, point_size=4.0):
    from geoplotlib.utils import DataAccessObject

    station_data = DataAccessObject({
        "lat": [point["lat"] for point in points],
        "lon": [point["lon"] for point in points],
        "name": [point["name"] for point in points],
        "bikes": [point["bikes"] for point in points],
    })
    geoplotlib.dot(station_data, color="red", point_size=point_size)
