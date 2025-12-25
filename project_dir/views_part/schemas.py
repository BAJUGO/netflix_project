from pydantic import BaseModel, Field, ConfigDict, EmailStr


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


#! эта схема бесполезна, пока не будет функции, возвращающая весь список пользователей
class UserSchema(BaseReturn):
    visible_name: str
