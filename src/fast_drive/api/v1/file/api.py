from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Security, UploadFile, status

from ....core.user import get_current_user
from ....schema.auth import User
from ....schema.file import FileResponse, FilesResponse

router = APIRouter(prefix="/files", tags=["files"])


def get_user_static_path(username: str) -> str:
    return f"./static/{username}"


@router.post(
    "/upload_file",
    response_model=FileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_file(
    current_user: Annotated[User, Security(get_current_user, scopes=["files"])],
    file: UploadFile = File(...),
):
    """
    Upload a file

    Args:
        current_user (Annotated[User, Security]): Current user
        file (UploadFile): File to upload

    Returns:
        FileResponse: File
    """
    from ....core.disk import async_copy_file, create_folder

    root_path = get_user_static_path(current_user.username)
    create_folder(root_path)

    return {
        "filename": await async_copy_file(
            file=file.file,
            path=root_path,
            filename=file.filename,  # type: ignore
        ),
        "user": current_user,
    }


@router.post(
    "/upload_files",
    status_code=status.HTTP_201_CREATED,
    response_model=FilesResponse,
)
async def create_files(
    current_user: Annotated[User, Security(get_current_user, scopes=["files"])],
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    """
    Upload multiple files

    Args:
        current_user (Annotated[User, Security]): Current user
        files (Annotated[list[UploadFile], File]): Files to upload

    Returns:
        FilesResponse: Files
    """
    from ....core.disk import asnyc_copy_files, create_folder

    root_path = get_user_static_path(current_user.username)
    create_folder(root_path)

    filenames = await asnyc_copy_files(files=files, root_path=root_path)

    return {"files": filenames, "user": current_user}


@router.get(
    "/get_files",
    status_code=status.HTTP_200_OK,
    response_model=FilesResponse,
    responses={
        200: {"model": FilesResponse},
        404: {
            "description": "Not found directory for {user}",
            "content": {
                "application/json": {
                    "example": {"detail": "Not found directory for {user}"}
                }
            },
        },
    },
)
async def get_files_by_self(
    current_user: Annotated[User, Security(get_current_user, scopes=["files"])],
):
    """
    Get files by self

    Args:
        current_user (Annotated[User, Security]): Current user

    Raises:
        HTTPException: Not found directory for {user}

    Returns:
        FilesResponse: Files
    """
    root_path = get_user_static_path(current_user.username)

    try:
        from os import listdir

        files = listdir(path=root_path)

        return {"files": files, "user": current_user}
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Not found directory for {current_user.username}",
        ) from FileNotFoundError
