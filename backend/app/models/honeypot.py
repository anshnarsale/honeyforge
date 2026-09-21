import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, DateTime
from app.core.database import Base


class Honeypot(Base):
    __tablename__ = "honeypots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)  # http, tcp, ssh
    port = Column(Integer, nullable=False)
    banner = Column(String, nullable=True)
    hostname = Column(String, nullable=True)
    fake_username = Column(String, nullable=True)
    fake_password = Column(String, nullable=True)
    status = Column(String, default="stopped")  # stopped, running
    pid = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    started_at = Column(DateTime, nullable=True)
