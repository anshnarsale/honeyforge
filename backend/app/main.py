from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.events import router as events_router
from app.api.honeypots import router as honeypots_router

app = FastAPI(title="HoneyForge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router)
app.include_router(honeypots_router)


@app.get("/")
def read_root():
    return {"status": "ok", "service": "HoneyForge API"}
