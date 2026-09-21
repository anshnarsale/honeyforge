from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.models.honeypot import Honeypot
from app.schemas.honeypot import HoneypotCreate, HoneypotOut
from app.services.process_manager import start_honeypot_process, stop_honeypot_process, VALID_SERVICE_TYPES

router = APIRouter(prefix="/api/honeypots", tags=["honeypots"])


@router.get("/", response_model=List[HoneypotOut])
def list_honeypots(db: DBSession = Depends(get_db)):
    return db.query(Honeypot).order_by(Honeypot.created_at.desc()).all()


@router.post("/", response_model=HoneypotOut)
def create_honeypot(payload: HoneypotCreate, db: DBSession = Depends(get_db)):
    if payload.service_type not in VALID_SERVICE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid service_type")
    if not (1 <= payload.port <= 65535):
        raise HTTPException(status_code=400, detail="Invalid port")

    honeypot = Honeypot(
        name=payload.name,
        service_type=payload.service_type,
        port=payload.port,
        banner=payload.banner,
        hostname=payload.hostname,
        fake_username=payload.fake_username,
        fake_password=payload.fake_password,
    )
    db.add(honeypot)
    db.commit()
    db.refresh(honeypot)
    return honeypot


@router.post("/{honeypot_id}/start", response_model=HoneypotOut)
def start_honeypot(honeypot_id: str, db: DBSession = Depends(get_db)):
    honeypot = db.query(Honeypot).filter(Honeypot.id == honeypot_id).first()
    if not honeypot:
        raise HTTPException(status_code=404, detail="Honeypot not found")
    if honeypot.status == "running":
        raise HTTPException(status_code=400, detail="Honeypot already running")

    pid = start_honeypot_process(honeypot.id, honeypot.service_type, honeypot.port)
    honeypot.status = "running"
    honeypot.pid = pid
    honeypot.started_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(honeypot)
    return honeypot


@router.post("/{honeypot_id}/stop", response_model=HoneypotOut)
def stop_honeypot(honeypot_id: str, db: DBSession = Depends(get_db)):
    honeypot = db.query(Honeypot).filter(Honeypot.id == honeypot_id).first()
    if not honeypot:
        raise HTTPException(status_code=404, detail="Honeypot not found")
    if honeypot.status != "running":
        raise HTTPException(status_code=400, detail="Honeypot not running")

    if honeypot.pid:
        stop_honeypot_process(honeypot.pid)
    honeypot.status = "stopped"
    honeypot.pid = None
    db.commit()
    db.refresh(honeypot)
    return honeypot


@router.delete("/{honeypot_id}")
def delete_honeypot(honeypot_id: str, db: DBSession = Depends(get_db)):
    honeypot = db.query(Honeypot).filter(Honeypot.id == honeypot_id).first()
    if not honeypot:
        raise HTTPException(status_code=404, detail="Honeypot not found")
    if honeypot.status == "running" and honeypot.pid:
        stop_honeypot_process(honeypot.pid)
    db.delete(honeypot)
    db.commit()
    return {"deleted": True}
