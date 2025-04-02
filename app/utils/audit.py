from typing import Optional, Dict, Any
from fastapi import Request
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.schemas.audit import AuditLogCreate
import uuid


def create_audit_log(
        db: Session,
        action: str,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None
) -> AuditLog:
    """
    감사 로그를 생성합니다.
    
    Args:
        db: 데이터베이스 세션
        action: 수행된 작업 (예: 'login', 'deposit', 'advisory_request')
        user_id: 사용자 ID (선택사항)
        details: 추가 상세 정보 (선택사항)
        request: FastAPI Request 객체 (선택사항)
    
    Returns:
        생성된 AuditLog 객체
    """
    ip_address = None
    user_agent = None

    if request:
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent")

    audit_log = AuditLog(
        id=str(uuid.uuid4()),
        user_id=user_id,
        action=action,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log


def log_user_action(
        db: Session,
        action: str,
        user_id: str,
        details: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None
) -> None:
    """
    사용자 행동을 로깅합니다.
    
    Args:
        db: 데이터베이스 세션
        action: 수행된 작업
        user_id: 사용자 ID
        details: 추가 상세 정보 (선택사항)
        request: FastAPI Request 객체 (선택사항)
    """
    create_audit_log(db, action, user_id, details, request)


def log_system_action(
        db: Session,
        action: str,
        details: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None
) -> None:
    """
    시스템 행동을 로깅합니다.
    
    Args:
        db: 데이터베이스 세션
        action: 수행된 작업
        details: 추가 상세 정보 (선택사항)
        request: FastAPI Request 객체 (선택사항)
    """
    create_audit_log(db, action, None, details, request)
