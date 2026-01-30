from news2map.llm.extractor import extract_events


def test_extract_events_requires_key():
    events = extract_events("Berlin ist schön.")
    assert isinstance(events, list)
