from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any, TypeVar

ReturnType = TypeVar("ReturnType")

EXECUTOR = ThreadPoolExecutor()


async def run_in_threadpool(
    func: Callable[..., ReturnType],
    *args: Any,
    **kwargs: Any,
) -> ReturnType:
    from asyncio import get_event_loop
    from functools import partial

    loop = get_event_loop()

    return await loop.run_in_executor(EXECUTOR, partial(func, *args, **kwargs))
