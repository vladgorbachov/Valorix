from fastapi import FastAPI
from auth.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api", tags=["auth"])
