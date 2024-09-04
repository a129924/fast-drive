from fastapi import FastAPI

from .api.v1.v1_router import router as v1_router

app = FastAPI()
app.include_router(v1_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
