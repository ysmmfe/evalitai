from fastapi import FastAPI

from core.config import settings

app = FastAPI(
    title="Evalitai API",
    version="0.1.0",
    docs_url="/docs" if settings.environment == "development" else None,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
