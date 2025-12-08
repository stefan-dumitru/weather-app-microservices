from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security_scheme = HTTPBearer()

def validate_token(credentials = Depends(security_scheme)):
    """
    Supports both:
    - Bearer token via header (normal API)
    - Raw token string (SSE using query param)
    """

    # If SSE passed raw token as string
    if isinstance(credentials, str):
        token = credentials

    # Normal protected route
    else:
        token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )