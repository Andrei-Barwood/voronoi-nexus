"""
Core functionality for Bandidmon (Mega)

Bandidmon protege datos sensibles redactando información personal (PII) avanzada.
Misión: Outlaws from the West
Rol: data-protector
"""

import logging
import re
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, DigimonConfig, RedactionResult

logger = logging.getLogger(__name__)


class Bandidmon:
    """
    Bandidmon - Data Protector (Mega)

    Descripción:
        Protege datos sensibles con detección avanzada de PII (emails, tarjetas,
        SSN, IPs, teléfonos) y redacción configurable (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Bandidmon.

        Args:
            config: Diccionario de configuración opcional:
                - redaction_mode: Modo de redacción (mask/tokenize/remove) (default: "mask")
                - preserve_format: Preservar formato (default: True)
                - enable_ip_detection: Detectar IPs (default: True)
                - enable_ssn_detection: Detectar SSN (default: True)
                - enable_phone_detection: Detectar teléfonos (default: True)
        """
        self.name = "Bandidmon"
        self.mission = "Outlaws from the West"
        self.role = "data-protector"
        self.config = config or {}

        self.redaction_mode = self.config.get("redaction_mode", "mask")
        self.preserve_format = bool(self.config.get("preserve_format", True))
        self.enable_ip_detection = bool(self.config.get("enable_ip_detection", True))
        self.enable_ssn_detection = bool(self.config.get("enable_ssn_detection", True))
        self.enable_phone_detection = bool(self.config.get("enable_phone_detection", True))

        # Patrones regex avanzados para PII (2025-2026)
        self.patterns: Dict[str, Dict[str, Any]] = {
            "email": {
                "pattern": r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
                "enabled": True,
                "label": "Email",
            },
            "credit_card": {
                "pattern": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                "enabled": True,
                "label": "Credit Card",
            },
            "ip_address": {
                "pattern": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                "enabled": self.enable_ip_detection,
                "label": "IP Address",
            },
            "ssn": {
                "pattern": r'\b\d{3}-\d{2}-\d{4}\b',
                "enabled": self.enable_ssn_detection,
                "label": "SSN",
            },
            "phone": {
                "pattern": r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
                "enabled": self.enable_phone_detection,
                "label": "Phone Number",
            },
        }

        logger.info(
            "Initialized %s - %s (mode=%s, ip=%s, ssn=%s, phone=%s)",
            self.name,
            self.role,
            self.redaction_mode,
            self.enable_ip_detection,
            self.enable_ssn_detection,
            self.enable_phone_detection,
        )

    def _redact_match(self, match: re.Match, pii_type: str) -> str:
        """
        Redacta un match según el modo configurado.

        Args:
            match: Match object de regex
            pii_type: Tipo de PII

        Returns:
            String redactado
        """
        original = match.group(0)

        if self.redaction_mode == "remove":
            return ""

        elif self.redaction_mode == "tokenize":
            return f"[{pii_type.upper()}_TOKEN]"

        else:  # mask (default)
            if self.preserve_format:
                # Preservar formato básico
                if pii_type == "email":
                    return "[REDACTED_EMAIL]"
                elif pii_type == "credit_card":
                    return "****-****-****-****"
                elif pii_type == "ssn":
                    return "***-**-****"
                elif pii_type == "phone":
                    return "(***) ***-****"
                else:
                    return "*" * min(len(original), 20)
            else:
                return f"[REDACTED:{pii_type.upper()}]"

    def redact_pii(self, text: str) -> RedactionResult:
        """
        Redacta PII de un texto.

        Args:
            text: Texto a redactar

        Returns:
            RedactionResult con resultados
        """
        safe_text = text
        redacted_items: List[Dict[str, Any]] = []
        statistics: Dict[str, int] = {}

        for pii_type, config in self.patterns.items():
            if not config["enabled"]:
                continue

            pattern = config["pattern"]
            label = config["label"]

            # Encontrar todas las coincidencias
            matches = list(re.finditer(pattern, safe_text))

            if matches:
                statistics[label] = len(matches)

                # Redactar de atrás hacia adelante para preservar índices
                for match in reversed(matches):
                    start, end = match.span()
                    redacted_value = self._redact_match(match, pii_type)
                    safe_text = safe_text[:start] + redacted_value + safe_text[end:]

                    redacted_items.append(
                        {
                            "type": pii_type,
                            "label": label,
                            "position": start,
                            "length": end - start,
                        }
                    )

        total_redacted = sum(statistics.values())

        return RedactionResult(
            original_text=text,
            safe_text=safe_text,
            redacted_items=redacted_items,
            statistics=statistics,
            total_redacted=total_redacted,
        )

    def analyze(self, text: Optional[str] = None, texts: Optional[List[str]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: un texto o múltiples.

        Args:
            text: Texto individual
            texts: Lista de textos

        Returns:
            AnalysisResult con resultados
        """
        if texts:
            results = []
            total_stats: Dict[str, int] = {}
            total_redacted = 0

            for txt in texts:
                result = self.redact_pii(txt)
                results.append(result.model_dump())

                # Acumular estadísticas
                for label, count in result.statistics.items():
                    total_stats[label] = total_stats.get(label, 0) + count
                total_redacted += result.total_redacted

            status = "success"
            return AnalysisResult(
                status=status,
                message=f"Redacted PII from {len(texts)} texts: {total_redacted} items total",
                data={"results": results, "total_statistics": total_stats, "total_redacted": total_redacted},
            )

        elif text:
            result = self.redact_pii(text)
            status = "success"
            return AnalysisResult(
                status=status,
                message=f"Redacted {result.total_redacted} PII items",
                data=result.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No text provided",
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
        enabled_types = [config["label"] for config in self.patterns.values() if config["enabled"]]
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "redaction_mode": self.redaction_mode,
            "supported_types": ", ".join(enabled_types),
        }


# Alias para retrocompatibilidad
Digimon = Bandidmon
