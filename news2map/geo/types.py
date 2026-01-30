from dataclasses import dataclass


@dataclass
class GeoFeature:
    name: str
    latitude: float
    longitude: float
    properties: dict
