from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix = "/auth", tags = ["auth"])


@router.post("/login")
async def login(username: str, password: str):
    # TODO: Implement the logic to login
    pass
