from fastapi import FastAPI

from app.api.events import router as events_router

app = FastAPI(title="HoneyForge API")

app.include_router(events_router)


@app.get("/")
def read_root():
    return {"status": "ok", "service": "HoneyForge API"}
