from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    honeypot_id: str
    service: str
    source_ip: str
    source_port: Optional[int] = None
    event_type: str
    session_id: Optional[str] = None
    timestamp: datetime
    event_metadata: Optional[dict] = None
