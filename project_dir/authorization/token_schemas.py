from pydantic import BaseModel


class AccessTokenData(BaseModel):
    sub: int
    name: str
    role: str
    id: int
