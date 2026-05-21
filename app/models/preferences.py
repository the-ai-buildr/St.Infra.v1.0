import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


# SQLAlchemy Model
class Preferences(Base):
    __tablename__ = "preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    theme: Mapped[str] = mapped_column(String, default="system")
    default_view: Mapped[str] = mapped_column(String, default="dashboard")
    settings_json: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, server_default=text("'{}'::jsonb")
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()"),
    )


# Pydantic Schemas
class PreferencesBase(BaseModel):
    theme: str = "system"
    default_view: str = "dashboard"
    settings_json: Dict[str, Any] = {}


class PreferencesCreate(PreferencesBase):
    pass


class PreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    default_view: Optional[str] = None
    settings_json: Optional[Dict[str, Any]] = None


class PreferencesRead(PreferencesBase):
    id: uuid.UUID
    user_id: uuid.UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
