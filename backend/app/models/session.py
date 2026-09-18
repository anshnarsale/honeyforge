import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime
from app.core.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    honeypot_id = Column(String, nullable=False)
    service = Column(String, nullable=False)  # http, tcp, ssh
    source_ip = Column(String, nullable=False)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime, nullable=True)
