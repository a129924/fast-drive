from pydantic import BaseModel


class User(BaseModel):
    username: str
    full_name: str
    email: str
    hashed_password: str
