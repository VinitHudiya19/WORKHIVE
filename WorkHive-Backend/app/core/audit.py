from sqlalchemy.orm import Session
import uuid
from typing import Optional
from fastapi import Request
from app.models.audit_log import AuditLog

def log_audit(
    db: Session,
    user_id: uuid.UUID,
    action: str,
    resource_type: str,
    resource_id: Optional[uuid.UUID] = None,
    request: Optional[Request] = None
):
    """
    Log an audit entry. Adds the AuditLog model to the current DB session.
    The caller should call db.commit() to persist it (usually at the end of the route).
    """
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
    log_entry = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(log_entry)
