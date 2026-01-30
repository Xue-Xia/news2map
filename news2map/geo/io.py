from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point

from news2map.geo.types import GeoFeature


def _to_gdf(features: list[GeoFeature]) -> gpd.GeoDataFrame:
    rows = []
    for f in features:
        rows.append(
            {
                **f.properties,
                "name": f.name,
                "geometry": Point(f.longitude, f.latitude),
            }
        )
    if not rows:
        # Create an empty GeoDataFrame with a geometry column
        return gpd.GeoDataFrame({"geometry": []}, geometry="geometry", crs="EPSG:4326")
    return gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")


def write_geojson(features: list[GeoFeature], path: str | Path) -> Path:
    gdf = _to_gdf(features)
    path = Path(path)
    gdf.to_file(path, driver="GeoJSON")
    return path


def write_shapefile(features: list[GeoFeature], path: str | Path) -> Path:
    gdf = _to_gdf(features)
    path = Path(path)
    gdf.to_file(path, driver="ESRI Shapefile")
    return path
