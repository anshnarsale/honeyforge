from app.core.database import Base, engine
from app.models.honeypot import Honeypot
from app.models.event import Event
from app.models.session import Session

Base.metadata.create_all(bind=engine)
print("Database tables created.")
