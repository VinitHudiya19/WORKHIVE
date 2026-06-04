from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
import enum
from app.core.database import Base


class ProjectAccessRole(enum.Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    MANAGER = "manager"


class ProjectAccess(Base):
    __tablename__ = "project_access"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(ProjectAccessRole), default=ProjectAccessRole.VIEWER, nullable=False)
    granted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    project = relationship("Project")
    user = relationship("User")
