"""
Core functionality for Privilegemon (Mega)

Privilegemon audita elevación de privilegios con justificación y tracking.
Misión: Clemens Point
Rol: privilege-auditor
"""

import logging
import secrets
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, PrivilegeAudit, PrivilegeEvent

logger = logging.getLogger(__name__)


class Privilegemon:
    """
    Privilegemon - Privilege Auditor (Mega)

    Descripción:
        Audita elevación de privilegios con justificación requerida,
        tracking de eventos y límites de duración (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Privilegemon.

        Args:
            config: Diccionario de configuración opcional:
                - track_elevations: Rastrear elevaciones (default: True)
                - require_justification: Requerir justificación (default: True)
                - max_elevation_duration: Duración máxima en segundos (default: 3600)
        """
        self.name = "Privilegemon"
        self.mission = "Clemens Point"
        self.role = "privilege-auditor"
        self.config = config or {}

        self.track_elevations = bool(self.config.get("track_elevations", True))
        self.require_justification = bool(self.config.get("require_justification", True))
        self.max_elevation_duration = int(self.config.get("max_elevation_duration", 3600))

        # Simulación de almacenamiento de eventos (en producción usar DB)
        self.events: Dict[str, Dict[str, Any]] = {}

        logger.info(
            "Initialized %s - %s (require_justification=%s, max_duration=%ds)",
            self.name,
            self.role,
            self.require_justification,
            self.max_elevation_duration,
        )

    def request_elevation(
        self, user_id: str, requested_privilege: str, justification: Optional[str] = None
    ) -> PrivilegeEvent:
        """
        Solicita elevación de privilegios.

        Args:
            user_id: ID del usuario
            requested_privilege: Nivel de privilegio solicitado
            justification: Justificación (opcional si require_justification=False)

        Returns:
            PrivilegeEvent con resultado
        """
        event_id = secrets.token_urlsafe(16)
        now = datetime.now().isoformat()
        granted = True

        # Verificar justificación
        if self.require_justification and not justification:
            granted = False

        event_data = {
            "event_id": event_id,
            "user_id": user_id,
            "requested_privilege": requested_privilege,
            "justification": justification,
            "granted": granted,
            "timestamp": now,
            "duration": None,
        }

        if self.track_elevations:
            self.events[event_id] = event_data

        return PrivilegeEvent(
            event_id=event_id,
            user_id=user_id,
            requested_privilege=requested_privilege,
            justification=justification,
            granted=granted,
            timestamp=now,
            duration=None,
        )

    def audit_privileges(self) -> PrivilegeAudit:
        """
        Audita todos los eventos de privilegios.

        Returns:
            PrivilegeAudit con resultados
        """
        granted_count = 0
        denied_count = 0
        events_by_user: Dict[str, int] = defaultdict(int)
        violations: List[str] = []

        for event_data in self.events.values():
            user_id = event_data.get("user_id", "")
            events_by_user[user_id] += 1

            if event_data.get("granted", False):
                granted_count += 1

                # Verificar duración
                duration = event_data.get("duration")
                if duration and duration > self.max_elevation_duration:
                    violations.append(f"Event {event_data.get('event_id')} exceeded max duration")
            else:
                denied_count += 1

        return PrivilegeAudit(
            total_events=len(self.events),
            granted_count=granted_count,
            denied_count=denied_count,
            events_by_user=dict(events_by_user),
            violations=violations,
            audit_summary={
                "require_justification": self.require_justification,
                "max_duration": self.max_elevation_duration,
                "violation_count": len(violations),
            },
        )

    def analyze(self, action: str = "audit", elevation_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: auditar o solicitar elevación.

        Args:
            action: Acción ("audit" o "request")
            elevation_data: Datos de elevación (si action="request")

        Returns:
            AnalysisResult con resultados
        """
        if action == "audit":
            audit = self.audit_privileges()
            status = "warning" if audit.violations else "success"
            return AnalysisResult(
                status=status,
                message=f"Privilege audit completed: {audit.total_events} events",
                data=audit.model_dump(),
            )

        elif action == "request" and elevation_data:
            user_id = elevation_data.get("user_id", "")
            privilege = elevation_data.get("privilege", "")
            justification = elevation_data.get("justification")

            event = self.request_elevation(user_id, privilege, justification)
            status = "success" if event.granted else "warning"
            return AnalysisResult(
                status=status,
                message="Privilege elevation requested",
                data=event.model_dump(),
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
            return "user_id" in data and "privilege" in data
        return True

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "require_justification": str(self.require_justification),
            "max_elevation_duration": str(self.max_elevation_duration),
        }


# Alias para retrocompatibilidad
Digimon = Privilegemon

