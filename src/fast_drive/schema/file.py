from pydantic import BaseModel

from .auth import UserResponse


class File(BaseModel):
    filename: str
    user: UserResponse
