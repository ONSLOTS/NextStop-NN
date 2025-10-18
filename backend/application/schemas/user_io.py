"""Schemas for pydantic validation."""

import pydantic

import models.place_payload


class UserInput(pydantic.BaseModel):
    """Pydantic model of the user input."""

    prompt: str = pydantic.Field(..., max_length=200)
    time_for_walk: int = pydantic.Field(..., le=24, ge=1)
    latitude: float = pydantic.Field(..., ge=-90, le=90)
    longitude: float = pydantic.Field(..., ge=-180, le=180)

class UserOutput(pydantic.BaseModel):
    """Pydantic model of the user output."""

    walking_time: int | None
    walking_path: list[models.place_payload.PlacePayload] = (
        pydantic.Field(..., min_length=1),
        )
    explanation: list[str] = pydantic.Field(...)