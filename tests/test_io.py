from pathlib import Path

from news2map.geo.io import write_geojson
from news2map.geo.types import GeoFeature


def test_write_geojson(tmp_path: Path):
    features = [
        GeoFeature("Berlin", 52.52, 13.405, {"event_title": "Test"}),
    ]
    out = write_geojson(features, tmp_path / "events.geojson")
    assert out.exists()
