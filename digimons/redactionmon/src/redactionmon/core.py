"""
Core functionality for Redactionmon (Mega)

Redactionmon redacta información PII automáticamente con múltiples estilos.
Misión: Outlaws from the West
Rol: data-redactor
"""

import logging
import re
import secrets
from collections import defaultdict
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, RedactionRecord, RedactionResult

logger = logging.getLogger(__name__)


class Redactionmon:
    """
    Redactionmon - Data Redactor (Mega)

    Descripción:
        Redacta información PII automáticamente con múltiples estilos,
        preservación de estructura y tracking detallado (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Redactionmon.

        Args:
            config: Diccionario de configuración opcional:
                - redaction_style: Estilo de redacción (mask/tokenize/remove) (default: "mask")
                - preserve_structure: Preservar estructura (default: True)
                - pii_types: Tipos de PII a redactar (default: email, phone, ssn, credit_card, ip)
        """
        self.name = "Redactionmon"
        self.mission = "Outlaws from the West"
        self.role = "data-redactor"
        self.config = config or {}

        self.redaction_style = self.config.get("redaction_style", "mask")
        self.preserve_structure = bool(self.config.get("preserve_structure", True))
        self.pii_types = self.config.get("pii_types", ["email", "phone", "ssn", "credit_card", "ip"])

        # Patrones PII
        self.patterns: Dict[str, Dict[str, Any]] = {
            "email": {
                "pattern": r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
                "mask": "[EMAIL_REDACTED]",
                "token": "[EMAIL_TOKEN]",
            },
            "phone": {
                "pattern": r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
                "mask": "[PHONE_REDACTED]",
                "token": "[PHONE_TOKEN]",
            },
            "ssn": {
                "pattern": r'\b\d{3}-\d{2}-\d{4}\b',
                "mask": "***-**-****",
                "token": "[SSN_TOKEN]",
            },
            "credit_card": {
                "pattern": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                "mask": "****-****-****-****",
                "token": "[CARD_TOKEN]",
            },
            "ip": {
                "pattern": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                "mask": "[IP_REDACTED]",
                "token": "[IP_TOKEN]",
            },
        }

        logger.info(
            "Initialized %s - %s (style=%s, pii_types=%s)",
            self.name,
            self.role,
            self.redaction_style,
            len(self.pii_types),
        )

    def _apply_redaction(self, match: re.Match, pii_type: str) -> str:
        """
        Aplica redacción según el estilo configurado.

        Args:
            match: Match object de regex
            pii_type: Tipo de PII

        Returns:
            String redactado
        """
        if pii_type not in self.patterns:
            return match.group(0)

        pattern_config = self.patterns[pii_type]

        if self.redaction_style == "remove":
            return ""

        elif self.redaction_style == "tokenize":
            return pattern_config.get("token", f"[{pii_type.upper()}_TOKEN]")

        else:  # mask (default)
            return pattern_config.get("mask", "*" * len(match.group(0)))

    def redact_text(self, text: str) -> RedactionResult:
        """
        Redacta PII de un texto.

        Args:
            text: Texto a redactar

        Returns:
            RedactionResult con resultados
        """
        redacted_text = text
        redaction_records: List[RedactionRecord] = []
        redactions_by_type: Dict[str, int] = defaultdict(int)

        for pii_type in self.pii_types:
            if pii_type not in self.patterns:
                continue

            pattern = self.patterns[pii_type]["pattern"]
            matches = list(re.finditer(pattern, redacted_text, re.IGNORECASE))

            # Redactar de atrás hacia adelante para preservar índices
            for match in reversed(matches):
                start, end = match.span()
                original_value = match.group(0)
                redacted_value = self._apply_redaction(match, pii_type)

                # Crear registro
                record = RedactionRecord(
                    record_id=secrets.token_urlsafe(8),
                    pii_type=pii_type,
                    original_value=original_value[:30],  # Truncar
                    redacted_value=redacted_value,
                    position=start,
                    confidence=0.95,  # Simulado
                )
                redaction_records.append(record)

                # Aplicar redacción
                redacted_text = redacted_text[:start] + redacted_value + redacted_text[end:]
                redactions_by_type[pii_type] += 1

        total_redactions = sum(redactions_by_type.values())

        return RedactionResult(
            original_text=text,
            redacted_text=redacted_text,
            total_redactions=total_redactions,
            redactions_by_type=dict(redactions_by_type),
            redaction_records=redaction_records,
            statistics={
                "redaction_style": self.redaction_style,
                "preserve_structure": self.preserve_structure,
                "pii_types_enabled": self.pii_types,
            },
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
            total_redactions = 0
            total_by_type: Dict[str, int] = defaultdict(int)

            for txt in texts:
                result = self.redact_text(txt)
                results.append(result.model_dump())
                total_redactions += result.total_redactions

                for pii_type, count in result.redactions_by_type.items():
                    total_by_type[pii_type] += count

            return AnalysisResult(
                status="success",
                message=f"Redacted PII from {len(texts)} texts: {total_redactions} redactions total",
                data={
                    "results": results,
                    "total_redactions": total_redactions,
                    "total_by_type": dict(total_by_type),
                },
            )

        elif text:
            result = self.redact_text(text)
            return AnalysisResult(
                status="success",
                message=f"Redacted {result.total_redactions} PII items",
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
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "redaction_style": self.redaction_style,
            "pii_types": ", ".join(self.pii_types),
        }


# Alias para retrocompatibilidad
Digimon = Redactionmon

