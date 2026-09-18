from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.models.event import Event
from app.schemas.event import EventOut

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("/", response_model=List[EventOut])
def list_events(limit: int = Query(default=50, le=200), db: DBSession = Depends(get_db)):
    events = db.query(Event).order_by(Event.timestamp.desc()).limit(limit).all()
    return events
