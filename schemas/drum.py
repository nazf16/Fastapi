from pydantic import BaseModel, validator
from pydantic import BaseModel, validator


class Drum(BaseModel):
    title: str
    description: str


@validator("title")
def title_mustbe_min_3_characters(cls, v):
    if len(v) < 3:
        raise ValueError("title must be at least 3 characters")
    return v


class DrumResponseModel(Drum):
    id: int

    class config():
        orm_mode = True
