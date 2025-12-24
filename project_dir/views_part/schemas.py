from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import declared_attr

from project_dir.authorization import hash_password


class BaseReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AuthorCreate(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    age: int = Field(ge=6, le=130)


class AuthorSchema(BaseReturn, AuthorCreate):
    pass


class MovieCreate(BaseModel):
    title: str
    year_of_issue: int
    description: str | None = None
    genre: str
    author_id: int


class MovieSchema(BaseReturn, MovieCreate):
    pass


class UserCreate(BaseModel):
    visible_name: str
    username: str
    password: str




class UserSchema(BaseReturn):
    visible_name: str


