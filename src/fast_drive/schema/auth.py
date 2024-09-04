from pydantic import BaseModel


class User(BaseModel):
    username: str
    full_name: str
    email: str
    hashed_password: str
    disabled: bool = False


class UserResponse(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
