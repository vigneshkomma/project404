from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime, timezone
import uuid

def generate_uuid():
    return str(uuid.uuid4())


class AgentVersion(Base):
    __tablename__ = "agent_version"

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agents.id"))

    version = Column(Integer)
    code_storage_key = Column(String)
    commit_message = Column(String)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))