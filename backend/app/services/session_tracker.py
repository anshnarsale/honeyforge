import uuid
from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.session import Session


def start_session(honeypot_id: str, service: str, source_ip: str) -> str:
    session_id = str(uuid.uuid4())
    db = SessionLocal()
    try:
        session = Session(
            id=session_id,
            honeypot_id=honeypot_id,
            service=service,
            source_ip=source_ip,
        )
        db.add(session)
        db.commit()
    finally:
        db.close()
    return session_id


def end_session(session_id: str):
    db = SessionLocal()
    try:
        session = db.query(Session).filter(Session.id == session_id).first()
        if session:
            session.ended_at = datetime.now(timezone.utc)
            db.commit()
    finally:
        db.close()
