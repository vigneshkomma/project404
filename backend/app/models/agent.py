from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime, timezone
import uuid


def generate_uuid():
    return str(uuid.uuid4())

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))

    name = Column(String)
    description = Column(Text)

    runtime = Column(String)
    entry_file = Column(String)

    is_public = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))