from pydantic import BaseModel, Field, field_validator


class PlacePayload(BaseModel):
    id: int
    title: str
    description: str
    score: float | None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @field_validator('title')
    def title_not_empty(cls, v: str) -> str:
        if len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        return v.strip()

    @field_validator('description')
    def description_not_empty(cls, v: str) -> str:
        if len(v.strip()) == 0:
            raise ValueError('Description cannot be empty')
        return v.strip()
