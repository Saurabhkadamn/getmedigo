from fastapi import FastAPI

app = FastAPI(title="content-service", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "content-service"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "service": "content-service"}


@app.get("/content/home")
def homepage_content() -> dict[str, object]:
    return {
        "hero": "Healthcare made simple.",
        "sections": ["benefits", "how-it-works", "faqs"],
    }
