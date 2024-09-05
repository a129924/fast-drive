from typing import BinaryIO

from fastapi import UploadFile

from ._asyncio import run_in_threadpool


def create_folder(path: str):
    """
    Create a folder at the given path.
    If the folder already exists, do nothing.

    Args:
        path (str): The path to create the folder at.

    Returns:
        str: The path that was created.
    """
    from os import makedirs

    makedirs(path, exist_ok=True)


def copy_file(file: BinaryIO, path: str, filename: str) -> str:
    """
    Copy a file to the given path.

    Args:
        file (BinaryIO): The file to copy.
        path (str): The path to copy the file to.
        filename (str): The name of the file to copy.

    Returns:
        str: The name of the file that was copied.
    """
    from shutil import copyfileobj

    with open(f"{path}/{filename}", "wb") as f:
        copyfileobj(file, f)

    return filename


async def async_copy_file(file: BinaryIO, path: str, filename: str) -> str:
    """
    Copy a file to the given path.

    Args:
        file (BinaryIO): The file to copy.
        path (str): The path to copy the file to.
        filename (str): The name of the file to copy.

    Returns:
        str: The name of the file that was copied.
    """
    return await run_in_threadpool(copy_file, file, path, filename)


async def asnyc_copy_files(files: list[UploadFile], root_path: str) -> list[str]:
    """
    Copy multiple files to the given path.

    Args:
        files (list[UploadFile]): The files to copy.
        root_path (str): The path to copy the files to.

    Returns:
        list[str]: The names of the files that were copied.
    """
    from asyncio import gather

    tasks = (
        async_copy_file(file=file.file, path=root_path, filename=file.filename)  # type: ignore
        for file in files
    )

    return await gather(*tasks)
