"""
Core functionality for Tokenmon (Mega)

Tokenmon genera y valida tokens seguros (JWT, etc).
Misión: Red Dead Redemption
Rol: token-manager
"""

import base64
import hashlib
import hmac
import logging
import secrets
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, TokenResult

logger = logging.getLogger(__name__)


class Tokenmon:
    """
    Tokenmon - Token Manager (Mega)

    Descripción:
        Genera y valida tokens seguros (JWT simulado) con HMAC,
        expiración y verificación de integridad (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Tokenmon.

        Args:
            config: Diccionario de configuración opcional:
                - token_type: Tipo de token (default: "JWT")
                - algorithm: Algoritmo (default: "HS256")
                - expiration_hours: Expiración en horas (default: 24)
                - secret_length: Longitud del secreto (default: 32)
        """
        self.name = "Tokenmon"
        self.mission = "Red Dead Redemption"
        self.role = "token-manager"
        self.config = config or {}

        self.token_type = self.config.get("token_type", "JWT")
        self.algorithm = self.config.get("algorithm", "HS256")
        self.expiration_hours = int(self.config.get("expiration_hours", 24))
        self.secret_length = int(self.config.get("secret_length", 32))

        # Secreto por defecto (en producción debería venir de configuración segura)
        self.secret = secrets.token_bytes(self.secret_length)

        logger.info(
            "Initialized %s - %s (type=%s, algo=%s, exp=%dh)",
            self.name,
            self.role,
            self.token_type,
            self.algorithm,
            self.expiration_hours,
        )

    def generate_token(self, claims: Optional[Dict[str, Any]] = None, expiration_hours: Optional[int] = None) -> TokenResult:
        """
        Genera un token seguro.

        Args:
            claims: Claims/payload del token
            expiration_hours: Horas hasta expiración (opcional)

        Returns:
            TokenResult con token generado
        """
        exp_hours = expiration_hours or self.expiration_hours
        exp_time = datetime.now() + timedelta(hours=exp_hours)

        # Payload básico
        payload = {
            "iat": int(time.time()),
            "exp": int(exp_time.timestamp()),
            "type": self.token_type,
        }
        if claims:
            payload.update(claims)

        # Simulación de JWT: header.payload.signature
        header_b64 = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').decode("utf-8").rstrip("=")
        payload_b64 = base64.urlsafe_b64encode(str(payload).encode("utf-8")).decode("utf-8").rstrip("=")

        # HMAC para firma (simulado)
        message = f"{header_b64}.{payload_b64}".encode("utf-8")
        signature = hmac.new(self.secret, message, hashlib.sha256).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")

        token = f"{header_b64}.{payload_b64}.{signature_b64}"

        return TokenResult(
            token=token,
            token_type=self.token_type,
            algorithm=self.algorithm,
            expires_at=exp_time.isoformat(),
            valid=True,
            claims=payload,
            errors=[],
        )

    def validate_token(self, token: str) -> TokenResult:
        """
        Valida un token.

        Args:
            token: Token a validar

        Returns:
            TokenResult con resultado de validación
        """
        errors: List[str] = []
        valid = True

        try:
            parts = token.split(".")
            if len(parts) != 3:
                errors.append("Invalid token format")
                valid = False
            else:
                header_b64, payload_b64, signature_b64 = parts

                # Verificar firma
                message = f"{header_b64}.{payload_b64}".encode("utf-8")
                expected_sig = hmac.new(self.secret, message, hashlib.sha256).digest()
                expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode("utf-8").rstrip("=")

                if signature_b64 != expected_sig_b64:
                    errors.append("Invalid signature")
                    valid = False

                # Decodificar payload (simplificado)
                try:
                    payload_bytes = base64.urlsafe_b64decode(payload_b64 + "==")
                    # En una implementación real se parsearía JSON
                    claims = {"decoded": True}
                except Exception:
                    errors.append("Invalid payload encoding")
                    valid = False
                    claims = {}

                # Verificar expiración (simplificado)
                current_time = int(time.time())
                if claims.get("exp", 0) < current_time:
                    errors.append("Token expired")
                    valid = False

        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            valid = False
            claims = {}

        return TokenResult(
            token=token,
            token_type=self.token_type,
            algorithm=self.algorithm,
            expires_at=None,
            valid=valid,
            claims=claims,
            errors=errors,
        )

    def analyze(self, action: str = "generate", claims: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> AnalysisResult:
        """
        Ejecuta análisis: generar o validar token.

        Args:
            action: Acción ("generate" o "validate")
            claims: Claims para generar (si action="generate")
            token: Token para validar (si action="validate")

        Returns:
            AnalysisResult con resultados
        """
        if action == "generate":
            result = self.generate_token(claims=claims)
            status = "success" if result.valid else "error"
            return AnalysisResult(
                status=status,
                message="Token generated successfully" if result.valid else "Token generation failed",
                data=result.model_dump(),
            )

        elif action == "validate" and token:
            result = self.validate_token(token)
            status = "success" if result.valid else "warning"
            return AnalysisResult(
                status=status,
                message="Token is valid" if result.valid else "Token validation failed",
                data=result.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="Invalid action or missing parameters",
            data={},
            errors=["invalid_input"],
        )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, str):
            return bool(data)
        if isinstance(data, dict):
            return True  # Claims o configuración
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "token_type": self.token_type,
            "algorithm": self.algorithm,
        }


# Alias para retrocompatibilidad
Digimon = Tokenmon

