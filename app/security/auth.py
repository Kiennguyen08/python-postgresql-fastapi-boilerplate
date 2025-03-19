from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.constants.error import ErrorCode
from app.cores.errors import PermissionDeniedException
from app.endpoints import endpoint


class SecurityHeaders(BaseModel):
    x_token: str = None


security = HTTPBearer()


# Dependency to validate the token
async def get_current_user(
    security: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    if not security.credentials:
        raise PermissionDeniedException(ErrorCode.UNAUTHORIZED_PASSPORT.value)
    try:
        user = await endpoint.passport.authenticate(token=security.credentials)
        return user.data
    except Exception:
        raise PermissionDeniedException(ErrorCode.UNAUTHENTICATED_PASSPORT.value)
