import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, DateTime, JSON
from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    honeypot_id = Column(String, nullable=False)
    service = Column(String, nullable=False)  # http, tcp, ssh
    source_ip = Column(String, nullable=False)
    source_port = Column(Integer, nullable=True)
    event_type = Column(String, nullable=False)  # http_request, tcp_connect, ssh_login, ssh_command
    session_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    event_metadata = Column(JSON, nullable=True)
