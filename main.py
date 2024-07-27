from fastapi import FastAPI, HTTPException, Body, Query, Request
from typing import Dict
from pydantic import BaseModel
import json

app = FastAPI()


class User(BaseModel):
    user: str


@app.post("/")
async def root(request: Request):
    # print("398191840983")
    body = await request.body()
    print(body)
    return "pass"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
