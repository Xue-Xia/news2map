import logging
import time
import requests

from news2map.config import (
    NOMINATIM_BASE_URL,
    NOMINATIM_COUNTRYCODES,
    NOMINATIM_EMAIL,
    NOMINATIM_USER_AGENT,
)
from news2map.geo.types import GeoFeature

logger = logging.getLogger("news2map.geocoder")


def geocode_places(events):
    features: list[GeoFeature] = []
    for event in events:
        for place in getattr(event, "places", []):
            coords = _geocode_nominatim(place.name)
            if not coords:
                continue
            lat, lon = coords
            props = {
                "event_type": getattr(event, "event_type", None),
                "event_title": event.title,
                "event_description": event.description,
                "event_time_text": getattr(event, "time_text", None),
                "event_confidence": getattr(event, "confidence", None),
                "event_source_quote": getattr(getattr(event, "source", None), "quote", None),
                "place_name": place.name,
                "place_admin_level": getattr(place, "admin_level", None),
                "place_geometry_hint": getattr(place, "geometry_hint", None),
                "context": place.context,
                "place_confidence": getattr(place, "confidence", None),
                "place_source_quote": getattr(getattr(place, "source", None), "quote", None),
            }
            features.append(GeoFeature(place.name, lat, lon, props))
    return features


def _geocode_nominatim(query: str):
    url = f"{NOMINATIM_BASE_URL}/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    }
    if NOMINATIM_COUNTRYCODES:
        params["countrycodes"] = NOMINATIM_COUNTRYCODES
    if NOMINATIM_EMAIL:
        params["email"] = NOMINATIM_EMAIL
    headers = {"User-Agent": NOMINATIM_USER_AGENT}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return _geocode_fallbacks(query)
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        time.sleep(1)
        return lat, lon
    except Exception as exc:
        logger.warning("Geocoding failed for '%s': %s", query, exc)
        return None


def _geocode_fallbacks(query: str):
    variants = []
    if "," in query:
        parts = [p.strip() for p in query.split(",") if p.strip()]
        variants.extend(parts)
    variants.append(f"{query}, Germany")

    for q in variants:
        url = f"{NOMINATIM_BASE_URL}/search"
        params = {
            "q": q,
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
        }
        if NOMINATIM_COUNTRYCODES:
            params["countrycodes"] = NOMINATIM_COUNTRYCODES
        if NOMINATIM_EMAIL:
            params["email"] = NOMINATIM_EMAIL
        headers = {"User-Agent": NOMINATIM_USER_AGENT}
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if not data:
                continue
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            time.sleep(1)
            return lat, lon
        except Exception:
            continue
    return None
