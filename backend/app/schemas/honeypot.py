from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HoneypotCreate(BaseModel):
    name: str
    service_type: str
    port: int
    banner: Optional[str] = None
    hostname: Optional[str] = None
    fake_username: Optional[str] = None
    fake_password: Optional[str] = None


class HoneypotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    service_type: str
    port: int
    banner: Optional[str] = None
    hostname: Optional[str] = None
    fake_username: Optional[str] = None
    fake_password: Optional[str] = None
    status: str
    pid: Optional[int] = None
    created_at: datetime
    started_at: Optional[datetime] = None
