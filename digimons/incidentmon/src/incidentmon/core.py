"""
Core functionality for Incidentmon (Mega)

Incidentmon automatiza respuesta a incidentes de seguridad.
Misión: The Gunslinger
Rol: incident-response
"""

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, IncidentAction, IncidentResponse

logger = logging.getLogger(__name__)


class Incidentmon:
    """
    Incidentmon - Incident Response (Mega)

    Descripción:
        Automatiza respuesta a incidentes de seguridad con contención,
        aislamiento y notificaciones (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Incidentmon.

        Args:
            config: Diccionario de configuración opcional:
                - auto_contain: Contención automática (default: False)
                - severity_threshold: Umbral de severidad (default: "medium")
                - notification_enabled: Notificaciones habilitadas (default: False)
        """
        self.name = "Incidentmon"
        self.mission = "The Gunslinger"
        self.role = "incident-response"
        self.config = config or {}

        self.auto_contain = bool(self.config.get("auto_contain", False))
        self.severity_threshold = self.config.get("severity_threshold", "medium")
        self.notification_enabled = bool(self.config.get("notification_enabled", False))

        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        self.severity_threshold_level = severity_order.get(self.severity_threshold.lower(), 2)

        logger.info(
            "Initialized %s - %s (auto_contain=%s, threshold=%s)",
            self.name,
            self.role,
            self.auto_contain,
            self.severity_threshold,
        )

    def respond_to_incident(
        self,
        incident_type: str,
        severity: str,
        target: str,
        description: Optional[str] = None,
    ) -> IncidentResponse:
        """
        Responde a un incidente de seguridad.

        Args:
            incident_type: Tipo de incidente
            severity: Severidad (critical/high/medium/low)
            target: Objetivo afectado
            description: Descripción opcional

        Returns:
            IncidentResponse con acciones tomadas
        """
        incident_id = str(uuid.uuid4())[:8]
        actions: List[IncidentAction] = []
        severity_level = {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(severity.lower(), 3)
        contained = False

        # Determinar si se debe actuar
        if severity_level <= self.severity_threshold_level:
            # Contención automática
            if self.auto_contain and severity_level <= 1:  # critical o high
                contain_action = IncidentAction(
                    action_type="contain",
                    target=target,
                    status="executed",
                    timestamp=datetime.now().isoformat(),
                )
                actions.append(contain_action)
                contained = True

            # Aislamiento
            if severity_level == 0:  # critical
                isolate_action = IncidentAction(
                    action_type="isolate",
                    target=target,
                    status="executed",
                    timestamp=datetime.now().isoformat(),
                )
                actions.append(isolate_action)

            # Notificación
            if self.notification_enabled:
                notify_action = IncidentAction(
                    action_type="notify",
                    target="security-team",
                    status="sent",
                    timestamp=datetime.now().isoformat(),
                )
                actions.append(notify_action)

        status = "contained" if contained else "monitored"

        return IncidentResponse(
            incident_id=incident_id,
            severity=severity,
            status=status,
            actions_taken=actions,
            contained=contained,
            response_summary={
                "incident_type": incident_type,
                "target": target,
                "description": description,
                "actions_count": len(actions),
            },
        )

    def analyze(
        self,
        incident_type: Optional[str] = None,
        severity: Optional[str] = None,
        target: Optional[str] = None,
        incidents: Optional[List[Dict[str, Any]]] = None,
    ) -> AnalysisResult:
        """
        Ejecuta respuesta: un incidente o múltiples.

        Args:
            incident_type: Tipo de incidente individual
            severity: Severidad individual
            target: Objetivo individual
            incidents: Lista de incidentes

        Returns:
            AnalysisResult con resultados
        """
        if incidents:
            responses = []
            total_contained = 0
            for inc in incidents:
                response = self.respond_to_incident(
                    incident_type=inc.get("incident_type", "unknown"),
                    severity=inc.get("severity", "low"),
                    target=inc.get("target", ""),
                    description=inc.get("description"),
                )
                responses.append(response.model_dump())
                if response.contained:
                    total_contained += 1

            return AnalysisResult(
                status="success",
                message=f"Processed {len(incidents)} incidents, {total_contained} contained",
                data={"responses": responses, "total_incidents": len(incidents), "contained_count": total_contained},
            )

        elif incident_type and severity and target:
            response = self.respond_to_incident(incident_type, severity, target)
            status = "warning" if response.contained else "success"
            return AnalysisResult(
                status=status,
                message=f"Incident response completed: {response.status}",
                data=response.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No incident data provided",
            data={},
            errors=["missing_input"],
        )

    def validate(self, data: Any) -> bool:
        """
        Valida datos de entrada.
        """
        if data is None:
            return False
        if isinstance(data, dict):
            return "severity" in data and "target" in data
        if isinstance(data, list):
            return all(isinstance(item, dict) and "severity" in item and "target" in item for item in data)
        return False

    def get_info(self) -> Dict[str, str]:
        """
        Obtener información del Digimon.
        """
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "auto_contain": str(self.auto_contain),
            "severity_threshold": self.severity_threshold,
        }


# Alias para retrocompatibilidad
Digimon = Incidentmon
