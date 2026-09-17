import argparse
import csv
from pathlib import Path

import numpy as np


def load_trips(csv_path, sample_every):
    start_lat = []
    start_lon = []
    graph_start_lat = []
    graph_start_lon = []
    graph_end_lat = []
    graph_end_lon = []
    member_type = []

    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {
            "start_lat",
            "start_lng",
            "end_lat",
            "end_lng",
            "member_casual",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

        for row_number, row in enumerate(reader):
            try:
                current_start_lat = float(row["start_lat"])
                current_start_lon = float(row["start_lng"])
                current_end_lat = float(row["end_lat"])
                current_end_lon = float(row["end_lng"])
            except (TypeError, ValueError):
                continue

            start_lat.append(current_start_lat)
            start_lon.append(current_start_lon)
            member_type.append(row["member_casual"])
            if row_number % sample_every == 0:
                graph_start_lat.append(current_start_lat)
                graph_start_lon.append(current_start_lon)
                graph_end_lat.append(current_end_lat)
                graph_end_lon.append(current_end_lon)

    return {
        "lat": np.asarray(start_lat),
        "lon": np.asarray(start_lon),
        "src_lat": np.asarray(graph_start_lat),
        "src_lon": np.asarray(graph_start_lon),
        "dest_lat": np.asarray(graph_end_lat),
        "dest_lon": np.asarray(graph_end_lon),
        "member_casual": np.asarray(member_type),
    }


def main():
    parser = argparse.ArgumentParser(description="Visualize CABI bike trips with geoplotlib")
    parser.add_argument("csv_path", nargs="?", type=Path, default=Path("cabi_bike.csv"))
    parser.add_argument("--sample-every", type=int, default=100)
    parser.add_argument("--save", type=Path, help="Save a PNG instead of opening the map window")
    args = parser.parse_args()

    if args.sample_every < 1:
        parser.error("--sample-every must be at least 1")
    if not args.csv_path.exists():
        parser.error(f"CSV file not found: {args.csv_path}")

    import pyglet
    pyglet.options["debug_gl"] = False
    import geoplotlib
    from geoplotlib.utils import DataAccessObject

    loaded = load_trips(args.csv_path, args.sample_every)
    density_data = DataAccessObject({
        "lat": loaded["lat"],
        "lon": loaded["lon"],
        "member_casual": loaded["member_casual"],
    })
    route_data = DataAccessObject({
        "src_lat": loaded["src_lat"],
        "src_lon": loaded["src_lon"],
        "dest_lat": loaded["dest_lat"],
        "dest_lon": loaded["dest_lon"],
    })

    geoplotlib.set_window_size(1280, 850)
    geoplotlib.tiles_provider({
        "url": lambda zoom, xtile, ytile: (
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Street_Map/MapServer/tile/%d/%d/%d" % (zoom, ytile, xtile)
        ),
        "tiles_dir": "esri_world_street_map",
        "attribution": (
            "made with geoplotlib | Tiles &copy; Esri, HERE, Garmin, "
            "(c) OpenStreetMap contributors, and the GIS user community"
        ),
    })
    geoplotlib.hist(
        density_data,
        cmap="hot",
        binsize=8,
        alpha=210,
        show_colorbar=True,
    )
    geoplotlib.graph(
        route_data,
        "src_lat",
        "src_lon",
        "dest_lat",
        "dest_lon",
        linewidth=1,
        alpha=70,
        color="winter",
    )

    if args.save:
        output_path = args.save.with_suffix("") if args.save.suffix.lower() == ".png" else args.save
        geoplotlib.savefig(str(output_path))
        print(f"Saved {output_path}.png")
    else:
        geoplotlib.show()


if __name__ == "__main__":
    main()