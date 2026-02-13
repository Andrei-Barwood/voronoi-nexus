"""
Core functionality for VoronoiReclaim (Production)

VoronoiReclaim - Ransomware Detector
Misión: Revenge
Rol: ransomware-detector
"""

import logging
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, DetectionFinding, DetectionReport

logger = logging.getLogger(__name__)


class VoronoiReclaim:
    """
    VoronoiReclaim - Ransomware Detector (Production)

    Descripción:
        Detecta patrones de cifrado masivo y actividad tipica de ransomware.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar VoronoiReclaim.

        Args:
            config: Diccionario de configuración opcional:
                - severity_threshold: Umbral de severidad (default: "medium")
                - confidence_threshold: Umbral de confianza (default: 0.7)
                - enable_enrichment: Habilita contexto adicional (default: True)
        """
        self.name = "Voronoi Reclaim"
        self.mission = "Revenge"
        self.role = "ransomware-detector"
        self.config = config or {}

        self.severity_threshold = self.config.get("severity_threshold", "medium")
        self.confidence_threshold = float(self.config.get("confidence_threshold", 0.7))
        self.enable_enrichment = bool(self.config.get("enable_enrichment", True))

        self._severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        self._severity_threshold_rank = self._severity_rank.get(self.severity_threshold.lower(), 2)
        self._risk_signals = {
            "critical": ["critical", "mass", "deleted", "beaconing", "persistence"],
            "high": ["suspicious", "anomaly", "evasion", "packed", "callback"],
            "medium": ["warning", "irregular", "mismatch", "cluster", "entropy"],
        }

        logger.info(
            "Initialized %s - %s (threshold=%s, confidence=%.2f)",
            self.name,
            self.role,
            self.severity_threshold,
            self.confidence_threshold,
        )

    def _normalize_signal(self, key: str, value: Any) -> float:
        """
        Normaliza una señal a un score [0, 1].
        """
        if isinstance(value, bool):
            return 1.0 if value else 0.0
        if isinstance(value, (int, float)):
            if value <= 1.0:
                return float(value)
            return min(float(value) / 100.0, 1.0)
        if isinstance(value, str):
            return 1.0 if value.lower() in ("true", "yes", "high", "critical") else 0.3
        return 0.0

    def detect_ransomware(self, event_data: Dict[str, Any]) -> DetectionReport:
        """
        Ejecuta el método especializado del producto.
        """
        findings: List[DetectionFinding] = []
        total_checks = len(event_data)

        for key, value in event_data.items():
            score = self._normalize_signal(key, value)
            key_l = key.lower()

            if score < self.confidence_threshold:
                continue

            severity = "medium"
            if any(token in key_l for token in self._risk_signals["critical"]):
                severity = "critical"
            elif any(token in key_l for token in self._risk_signals["high"]):
                severity = "high"
            elif any(token in key_l for token in self._risk_signals["medium"]):
                severity = "medium"
            else:
                severity = "low"

            if self._severity_rank[severity] > self._severity_threshold_rank:
                continue

            findings.append(
                DetectionFinding(
                    indicator=key,
                    category=self.role,
                    severity=severity,
                    confidence=round(score, 2),
                    recommendation="Escalar al SOC y activar playbook de contención"
                    if severity in ("critical", "high")
                    else "Monitorear y correlacionar con telemetría adicional",
                )
            )

        alerts_count = len(findings)
        return DetectionReport(
            total_checks=total_checks,
            alerts_count=alerts_count,
            findings=findings,
            summary={
                "engine": self.name,
                "role": self.role,
                "enrichment_enabled": self.enable_enrichment,
                "severity_threshold": self.severity_threshold,
                "confidence_threshold": self.confidence_threshold,
            },
        )

    def analyze(self, event_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta el análisis principal del módulo.
        """
        if not event_data:
            return AnalysisResult(
                status="error",
                message="No input data provided",
                data={},
                errors=["missing_input"],
            )

        report = self.detect_ransomware(event_data)
        status = "warning" if report.alerts_count > 0 else "success"
        return AnalysisResult(
            status=status,
            message=f"Analysis completed: {report.alerts_count} alerts generated",
            data=report.model_dump(),
        )

    def validate(self, data: Any) -> bool:
        """
        Valida datos de entrada.
        """
        if data is None:
            return False
        if isinstance(data, dict):
            return len(data) > 0
        return False

    def get_info(self) -> Dict[str, str]:
        """
        Obtener información del módulo.
        """
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Production",
            "severity_threshold": self.severity_threshold,
            "confidence_threshold": str(self.confidence_threshold),
        }


# Alias para retrocompatibilidad
módulo = VoronoiReclaim
