import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="api-gateway", version="0.1.0")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8002")
CONTENT_SERVICE_URL = os.getenv("CONTENT_SERVICE_URL", "http://content-service:8003")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "api-gateway"}


async def proxy_post(url: str, payload: dict[str, Any], request_id: str | None = None) -> Any:
    headers = {"x-request-id": request_id} if request_id else {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


async def proxy_get(url: str, request_id: str | None = None) -> Any:
    headers = {"x-request-id": request_id} if request_id else {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url, headers=headers)
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.get("/ready")
async def ready() -> dict[str, Any]:
    results: dict[str, str] = {}
    all_ready = True

    async with httpx.AsyncClient(timeout=2.0) as client:
        for service_name, url in READINESS_TARGETS.items():
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    results[service_name] = "ready"
                else:
                    results[service_name] = f"not_ready_http_{response.status_code}"
                    all_ready = False
            except httpx.HTTPError:
                results[service_name] = "unreachable"
                all_ready = False

    if not all_ready:
        raise HTTPException(status_code=503, detail={"status": "not_ready", "checks": results})

    return {"status": "ready", "service": "api-gateway", "checks": results}


@app.post("/api/v1/auth/login")
async def login(request: Request) -> Any:
    payload = await request.json()
    return await proxy_post(
        f"{AUTH_SERVICE_URL}/auth/login",
        payload,
        request.headers.get("x-request-id"),
    )


@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: str, request: Request) -> Any:
    return await proxy_get(
        f"{USER_SERVICE_URL}/users/{user_id}",
        request.headers.get("x-request-id"),
    )


@app.get("/api/v1/content/home")
async def get_home_content(request: Request) -> Any:
    return await proxy_get(
        f"{CONTENT_SERVICE_URL}/content/home",
        request.headers.get("x-request-id"),
    )
