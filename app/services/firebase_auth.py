import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.exceptions import FirebaseError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import requests
import logging
from typing import Optional
import jwt
from app.config import settings

logger = logging.getLogger(__name__)

security = HTTPBearer()


class FirebaseAuth:
    """Servicio para autenticación con Firebase usando email/password"""

    FIREBASE_SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.FIREBASE_API_KEY}"

    @staticmethod
    async def authenticate_user(email: str, password: str) -> dict:
        """
        Auténtica un usuario con email y contraseña usando Firebase REST API
        """
        try:
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }

            logger.info(f"Autenticando usuario: {email}")
            response = requests.post(
                FirebaseAuth.FIREBASE_SIGN_IN_URL,
                json=payload,
                timeout=10
            )

            data = response.json()

            if response.status_code != 200:
                error_msg = data.get("error", {}).get("message", "Error de autenticación")
                logger.error(f"Firebase auth error: {error_msg}")

                # Mapeo de errores de Firebase
                error_mappings = {
                    "EMAIL_NOT_FOUND": ("Usuario no encontrado", status.HTTP_404_NOT_FOUND),
                    "INVALID_PASSWORD": ("Contraseña incorrecta", status.HTTP_401_UNAUTHORIZED),
                    "USER_DISABLED": ("Usuario deshabilitado", status.HTTP_401_UNAUTHORIZED),
                    "TOO_MANY_ATTEMPTS_TRY_LATER": ("Demasiados intentos, intenta más tarde",
                                                    status.HTTP_429_TOO_MANY_REQUESTS),
                }

                detail, status_code = error_mappings.get(
                    error_msg,
                    (f"Error de autenticación: {error_msg}", status.HTTP_401_UNAUTHORIZED)
                )

                raise HTTPException(status_code=status_code, detail=detail)

            # Extraer datos del usuario de la respuesta
            user_data = {
                "uid": data.get("localId"),
                "email": data.get("email"),
                "id_token": data.get("idToken"),
                "refresh_token": data.get("refreshToken", ""),
                "email_verified": data.get("emailVerified", False),
                "expires_in": data.get("expiresIn", "")
            }

            logger.info(f"Usuario autenticado exitosamente: {user_data['email']}")
            return user_data

        except requests.exceptions.Timeout:
            logger.error("Timeout al conectar con Firebase")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Timeout en servicio de autenticación"
            )
        except requests.exceptions.ConnectionError:
            logger.error("Error de conexión con Firebase")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio de autenticación no disponible"
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error inesperado en autenticación: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )




