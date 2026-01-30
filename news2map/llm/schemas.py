from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, conlist, confloat


AdminLevel = Literal[
    "country",
    "state",
    "county",
    "city",
    "district",
    "neighborhood",
    "street",
    "poi",
    "unknown",
]
GeometryHint = Literal["point", "line", "polygon", "unknown"]


class SourceSpan(BaseModel):
    quote: str = Field(..., description="Short exact quote (<=200 chars)")
    start_char: Optional[int] = Field(default=None, description="Start char offset if available")
    end_char: Optional[int] = Field(default=None, description="End char offset if available")


class Place(BaseModel):
    name: str = Field(..., description="Place name as mentioned in the article")
    admin_level: AdminLevel = Field(default="unknown", description="Granularity to help geocoding")
    geometry_hint: GeometryHint = Field(default="point", description="Likely geometry type for mapping")
    context: Optional[str] = Field(default=None, description="Short context sentence")
    confidence: confloat(ge=0.0, le=1.0) = Field(default=0.7, description="Extraction confidence")
    source: Optional[SourceSpan] = None


class Event(BaseModel):
    event_type: str = Field(..., description="Label like accident, construction, housing, policy")
    title: str = Field(..., description="Short headline-like summary")
    description: Optional[str] = Field(default=None, description="One to two sentences describing what happened")
    time_text: Optional[str] = Field(default=None, description="Time expression as written")
    places: conlist(Place, min_length=1) = Field(..., description="Places tied to this event")
    confidence: confloat(ge=0.0, le=1.0) = Field(default=0.7, description="Event confidence")
    source: Optional[SourceSpan] = None


class ExtractedEvents(BaseModel):
    events: list[Event] = Field(default_factory=list)
