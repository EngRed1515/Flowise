"""Authentication, password hashing, JWT issuance, and RBAC permission matrix."""
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.governance import User

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

# Role -> set of permission verbs. '*' = all permissions (Administrator).
ROLE_PERMISSIONS: dict[str, set[str]] = {
    "Administrator": {"*"},
    "Methodologist": {"rule:read", "rule:write", "rule:approve", "standard:read", "standard:write",
                      "metadata:read", "metadata:write", "enterprise:read", "classify:run", "classify:read",
                      "review:read", "quality:read"},
    "Data Steward": {"enterprise:read", "enterprise:write", "ownership:write", "classify:run", "classify:read",
                     "quality:read", "review:read", "review:write", "metadata:read", "rule:read"},
    "Classifier": {"enterprise:read", "enterprise:write", "classify:run", "classify:read", "review:read",
                   "rule:read", "metadata:read", "quality:read"},
    "Reviewer": {"enterprise:read", "review:read", "review:write", "classify:run", "classify:read",
                 "override:write", "rule:read", "metadata:read", "quality:read"},
    "Auditor": {"enterprise:read", "audit:read", "classify:read", "quality:read", "rule:read",
                "metadata:read", "review:read", "standard:read"},
    "Analyst": {"enterprise:read", "classify:read", "quality:read", "rule:read", "metadata:read",
                "standard:read", "review:read"},
}


def hash_password(pw: str) -> str:
    return pwd_context.hash(pw)


def verify_password(pw: str, hashed: str) -> bool:
    return pwd_context.verify(pw, hashed)


def create_access_token(username: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": username, "role": role, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def has_permission(role: str, perm: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, set())
    return "*" in perms or perm in perms


def get_current_user(token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    cred_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if not token:
        raise cred_exc
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        username = payload.get("sub")
    except JWTError:
        raise cred_exc
    user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if not user or not user.is_active:
        raise cred_exc
    return user


def require(perm: str):
    """Dependency factory enforcing a permission for the current user."""

    def _dep(user: User = Depends(get_current_user)) -> User:
        if not has_permission(user.role, perm):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Role '{user.role}' lacks permission '{perm}'")
        return user

    return _dep
