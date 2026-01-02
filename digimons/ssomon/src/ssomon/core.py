"""
Core functionality for SSOmon (Mega)

SSOmon implementa Single Sign-On con SAML y OpenID Connect.
Misión: Goodbye, Dear Friend
Rol: sso-manager
"""

import logging
import secrets
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, SSOAnalysis, SSOSession

logger = logging.getLogger(__name__)


class SSOmon:
    """
    SSOmon - SSO Manager (Mega)

    Descripción:
        Implementa Single Sign-On con soporte SAML y OpenID Connect,
        gestión de sesiones y análisis de seguridad (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar SSOmon.

        Args:
            config: Diccionario de configuración opcional:
                - idp_url: URL del Identity Provider (opcional)
                - sp_entity_id: Entity ID del Service Provider (opcional)
                - enable_saml: Habilitar SAML (default: True)
                - enable_oidc: Habilitar OpenID Connect (default: True)
        """
        self.name = "SSOmon"
        self.mission = "Goodbye, Dear Friend"
        self.role = "sso-manager"
        self.config = config or {}

        self.idp_url = self.config.get("idp_url")
        self.sp_entity_id = self.config.get("sp_entity_id")
        self.enable_saml = bool(self.config.get("enable_saml", True))
        self.enable_oidc = bool(self.config.get("enable_oidc", True))

        # Simulación de almacenamiento de sesiones (en producción usar DB/Redis)
        self.sessions: Dict[str, Dict[str, Any]] = {}

        logger.info(
            "Initialized %s - %s (saml=%s, oidc=%s)",
            self.name,
            self.role,
            self.enable_saml,
            self.enable_oidc,
        )

    def create_sso_session(
        self, user_id: str, idp: str, protocol: str, attributes: Optional[Dict[str, Any]] = None
    ) -> SSOSession:
        """
        Crea una sesión SSO.

        Args:
            user_id: ID del usuario
            idp: Identity Provider
            protocol: Protocolo (SAML/OIDC)
            attributes: Atributos del usuario (opcional)

        Returns:
            SSOSession creada
        """
        # Verificar protocolo
        if protocol.upper() == "SAML" and not self.enable_saml:
            raise ValueError("SAML is not enabled")
        if protocol.upper() == "OIDC" and not self.enable_oidc:
            raise ValueError("OpenID Connect is not enabled")

        session_id = secrets.token_urlsafe(32)
        now = datetime.now()
        expires_at = now + timedelta(hours=8)  # SSO sessions típicamente duran más

        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "idp": idp,
            "protocol": protocol.upper(),
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "attributes": attributes or {},
            "expires_timestamp": expires_at.timestamp(),
        }
        self.sessions[session_id] = session_data

        return SSOSession(
            session_id=session_id,
            user_id=user_id,
            idp=idp,
            protocol=protocol.upper(),
            created_at=now.isoformat(),
            expires_at=expires_at.isoformat(),
            attributes=attributes or {},
        )

    def analyze_sso(self) -> SSOAnalysis:
        """
        Analiza las sesiones SSO activas.

        Returns:
            SSOAnalysis con resultados
        """
        now_timestamp = time.time()
        active = []
        sessions_by_protocol: Dict[str, int] = defaultdict(int)
        sessions_by_idp: Dict[str, int] = defaultdict(int)
        violations: List[str] = []

        for session_id, session_data in list(self.sessions.items()):
            expires_timestamp = session_data.get("expires_timestamp", 0)
            if now_timestamp > expires_timestamp:
                self.sessions.pop(session_id, None)
            else:
                active.append(session_id)
                protocol = session_data.get("protocol", "unknown")
                idp = session_data.get("idp", "unknown")
                sessions_by_protocol[protocol] += 1
                sessions_by_idp[idp] += 1

        # Verificar violaciones
        if not self.enable_saml and any(s.get("protocol") == "SAML" for s in self.sessions.values()):
            violations.append("SAML sessions found but SAML is disabled")

        return SSOAnalysis(
            total_sessions=len(self.sessions),
            active_sessions=len(active),
            sessions_by_protocol=dict(sessions_by_protocol),
            sessions_by_idp=dict(sessions_by_idp),
            violations=violations,
            analysis_summary={
                "idp_url": self.idp_url,
                "sp_entity_id": self.sp_entity_id,
                "violation_count": len(violations),
            },
        )

    def analyze(self, action: str = "analyze", session_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: analizar SSO o crear sesión.

        Args:
            action: Acción ("analyze" o "create")
            session_data: Datos de sesión (si action="create")

        Returns:
            AnalysisResult con resultados
        """
        if action == "analyze":
            analysis = self.analyze_sso()
            status = "warning" if analysis.violations else "success"
            return AnalysisResult(
                status=status,
                message=f"SSO analysis completed: {analysis.active_sessions} active sessions",
                data=analysis.model_dump(),
            )

        elif action == "create" and session_data:
            try:
                user_id = session_data.get("user_id", "")
                idp = session_data.get("idp", "default")
                protocol = session_data.get("protocol", "SAML")
                attributes = session_data.get("attributes")

                session = self.create_sso_session(user_id, idp, protocol, attributes)
                return AnalysisResult(
                    status="success",
                    message="SSO session created successfully",
                    data=session.model_dump(),
                )
            except Exception as e:
                return AnalysisResult(
                    status="error",
                    message="SSO session creation failed",
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
        if isinstance(data, dict):
            return "user_id" in data and "protocol" in data
        return True

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "enable_saml": str(self.enable_saml),
            "enable_oidc": str(self.enable_oidc),
        }


# Alias para retrocompatibilidad
Digimon = SSOmon

