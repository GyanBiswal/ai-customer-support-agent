from fastapi import FastAPI
from sqlalchemy import text

from app.core.redis_client import redis_client
from app.db.session import engine

app = FastAPI(title="AI Customer Support Agent")


@app.get("/health")
async def health():
    status = {"api": "ok", "database": "unreachable", "redis": "unreachable"}

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        status["database"] = "ok"
    except Exception as e:
        status["database"] = f"error: {e}"

    try:
        await redis_client.ping()
        status["redis"] = "ok"
    except Exception as e:
        status["redis"] = f"error: {e}"

    return status