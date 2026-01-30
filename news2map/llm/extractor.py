import os

from openai import OpenAI

from news2map.config import LLM_MODEL, OPENAI_API_KEY
from news2map.llm.schemas import ExtractedEvents, Event


def extract_events(text: str) -> list[Event]:
    if not _can_use_openai():
        return []

    client = OpenAI()
    system_msg = (
        "You are a geoparsing assistant. Extract events and places from the article. "
        "Return structured data matching the provided schema. Each event needs: "
        "event_type, title, description (1-2 sentences if possible), time_text if present, "
        "places (at least one), and confidence. Each place should include name, admin_level, "
        "geometry_hint, optional context, confidence, and optional source quote. "
        "Keep place names exactly as mentioned. German articles are common."
    )

    result = client.beta.chat.completions.parse(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": text},
        ],
        response_format=ExtractedEvents,
    )

    parsed = result.choices[0].message.parsed
    return parsed.events if parsed else []


def _can_use_openai() -> bool:
    return bool(OPENAI_API_KEY or os.getenv("OPENAI_API_KEY"))
