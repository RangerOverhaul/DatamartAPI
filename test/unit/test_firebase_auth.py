import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from app.services.firebase_auth import FirebaseAuth
from app.services.auth_service import get_current_user


@pytest.mark.unit
class TestFirebaseAuth:
    """Tests para el servicio de autenticación Firebase"""

    @pytest.mark.asyncio
    async def test_verify_valid_firebase_token(self):
        """Debe verificar correctamente un token válido de Firebase"""
        with patch('firebase_admin.auth.verify_id_token') as mock_verify:
            mock_verify.return_value = {"uid": "123", "email": "test@example.com"}

            result = await FirebaseAuth.verify_firebase_token("valid_token")

            assert result["uid"] == "123"
            assert result["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_verify_expired_firebase_token(self):
        """Debe lanzar error para token expirado"""
        with patch('firebase_admin.auth.verify_id_token') as mock_verify:
            mock_verify.side_effect = Exception("Token expired")

            with pytest.raises(HTTPException) as exc_info:
                await FirebaseAuth.verify_firebase_token("expired_token")

            assert exc_info.value.status_code == 401