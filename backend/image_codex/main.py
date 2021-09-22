import os

from fastapi import FastAPI

app = FastAPI(root_path=os.environ.get('ROOT_PATH') or "")


@app.get("/")
async def root():
    return {"message": "Hello World"}
