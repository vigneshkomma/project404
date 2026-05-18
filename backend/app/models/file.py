from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime, timezone
import uuid



def generate_uuid():
    return str(uuid.uuid4())

class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agents.id"))
    user_id = Column(String, ForeignKey("users.id"))

    filename = Column(String)
    storage_key = Column(String)
    file_type = Column(String)
    size = Column(Integer)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))