from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
import os

from .auth import router as auth_router
from .tasks import router as tasks_router
from .database import engine
from .models import User
from .utils import decode_access_token

app = FastAPI()
app.include_router(auth_router)
app.include_router(tasks_router)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="frontend")


@app.middleware("http")
async def inject_user(request: Request, call_next):
    token = request.headers.get("Authorization")
    request.state.current_user = None
    if token and token.startswith("Bearer "):
        data = decode_access_token(token[7:])
        if data:
            with Session(engine) as session:
                user = session.get(User, UUID(data.get("sub")))
                request.state.current_user = user
    response = await call_next(request)
    return response

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
