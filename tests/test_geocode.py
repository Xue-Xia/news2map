from news2map.geo.geocoder import geocode_places
from news2map.llm.schemas import Event, Place


def test_geocode_places_monkeypatch(monkeypatch):
    def fake_geocode(query: str):
        return (52.52, 13.405)

    monkeypatch.setattr("news2map.geo.geocoder._geocode_nominatim", fake_geocode)

    events = [
        Event(
            event_type="test",
            title="Test",
            description="Desc",
            places=[Place(name="Berlin")],
        )
    ]
    features = geocode_places(events)
    assert len(features) == 1
    assert features[0].name == "Berlin"
