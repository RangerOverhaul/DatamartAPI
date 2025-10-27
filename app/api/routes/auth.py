import logging
from datetime import timedelta, datetime
import jwt
from fastapi import APIRouter, Depends, HTTPException, status


from app.config import settings
from app.services.firebase_auth import FirebaseAuth
from app.services.auth_service import get_current_user, create_jwt_token
from app.models.schemas import UserProfile, LoginRequest
from app.models.responses import LoginResponse

router = APIRouter(prefix = "/api/v1/auth", tags = ["authentication"])

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Autenticar usuario",
    description="Autentica un usuario usando Firebase ID token y retorna un JWT"
)
async def login(login_data: LoginRequest):
    """
    Endpoint para autenticar usuarios con email y contraseña.
    """
    try:
        # Autenticar con Firebase
        user_data = await FirebaseAuth.authenticate_user(
            email=login_data.email,
            password=login_data.password
        )

        # Crear JWT personalizado
        jwt_token = create_jwt_token(user_data)

        return LoginResponse(
            access_token=jwt_token,
            token_type="bearer",
            user_id=user_data.get("uid"),
            email=user_data.get("email"),
            email_verified=user_data.get("email_verified", False),
            expires_in=30 * 60  # 30 minutos en segundos
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el login: {str(e)}"
        )


@router.get(
    "/self",
    response_model=UserProfile,
    summary="Obtener perfil de usuario",
    description="Obtiene el perfil del usuario autenticado"
)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Endpoint para obtener el perfil del usuario actual.
    """
    return UserProfile(
        user_id=current_user.get("sub"),
        email=current_user.get("email"),
        email_verified=current_user.get("email_verified", False)
    )

@router.post(
    "/verify",
    summary="Verificar token",
    description="Verifica si un token JWT es válido"
)
async def verify_token(current_user: dict = Depends(get_current_user)):
    """
    Endpoint para verificar la validez de un token.
    """
    return {
        "valid": True,
        "user_id": current_user.get("sub"),
        "email": current_user.get("email"),
        "email_verified": current_user.get("email_verified", False)
    }


