from typing import Annotated

from fastapi import APIRouter, File, Security, UploadFile, status

from ....core.user import get_current_user
from ....schema.auth import User
from ....schema.file import File as FileResponse

router = APIRouter(prefix="/files", tags=["files"])


@router.post(
    "/upload_file",
    response_model=FileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_file(
    current_user: Annotated[User, Security(get_current_user, scopes=["files"])],
    file: UploadFile = File(...),
) -> FileResponse:
    return {"filename": file.filename, "user": current_user}
