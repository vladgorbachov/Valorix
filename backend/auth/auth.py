from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

USERS = {"test@example.com": "password123"}

@router.post("/login")
async def login(request: LoginRequest):
    if USERS.get(request.email) == request.password:
        return {"token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
