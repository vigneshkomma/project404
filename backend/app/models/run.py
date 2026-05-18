from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from app.core.database import Base
from datetime import datetime, timezone
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Run(Base):
    __tablename__ = "runs"

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agents.id"))
    user_id = Column(String, ForeignKey("users.id"))
    version_id = Column(String, ForeignKey("agent_versions.id"))

    status = Column(String)

    input = Column(JSON)
    output = Column(JSON)

    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))   