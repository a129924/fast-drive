from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/")
async def test():
    from contextlib import redirect_stdout
    from io import StringIO
    from uuid import uuid4

    buff = StringIO()

    uuid = uuid4()

    with redirect_stdout(buff):
        for i in range(1000000):
            print(f"{uuid}_{i}")

    return {"uuid": uuid, "count": 1000000, "output": buff.getvalue()}
