import logging
from datetime import timedelta, datetime
from typing import Optional

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status

from app.config import settings
from app.services.firebase_auth import security, FirebaseAuth, logger

def create_jwt_token(user_data: dict) -> str:
    """
    Crea un JWT token personalizado con la información del usuario
    """
    expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now() + expires_delta

    payload = {
        "sub": user_data.get("uid"),
        "email": user_data.get("email"),
        "email_verified": user_data.get("email_verified", False),
        "exp": expire,
        "type": "access"
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token

def verify_jwt_token(token: str) -> dict:
    """
    Verifica un JWT token personalizado
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Validaciones adicionales
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tipo de token inválido"
            )

        return payload

    except jwt.exceptions.PyJWTError as e:
        logging.error(f"JWT Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de autenticacion"
        )

# Dependencia para proteger endpoints
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependencia para obtener el usuario actual desde el token JWT
    """
    token = credentials.credentials

    try:
        user_data = verify_jwt_token(token)
        return user_data
    except HTTPException as e:
        logger.error(f"Error de autenticación: {str(e)}")
        raise


# Opcional (para endpoints que pueden ser públicos/privados)
async def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[dict]:
    """
    Dependencia opcional que retorna usuario si existe, None si no
    """
    if credentials is None:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None