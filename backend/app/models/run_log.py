from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime, timezone
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class RunLog(Base):
    __tablename__ = "run_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    run_id = Column(String, ForeignKey("runs.id"))

    log = Column(Text)
    level = Column(String)

    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))