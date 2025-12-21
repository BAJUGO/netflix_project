from pydantic import BaseModel


class AccessTokenData(BaseModel):
    name: str
    role: str
    id: int
