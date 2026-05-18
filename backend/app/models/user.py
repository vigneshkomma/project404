from sqlalchemy import Column, String, DateTime
from app.core.database import Base
from datetime import datetime, timezone
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True,default=generate_uuid)

    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


    password_hash = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
