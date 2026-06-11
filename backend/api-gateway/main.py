from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
import httpx

# 1. Manage a single HTTP client lifespan for better performance
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient()
    yield
    await app.state.http_client.aclose()

app = FastAPI(title="API Gateway", version="1.0.0", lifespan=lifespan)

USER_SERVICE_URL = "http://localhost:8001"

@app.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(path: str, request: Request):
    url = f"{USER_SERVICE_URL}/auth/{path}"
    body = await request.body()
    
    # Copy headers and remove the host header to avoid routing loops
    headers = dict(request.headers)
    headers.pop("host", None)
    
    # Reuse the global async client
    client = request.app.state.http_client
    
    response = await client.request(
        method=request.method,
        url=url,
        headers=headers,
        content=body,
        params=dict(request.query_params)
    )
    
    # 2. Properly return the raw content, status code, and content-type
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers={"Content-Type": response.headers.get("content-type", "application/json")}
    )

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}