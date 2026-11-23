from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..database import get_db
from ..model import employee , department
from .jwt_handler import verify_access_token

optional_security = HTTPBearer(auto_error=False)


def _extract_token(
    access_token: str | None = Cookie(default=None),
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_security),
) -> str | None:
    if access_token:
        return access_token
    if credentials and credentials.credentials:
        return credentials.credentials
    return None


def get_current_employee(
    token: str | None = Depends(_extract_token),
    db: Session = Depends(get_db),
) -> employee:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_access_token(token)
    user_id = payload.get("sub") or payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is missing user identification",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(employee).filter(employee.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


ROLE_CUSTOMER = 0
ROLE_SHOP_OWNER = 1
ROLE_SUPER_ADMIN = 2


def require_role(*roles: int):
    """Factory dependency that requires the user to have one of the specified roles."""
    def _role_checker(current_user: employee = Depends(get_current_employee)) -> employee:
        user_role = getattr(current_user, "role", 0)
        if user_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: requires role in {roles}, but your role is {user_role}",
            )
        return current_user
    return _role_checker


def require_shop_owner(
    current_user: employee = Depends(get_current_employee),
) -> employee:
    """Requires authenticated user with Role 1 (Shop Owner) or Role 2 (Super Admin)."""
    user_role = getattr(current_user, "role", 0)
    if user_role not in (ROLE_SHOP_OWNER, ROLE_SUPER_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Shop Owner or Super Admin privileges required to perform this action",
        )
    return current_user
