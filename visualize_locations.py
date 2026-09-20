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


def visualize_locations(geoplotlib, points, point_size=2.0):
    from geoplotlib.core import BatchPainter
    from geoplotlib.layers import BaseLayer
    from geoplotlib.utils import BoundingBox

    class LocationLayer(BaseLayer):
        def invalidate(self, proj):
            self.painter = BatchPainter()
            lat, lon = coordinates(points)
            x, y = proj.lonlat_to_screen(lon, lat)
            self.painter.set_color("red")
            self.painter.points(x, y, 2 * point_size, rounded=True)

        def draw(self, proj, mouse_x, mouse_y, ui_manager):
            self.painter.batch_draw()

        def bbox(self):
            lat, lon = coordinates(points)
            return BoundingBox.from_points(lons=lon, lats=lat)

    geoplotlib.add_layer(LocationLayer())
