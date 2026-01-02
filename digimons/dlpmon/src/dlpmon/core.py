"""
Core functionality for DLPmon (Mega)

DLPmon previene fuga de datos sensibles con detección avanzada y políticas.
Misión: The New Austin
Rol: data-loss-prevention
"""

import logging
import re
import secrets
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, DLPAnalysis, PolicyViolation

logger = logging.getLogger(__name__)


class DLPmon:
    """
    DLPmon - Data Loss Prevention (Mega)

    Descripción:
        Previene fuga de datos sensibles con detección avanzada basada en
        contenido, contexto y comportamiento, con políticas configurables (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar DLPmon.

        Args:
            config: Diccionario de configuración opcional:
                - detection_modes: Modos de detección (default: content, context, behavior)
                - sensitivity_level: Nivel de sensibilidad (default: "medium")
                - enable_blocking: Habilitar bloqueo automático (default: True)
                - alert_threshold: Umbral de alertas (default: 3)
        """
        self.name = "DLPmon"
        self.mission = "The New Austin"
        self.role = "data-loss-prevention"
        self.config = config or {}

        self.detection_modes = self.config.get("detection_modes", ["content", "context", "behavior"])
        self.sensitivity_level = self.config.get("sensitivity_level", "medium")
        self.enable_blocking = bool(self.config.get("enable_blocking", True))
        self.alert_threshold = int(self.config.get("alert_threshold", 3))

        # Políticas DLP predefinidas
        self.policies: Dict[str, Dict[str, Any]] = {
            "credit_card": {
                "pattern": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                "severity": "high",
                "enabled": True,
            },
            "ssn": {
                "pattern": r'\b\d{3}-\d{2}-\d{4}\b',
                "severity": "critical",
                "enabled": True,
            },
            "email": {
                "pattern": r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
                "severity": "medium",
                "enabled": True,
            },
            "ip_address": {
                "pattern": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                "severity": "low",
                "enabled": True,
            },
        }

        logger.info(
            "Initialized %s - %s (modes=%s, sensitivity=%s, blocking=%s)",
            self.name,
            self.role,
            len(self.detection_modes),
            self.sensitivity_level,
            self.enable_blocking,
        )

    def _check_sensitivity(self, severity: str) -> bool:
        """Verifica si la severidad cumple con el nivel de sensibilidad configurado."""
        levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        current_level = levels.get(self.sensitivity_level, 2)
        violation_level = levels.get(severity, 1)
        return violation_level >= current_level

    def scan_content(self, content: str, context: Optional[str] = None) -> List[PolicyViolation]:
        """
        Escanea contenido en busca de violaciones de políticas.

        Args:
            content: Contenido a escanear
            context: Contexto adicional (opcional)

        Returns:
            Lista de PolicyViolation detectadas
        """
        violations: List[PolicyViolation] = []

        for policy_name, policy_config in self.policies.items():
            if not policy_config.get("enabled", True):
                continue

            pattern = policy_config.get("pattern", "")
            severity = policy_config.get("severity", "medium")

            # Verificar nivel de sensibilidad
            if not self._check_sensitivity(severity):
                continue

            # Buscar coincidencias
            matches = re.finditer(pattern, content, re.IGNORECASE)

            for match in matches:
                violation_id = secrets.token_urlsafe(8)
                detected_data = match.group(0)

                violation = PolicyViolation(
                    violation_id=violation_id,
                    policy_name=policy_name,
                    violation_type="content",
                    severity=severity,
                    detected_data=detected_data[:50],  # Limitar longitud
                    location=f"position_{match.start()}",
                    timestamp=datetime.now().isoformat(),
                )
                violations.append(violation)

        return violations

    def analyze(self, content: Optional[str] = None, contents: Optional[List[str]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: un contenido o múltiples.

        Args:
            content: Contenido individual
            contents: Lista de contenidos

        Returns:
            AnalysisResult con resultados
        """
        if contents:
            all_violations: List[PolicyViolation] = []
            violations_by_severity: Dict[str, int] = defaultdict(int)
            violations_by_policy: Dict[str, int] = defaultdict(int)
            blocked = 0

            for idx, cont in enumerate(contents):
                violations = self.scan_content(cont, context=f"item_{idx}")

                for violation in violations:
                    all_violations.append(violation)
                    violations_by_severity[violation.severity] += 1
                    violations_by_policy[violation.policy_name] += 1

                    # Bloquear si está habilitado y es crítico
                    if self.enable_blocking and violation.severity == "critical":
                        blocked += 1

            status = "warning" if all_violations else "success"
            if blocked > 0:
                status = "error"

            return AnalysisResult(
                status=status,
                message=f"DLP analysis completed: {len(all_violations)} violations detected",
                data={
                    "total_scanned": len(contents),
                    "violations_detected": len(all_violations),
                    "violations_by_severity": dict(violations_by_severity),
                    "violations_by_policy": dict(violations_by_policy),
                    "violations": [v.model_dump() for v in all_violations[:100]],  # Limitar
                    "blocked_count": blocked,
                    "analysis_summary": {
                        "sensitivity_level": self.sensitivity_level,
                        "blocking_enabled": self.enable_blocking,
                    },
                },
            )

        elif content:
            violations = self.scan_content(content)
            blocked = sum(1 for v in violations if self.enable_blocking and v.severity == "critical")

            status = "warning" if violations else "success"
            if blocked > 0:
                status = "error"

            return AnalysisResult(
                status=status,
                message=f"DLP analysis completed: {len(violations)} violations detected",
                data={
                    "total_scanned": 1,
                    "violations_detected": len(violations),
                    "violations_by_severity": {v.severity: sum(1 for v2 in violations if v2.severity == v.severity) for v in violations},
                    "violations_by_policy": {v.policy_name: sum(1 for v2 in violations if v2.policy_name == v.policy_name) for v in violations},
                    "violations": [v.model_dump() for v in violations],
                    "blocked_count": blocked,
                },
            )

        return AnalysisResult(
            status="error",
            message="No content provided",
            data={},
            errors=["missing_input"],
        )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, str):
            return bool(data)
        if isinstance(data, list):
            return all(isinstance(item, str) and item for item in data)
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "detection_modes": ", ".join(self.detection_modes),
            "sensitivity_level": self.sensitivity_level,
        }


# Alias para retrocompatibilidad
Digimon = DLPmon

