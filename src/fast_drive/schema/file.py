from pydantic import BaseModel

from .auth import UserResponse


class FileResponse(BaseModel):
    filename: str
    user: UserResponse


class FilesResponse(BaseModel):
    files: list[str]
    user: UserResponse
