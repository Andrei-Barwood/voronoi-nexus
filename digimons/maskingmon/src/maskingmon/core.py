"""
Core functionality for Maskingmon (Mega)

Maskingmon enmascara datos sensibles en logs preservando formato.
Misión: Good, Honest Snake Oil
Rol: data-masker
"""

import logging
import re
import secrets
from collections import defaultdict
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, MaskingRecord, MaskingResult

logger = logging.getLogger(__name__)


class Maskingmon:
    """
    Maskingmon - Data Masker (Mega)

    Descripción:
        Enmascara datos sensibles en logs preservando formato y contexto,
        con soporte para múltiples tipos de PII (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Maskingmon.

        Args:
            config: Diccionario de configuración opcional:
                - mask_character: Carácter para enmascarar (default: "*")
                - mask_length: Longitud fija de máscara (None = preservar) (default: None)
                - preserve_format: Preservar formato (default: True)
                - pii_types: Tipos de PII a enmascarar (default: email, phone, credit_card, ssn, ip)
                - log_context: Incluir contexto en logs (default: True)
        """
        self.name = "Maskingmon"
        self.mission = "Good, Honest Snake Oil"
        self.role = "data-masker"
        self.config = config or {}

        self.mask_character = self.config.get("mask_character", "*")
        self.mask_length = self.config.get("mask_length")
        self.preserve_format = bool(self.config.get("preserve_format", True))
        self.pii_types = self.config.get("pii_types", ["email", "phone", "credit_card", "ssn", "ip"])
        self.log_context = bool(self.config.get("log_context", True))

        # Patrones PII
        self.patterns: Dict[str, Dict[str, Any]] = {
            "email": {
                "pattern": r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
                "mask_func": self._mask_email,
            },
            "phone": {
                "pattern": r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
                "mask_func": self._mask_phone,
            },
            "credit_card": {
                "pattern": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                "mask_func": self._mask_credit_card,
            },
            "ssn": {
                "pattern": r'\b\d{3}-\d{2}-\d{4}\b',
                "mask_func": self._mask_ssn,
            },
            "ip": {
                "pattern": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                "mask_func": self._mask_ip,
            },
        }

        logger.info(
            "Initialized %s - %s (mask_char=%s, pii_types=%s)",
            self.name,
            self.role,
            self.mask_character,
            len(self.pii_types),
        )

    def _mask_email(self, value: str) -> str:
        """Enmascara email."""
        if "@" not in value:
            return value

        local, domain = value.split("@", 1)
        if self.mask_length:
            masked_local = self.mask_character * self.mask_length
        else:
            masked_local = self.mask_character * min(len(local), 4)

        return f"{masked_local}@{domain}"

    def _mask_phone(self, value: str) -> str:
        """Enmascara teléfono."""
        digits_only = re.sub(r"[^\d]", "", value)
        if self.mask_length:
            return self.mask_character * self.mask_length
        if self.preserve_format:
            if "-" in value:
                return f"***-***-{digits_only[-4:]}"
            elif "(" in value:
                return f"***-***-{digits_only[-4:]}"
        return f"***-***-{digits_only[-4:]}"

    def _mask_credit_card(self, value: str) -> str:
        """Enmascara tarjeta de crédito."""
        if self.preserve_format:
            if "-" in value:
                return f"****-****-****-{value[-4:]}"
            elif " " in value:
                return f"**** **** **** {value[-4:]}"
        return f"****{value[-4:]}"

    def _mask_ssn(self, value: str) -> str:
        """Enmascara SSN."""
        if self.preserve_format:
            return f"***-**-{value[-4:]}"
        return "***-**-****"

    def _mask_ip(self, value: str) -> str:
        """Enmascara IP."""
        if self.mask_length:
            return self.mask_character * self.mask_length
        parts = value.split(".")
        return f"{self.mask_character * 3}.{self.mask_character * 3}.{self.mask_character * 3}.{parts[-1]}"

    def _apply_masking(self, match: re.Match, pii_type: str) -> str:
        """
        Aplica enmascarado según tipo de PII.

        Args:
            match: Match object de regex
            pii_type: Tipo de PII

        Returns:
            String enmascarado
        """
        if pii_type not in self.patterns:
            return match.group(0)

        mask_func = self.patterns[pii_type].get("mask_func")
        if mask_func:
            return mask_func(match.group(0))

        # Fallback: enmascarado genérico
        value = match.group(0)
        if self.mask_length:
            return self.mask_character * self.mask_length
        return self.mask_character * len(value)

    def mask_text(self, text: str) -> MaskingResult:
        """
        Enmascara PII de un texto.

        Args:
            text: Texto a enmascarar

        Returns:
            MaskingResult con resultados
        """
        masked_text = text
        masking_records: List[MaskingRecord] = []
        masked_by_type: Dict[str, int] = defaultdict(int)

        for pii_type in self.pii_types:
            if pii_type not in self.patterns:
                continue

            pattern = self.patterns[pii_type]["pattern"]
            matches = list(re.finditer(pattern, masked_text, re.IGNORECASE))

            # Enmascarar de atrás hacia adelante para preservar índices
            for match in reversed(matches):
                start, end = match.span()
                original_value = match.group(0)
                masked_value = self._apply_masking(match, pii_type)

                # Crear registro
                record = MaskingRecord(
                    record_id=secrets.token_urlsafe(8),
                    pii_type=pii_type,
                    original_value=original_value[:30],  # Truncar
                    masked_value=masked_value,
                    position=start,
                    preserve_format=self.preserve_format,
                )
                masking_records.append(record)

                # Aplicar enmascarado
                masked_text = masked_text[:start] + masked_value + masked_text[end:]
                masked_by_type[pii_type] += 1

        total_masked = sum(masked_by_type.values())

        return MaskingResult(
            original_text=text,
            masked_text=masked_text,
            total_masked=total_masked,
            masked_by_type=dict(masked_by_type),
            masking_records=masking_records,
            statistics={
                "mask_character": self.mask_character,
                "preserve_format": self.preserve_format,
                "pii_types_enabled": self.pii_types,
            },
        )

    def analyze(self, text: Optional[str] = None, texts: Optional[List[str]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: enmascarar texto(s).

        Args:
            text: Texto individual
            texts: Lista de textos

        Returns:
            AnalysisResult con resultados
        """
        if texts:
            results = []
            total_masked = 0
            total_by_type: Dict[str, int] = defaultdict(int)

            for txt in texts:
                result = self.mask_text(txt)
                results.append(result.model_dump())
                total_masked += result.total_masked

                for pii_type, count in result.masked_by_type.items():
                    total_by_type[pii_type] += count

            return AnalysisResult(
                status="success",
                message=f"Masked PII from {len(texts)} texts: {total_masked} items masked total",
                data={
                    "results": results,
                    "total_masked": total_masked,
                    "total_by_type": dict(total_by_type),
                },
            )

        elif text:
            result = self.mask_text(text)
            return AnalysisResult(
                status="success",
                message=f"Masked {result.total_masked} PII items",
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
            "mask_character": self.mask_character,
            "pii_types": ", ".join(self.pii_types),
        }


# Alias para retrocompatibilidad
Digimon = Maskingmon

