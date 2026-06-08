from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Generation(Base):
    __tablename__ = "generations"

    id         = Column(Integer, primary_key=True, index=True)
    platform   = Column(String(50), nullable=False)
    topic      = Column(String(255), nullable=False)
    audience   = Column(String(255), nullable=False)
    tone       = Column(String(100), nullable=True)
    language   = Column(String(10), nullable=True, default="es")
    model_used = Column(String(100), nullable=False)
    content    = Column(Text, nullable=False)
    image_url  = Column(String(500), nullable=True)
    gen_type   = Column(String(50), nullable=False, default="general")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))