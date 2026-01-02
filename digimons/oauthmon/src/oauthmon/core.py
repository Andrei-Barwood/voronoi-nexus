"""
Core functionality for OAuthmon (Mega)

OAuthmon maneja flujos OAuth 2.0 con generación y validación de tokens.
Misión: Marko Dragic
Rol: oauth-handler
"""

import logging
import secrets
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, OAuthAnalysis, OAuthToken

logger = logging.getLogger(__name__)


class OAuthmon:
    """
    OAuthmon - OAuth Handler (Mega)

    Descripción:
        Maneja flujos OAuth 2.0 con generación de tokens, refresh tokens,
        y análisis de seguridad (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar OAuthmon.

        Args:
            config: Diccionario de configuración opcional:
                - authorization_url: URL de autorización (opcional)
                - token_url: URL de token (opcional)
                - client_id: Client ID (opcional)
                - supported_flows: Flujos soportados (default: authorization_code, client_credentials, implicit)
        """
        self.name = "OAuthmon"
        self.mission = "Marko Dragic"
        self.role = "oauth-handler"
        self.config = config or {}

        self.authorization_url = self.config.get("authorization_url")
        self.token_url = self.config.get("token_url")
        self.client_id = self.config.get("client_id")
        self.supported_flows = self.config.get(
            "supported_flows", ["authorization_code", "client_credentials", "implicit"]
        )

        # Simulación de almacenamiento de tokens (en producción usar DB/Redis)
        self.tokens: Dict[str, Dict[str, Any]] = {}

        logger.info(
            "Initialized %s - %s (flows=%s, client_id=%s)",
            self.name,
            self.role,
            len(self.supported_flows),
            "configured" if self.client_id else "not_set",
        )

    def generate_token(self, flow_type: str = "authorization_code", scope: Optional[str] = None, expires_in: int = 3600) -> OAuthToken:
        """
        Genera un token OAuth.

        Args:
            flow_type: Tipo de flujo OAuth
            scope: Scope del token (opcional)
            expires_in: Expiración en segundos (default: 3600)

        Returns:
            OAuthToken generado
        """
        if flow_type not in self.supported_flows:
            raise ValueError(f"Unsupported OAuth flow: {flow_type}")

        access_token = secrets.token_urlsafe(32)
        refresh_token = None

        # Refresh token solo para authorization_code
        if flow_type == "authorization_code":
            refresh_token = secrets.token_urlsafe(32)

        now = datetime.now()

        token_data = {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": expires_in,
            "refresh_token": refresh_token,
            "scope": scope,
            "created_at": now.isoformat(),
            "expires_timestamp": (now.timestamp() + expires_in),
            "flow_type": flow_type,
        }

        self.tokens[access_token] = token_data

        return OAuthToken(
            access_token=access_token,
            token_type="Bearer",
            expires_in=expires_in,
            refresh_token=refresh_token,
            scope=scope,
            created_at=now.isoformat(),
        )

    def validate_token(self, access_token: str) -> bool:
        """
        Valida un token OAuth.

        Args:
            access_token: Token a validar

        Returns:
            True si el token es válido
        """
        if access_token not in self.tokens:
            return False

        token_data = self.tokens[access_token]
        expires_timestamp = token_data.get("expires_timestamp", 0)

        if time.time() > expires_timestamp:
            self.tokens.pop(access_token, None)
            return False

        return True

    def analyze_oauth(self) -> OAuthAnalysis:
        """
        Analiza todos los tokens OAuth.

        Returns:
            OAuthAnalysis con resultados
        """
        now_timestamp = time.time()
        active = []
        expired = []
        tokens_by_flow: Dict[str, int] = defaultdict(int)
        violations: List[str] = []

        for token, token_data in list(self.tokens.items()):
            flow_type = token_data.get("flow_type", "unknown")
            tokens_by_flow[flow_type] += 1

            expires_timestamp = token_data.get("expires_timestamp", 0)
            if now_timestamp > expires_timestamp:
                expired.append(token)
                self.tokens.pop(token, None)
            else:
                active.append(token)

        # Verificar violaciones
        for flow in tokens_by_flow.keys():
            if flow not in self.supported_flows:
                violations.append(f"Unsupported flow type found: {flow}")

        return OAuthAnalysis(
            total_tokens=len(self.tokens),
            active_tokens=len(active),
            tokens_by_flow=dict(tokens_by_flow),
            expired_tokens=len(expired),
            violations=violations,
            analysis_summary={
                "authorization_url": self.authorization_url,
                "token_url": self.token_url,
                "client_id": self.client_id if self.client_id else "not_set",
                "violation_count": len(violations),
            },
        )

    def analyze(self, action: str = "analyze", token_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: analizar OAuth o generar token.

        Args:
            action: Acción ("analyze" o "generate")
            token_data: Datos de token (si action="generate")

        Returns:
            AnalysisResult con resultados
        """
        if action == "analyze":
            analysis = self.analyze_oauth()
            status = "warning" if analysis.violations else "success"
            return AnalysisResult(
                status=status,
                message=f"OAuth analysis completed: {analysis.active_tokens} active tokens",
                data=analysis.model_dump(),
            )

        elif action == "generate" and token_data:
            try:
                flow_type = token_data.get("flow_type", "authorization_code")
                scope = token_data.get("scope")
                expires_in = int(token_data.get("expires_in", 3600))

                token = self.generate_token(flow_type, scope, expires_in)
                return AnalysisResult(
                    status="success",
                    message="OAuth token generated successfully",
                    data=token.model_dump(),
                )
            except Exception as e:
                return AnalysisResult(
                    status="error",
                    message="OAuth token generation failed",
                    data={},
                    errors=[str(e)],
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
            return bool(data)  # access_token
        if isinstance(data, dict):
            return "flow_type" in data
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "supported_flows": ", ".join(self.supported_flows),
            "client_id": self.client_id if self.client_id else "not_set",
        }


# Alias para retrocompatibilidad
Digimon = OAuthmon

