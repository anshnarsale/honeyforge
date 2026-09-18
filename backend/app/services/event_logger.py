from app.core.database import SessionLocal
from app.models.event import Event

MAX_METADATA_SIZE = 4096  # rough safety limit on stored metadata


def log_event(
    honeypot_id: str,
    service: str,
    source_ip: str,
    event_type: str,
    source_port: int = None,
    session_id: str = None,
    metadata: dict = None,
):
    if metadata and len(str(metadata)) > MAX_METADATA_SIZE:
        metadata = {"truncated": True}

    db = SessionLocal()
    try:
        event = Event(
            honeypot_id=honeypot_id,
            service=service,
            source_ip=source_ip,
            source_port=source_port,
            event_type=event_type,
            session_id=session_id,
            event_metadata=metadata or {},
        )
        db.add(event)
        db.commit()
    finally:
        db.close()
