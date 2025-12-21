from pydantic import BaseModel, Field, ConfigDict


class BaseReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    age: int = Field(ge=6, le=130)


class AuthorSchema(BaseReturn, AuthorCreate):
    id: int


class MovieCreate(BaseModel):
    title: str
    year_of_issue: int
    description: str | None = None
    genre: str
    author_id: int


class MovieSchema(BaseReturn, MovieCreate):
    id: int
