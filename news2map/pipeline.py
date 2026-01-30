from pathlib import Path

from news2map.config import OUTPUT_DIR
from news2map.geo.geocoder import geocode_places
from news2map.geo.io import write_geojson, write_shapefile
from news2map.llm.extractor import extract_events


def run_pipeline(text: str, output_dir: str | None = None):
    output_root = Path(output_dir or OUTPUT_DIR)
    output_root.mkdir(parents=True, exist_ok=True)

    events = extract_events(text)
    features = geocode_places(events)

    geojson_path = write_geojson(features, output_root / "events.geojson")
    shp_path = write_shapefile(features, output_root / "events.shp")

    return PipelineResult(
        events=events,
        features=features,
        geojson_path=str(geojson_path),
        shapefile_path=str(shp_path),
    )


class PipelineResult:
    def __init__(self, events, features, geojson_path, shapefile_path):
        self.events = events
        self.features = features
        self.geojson_path = geojson_path
        self.shapefile_path = shapefile_path
