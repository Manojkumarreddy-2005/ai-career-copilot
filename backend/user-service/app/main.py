from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.auth import router as auth_router
import structlog

log = structlog.get_logger()

# 1. Define the lifespan behavior (startup and shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs ON STARTUP
    log.info("user_service_started")
    yield
    # This runs ON SHUTDOWN (Optional, but great for cleaning up resources)
    log.info("user_service_shutdown")

# 2. Pass the lifespan handler into your FastAPI instance
app = FastAPI(title="User Service", version="1.0.0", lifespan=lifespan)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}