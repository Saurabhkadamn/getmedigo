from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="user-service", version="0.1.0")


class UserProfile(BaseModel):
    user_id: str
    full_name: str
    timezone: str = "UTC"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "user-service"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "service": "user-service"}


@app.get("/users/{user_id}", response_model=UserProfile)
def get_user(user_id: str) -> UserProfile:
    # Stub profile for scaffold only.
    return UserProfile(user_id=user_id, full_name="Demo User")
