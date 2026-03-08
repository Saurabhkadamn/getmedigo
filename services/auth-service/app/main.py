from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI(title="auth-service", version="0.1.0")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "auth-service"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "service": "auth-service"}


@app.post("/auth/login")
def login(payload: LoginRequest) -> dict[str, str]:
    # Stub response for initial architecture bootstrap.
    return {
        "access_token": f"stub-token-for-{payload.email}",
        "token_type": "bearer",
    }
