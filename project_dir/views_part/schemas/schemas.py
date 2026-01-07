from pydantic import BaseModel, Field, ConfigDict, EmailStr


class BaseReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AuthorPatch(BaseModel):
    name: str | None = None
    age: int | None = None


class AuthorCreate(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    age: int = Field(ge=6, le=130)


class AuthorSchema(BaseReturn, AuthorCreate):
    pass


class MoviePatch(BaseModel):
    title: str | None
    year_of_issue: int | None
    description: str | None = None
    genre: str | None


class MovieCreate(BaseModel):
    title: str
    year_of_issue: int
    description: str | None = None
    genre: str
    author_id: int


class MovieSchema(BaseReturn, MovieCreate):
    pass


class SeriesPatch(BaseModel):
    title: str | None = None
    episodes: int | None = None
    seasons: int | None = None
    description: str | None = None
    genre: str | None = None


class SeriesCreate(BaseModel):
    title: str
    episodes: int
    seasons: int
    description: str | None = None
    genre: str
    author_id: int


class SeriesSchema(BaseReturn, SeriesCreate):
    pass


class UserCreate(BaseModel):
    visible_name: str = Field(min_length=2, max_length=35)
    password: str = Field(min_length=5, max_length=255)
    email: EmailStr


class UserSchema(BaseReturn, BaseModel):
    visible_name: str
    email: EmailStr