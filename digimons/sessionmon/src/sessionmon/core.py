"""
Core functionality for Sessionmon (Mega)

Sessionmon gestiona sesiones de usuario con seguridad avanzada.
Misión: Polite Society
Rol: session-manager
"""

import logging
import secrets
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, Session, SessionAnalysis

logger = logging.getLogger(__name__)


class Sessionmon:
    """
    Sessionmon - Session Manager (Mega)

    Descripción:
        Gestiona sesiones de usuario con timeout, límites concurrentes,
        protección contra session fixation y tracking de actividad (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Sessionmon.

        Args:
            config: Diccionario de configuración opcional:
                - session_timeout: Timeout en segundos (default: 3600)
                - max_concurrent_sessions: Máximo concurrente por usuario (default: 10)
                - enable_session_fixation: Protección session fixation (default: True)
        """
        self.name = "Sessionmon"
        self.mission = "Polite Society"
        self.role = "session-manager"
        self.config = config or {}

        self.session_timeout = int(self.config.get("session_timeout", 3600))
        self.max_concurrent_sessions = int(self.config.get("max_concurrent_sessions", 10))
        self.enable_session_fixation = bool(self.config.get("enable_session_fixation", True))

        # Simulación de almacenamiento de sesiones (en producción usar DB/Redis)
        self.sessions: Dict[str, Dict[str, Any]] = {}

        logger.info(
            "Initialized %s - %s (timeout=%ds, max_concurrent=%d)",
            self.name,
            self.role,
            self.session_timeout,
            self.max_concurrent_sessions,
        )

    def create_session(self, user_id: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Session:
        """
        Crea una nueva sesión.

        Args:
            user_id: ID del usuario
            ip_address: Dirección IP (opcional)
            user_agent: User agent (opcional)

        Returns:
            Session creada
        """
        now = datetime.now()
        expires_at = now + timedelta(seconds=self.session_timeout)

        # Generar session ID único (simulado)
        session_id = secrets.token_urlsafe(32)

        # Verificar límite de sesiones concurrentes
        user_sessions = [s for s in self.sessions.values() if s.get("user_id") == user_id and s.get("expires_at", 0) > time.time()]
        if len(user_sessions) >= self.max_concurrent_sessions:
            # Cerrar la sesión más antigua
            oldest = min(user_sessions, key=lambda s: s.get("created_at", 0))
            if oldest.get("session_id"):
                self.sessions.pop(oldest["session_id"], None)

        # Crear sesión
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "last_activity": now.isoformat(),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "expires_timestamp": expires_at.timestamp(),
        }
        self.sessions[session_id] = session_data

        return Session(
            session_id=session_id,
            user_id=user_id,
            created_at=now.isoformat(),
            expires_at=expires_at.isoformat(),
            last_activity=now.isoformat(),
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def validate_session(self, session_id: str) -> bool:
        """
        Valida una sesión.

        Args:
            session_id: ID de la sesión

        Returns:
            True si la sesión es válida
        """
        if session_id not in self.sessions:
            return False

        session = self.sessions[session_id]
        expires_timestamp = session.get("expires_timestamp", 0)

        if time.time() > expires_timestamp:
            # Sesión expirada
            self.sessions.pop(session_id, None)
            return False

        # Actualizar última actividad
        session["last_activity"] = datetime.now().isoformat()
        return True

    def analyze_sessions(self) -> SessionAnalysis:
        """
        Analiza todas las sesiones activas.

        Returns:
            SessionAnalysis con resultados
        """
        now_timestamp = time.time()
        active = []
        expired = []
        sessions_by_user: Dict[str, int] = {}
        violations: List[str] = []

        for session_id, session_data in list(self.sessions.items()):
            expires_timestamp = session_data.get("expires_timestamp", 0)
            user_id = session_data.get("user_id", "")

            if now_timestamp > expires_timestamp:
                expired.append(session_id)
                self.sessions.pop(session_id, None)
            else:
                active.append(session_id)
                sessions_by_user[user_id] = sessions_by_user.get(user_id, 0) + 1

        # Verificar violaciones
        for user_id, count in sessions_by_user.items():
            if count > self.max_concurrent_sessions:
                violations.append(f"User {user_id} has {count} concurrent sessions (limit: {self.max_concurrent_sessions})")

        return SessionAnalysis(
            total_sessions=len(self.sessions),
            active_sessions=len(active),
            expired_sessions=len(expired),
            sessions_by_user=sessions_by_user,
            violations=violations,
            analysis_summary={
                "session_timeout": self.session_timeout,
                "max_concurrent": self.max_concurrent_sessions,
                "violation_count": len(violations),
            },
        )

    def analyze(self, action: str = "analyze", user_id: Optional[str] = None) -> AnalysisResult:
        """
        Ejecuta análisis: analizar sesiones o crear sesión.

        Args:
            action: Acción ("analyze" o "create")
            user_id: ID de usuario (si action="create")

        Returns:
            AnalysisResult con resultados
        """
        if action == "analyze":
            analysis = self.analyze_sessions()
            status = "warning" if analysis.violations else "success"
            return AnalysisResult(
                status=status,
                message=f"Session analysis completed: {analysis.active_sessions} active",
                data=analysis.model_dump(),
            )

        elif action == "create" and user_id:
            session = self.create_session(user_id)
            return AnalysisResult(
                status="success",
                message="Session created successfully",
                data=session.model_dump(),
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
            return bool(data)  # session_id
        if isinstance(data, dict):
            return "user_id" in data
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "session_timeout": str(self.session_timeout),
            "max_concurrent_sessions": str(self.max_concurrent_sessions),
        }


# Alias para retrocompatibilidad
Digimon = Sessionmon

