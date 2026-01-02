"""
Core functionality for Biometricmon (Mega)

Biometricmon procesa datos biométricos con verificación y liveness detection.
Misión: My Last Boy
Rol: biometric-handler
"""

import hashlib
import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, BiometricAnalysis, BiometricData

logger = logging.getLogger(__name__)


class Biometricmon:
    """
    Biometricmon - Biometric Handler (Mega)

    Descripción:
        Procesa datos biométricos con verificación de confianza,
        detección de liveness y gestión de templates (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Biometricmon.

        Args:
            config: Diccionario de configuración opcional:
                - supported_types: Tipos soportados (default: fingerprint, face, iris, voice)
                - min_confidence: Confianza mínima (default: 0.95)
                - enable_liveness: Habilitar liveness detection (default: True)
        """
        self.name = "Biometricmon"
        self.mission = "My Last Boy"
        self.role = "biometric-handler"
        self.config = config or {}

        self.supported_types = self.config.get("supported_types", ["fingerprint", "face", "iris", "voice"])
        self.min_confidence = float(self.config.get("min_confidence", 0.95))
        self.enable_liveness = bool(self.config.get("enable_liveness", True))

        # Simulación de almacenamiento de templates (en producción usar DB segura)
        self.templates: Dict[str, Dict[str, Any]] = {}

        logger.info(
            "Initialized %s - %s (types=%s, min_confidence=%.2f, liveness=%s)",
            self.name,
            self.role,
            len(self.supported_types),
            self.min_confidence,
            self.enable_liveness,
        )

    def _hash_template(self, template_data: str) -> str:
        """Hash de template biométrico."""
        return hashlib.sha256(template_data.encode("utf-8")).hexdigest()

    def register_biometric(
        self, user_id: str, biometric_type: str, template_data: str, confidence: float, liveness_verified: bool = False
    ) -> BiometricData:
        """
        Registra un template biométrico.

        Args:
            user_id: ID del usuario
            biometric_type: Tipo de biométrico
            template_data: Datos del template (simulado como string)
            confidence: Nivel de confianza (0.0-1.0)
            liveness_verified: Si liveness fue verificado

        Returns:
            BiometricData registrado
        """
        if biometric_type not in self.supported_types:
            raise ValueError(f"Unsupported biometric type: {biometric_type}")

        if confidence < self.min_confidence:
            raise ValueError(f"Confidence {confidence} below minimum {self.min_confidence}")

        template_hash = self._hash_template(template_data)
        biometric_id = f"{user_id}_{biometric_type}_{template_hash[:8]}"

        now = datetime.now().isoformat()

        template_record = {
            "biometric_id": biometric_id,
            "user_id": user_id,
            "biometric_type": biometric_type,
            "template_hash": template_hash,
            "confidence": confidence,
            "liveness_verified": liveness_verified,
            "created_at": now,
        }
        self.templates[biometric_id] = template_record

        return BiometricData(
            biometric_id=biometric_id,
            user_id=user_id,
            biometric_type=biometric_type,
            template_hash=template_hash,
            confidence=confidence,
            liveness_verified=liveness_verified,
            created_at=now,
        )

    def analyze_biometrics(self) -> BiometricAnalysis:
        """
        Analiza todos los templates biométricos.

        Returns:
            BiometricAnalysis con resultados
        """
        templates_by_type: Dict[str, int] = defaultdict(int)
        low_confidence = 0
        liveness_verified = 0
        violations: List[str] = []

        for template_data in self.templates.values():
            bio_type = template_data.get("biometric_type", "unknown")
            templates_by_type[bio_type] += 1

            confidence = template_data.get("confidence", 0.0)
            if confidence < self.min_confidence:
                low_confidence += 1
                violations.append(f"Template {template_data.get('biometric_id')} has low confidence: {confidence}")

            if template_data.get("liveness_verified", False):
                liveness_verified += 1

            if self.enable_liveness and not template_data.get("liveness_verified", False):
                violations.append(f"Template {template_data.get('biometric_id')} missing liveness verification")

        return BiometricAnalysis(
            total_templates=len(self.templates),
            templates_by_type=dict(templates_by_type),
            low_confidence=low_confidence,
            liveness_verified=liveness_verified,
            violations=violations[:50],
            analysis_summary={
                "min_confidence": self.min_confidence,
                "liveness_enabled": self.enable_liveness,
                "violation_count": len(violations),
            },
        )

    def analyze(self, action: str = "analyze", biometric_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: analizar templates o registrar nuevo.

        Args:
            action: Acción ("analyze" o "register")
            biometric_data: Datos biométricos (si action="register")

        Returns:
            AnalysisResult con resultados
        """
        if action == "analyze":
            analysis = self.analyze_biometrics()
            status = "warning" if analysis.violations else "success"
            return AnalysisResult(
                status=status,
                message=f"Biometric analysis completed: {analysis.total_templates} templates",
                data=analysis.model_dump(),
            )

        elif action == "register" and biometric_data:
            try:
                user_id = biometric_data.get("user_id", "")
                bio_type = biometric_data.get("biometric_type", "")
                template_data = biometric_data.get("template_data", "")
                confidence = float(biometric_data.get("confidence", 0.0))
                liveness = bool(biometric_data.get("liveness_verified", False))

                biometric = self.register_biometric(user_id, bio_type, template_data, confidence, liveness)
                return AnalysisResult(
                    status="success",
                    message="Biometric template registered successfully",
                    data=biometric.model_dump(),
                )
            except Exception as e:
                return AnalysisResult(
                    status="error",
                    message="Biometric registration failed",
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
            return "user_id" in data and "biometric_type" in data
        return True

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "supported_types": ", ".join(self.supported_types),
            "min_confidence": str(self.min_confidence),
        }


# Alias para retrocompatibilidad
Digimon = Biometricmon

