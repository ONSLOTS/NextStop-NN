"""Schemas for pydantic validation."""

import pydantic


class UserInput(pydantic.BaseModel):
    """Pydantic model of the user input."""

    prompt: str = pydantic.Field(..., max_length=200)
    time_for_walk: int
    latitude: float = pydantic.Field(..., ge=-90, le=90)
    longitude: float = pydantic.Field(..., ge=-180, le=180)
