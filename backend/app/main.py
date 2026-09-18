from fastapi import FastAPI

app = FastAPI(title="HoneyForge API")


@app.get("/")
def read_root():
    return {"status": "ok", "service": "HoneyForge API"}
