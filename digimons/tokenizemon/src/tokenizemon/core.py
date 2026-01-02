"""
Core functionality for Tokenizemon (Mega)

Tokenizemon tokeniza datos sensibles con múltiples formatos y reversibilidad.
Misión: Paradise Mercifully Departed
Rol: tokenization-engine
"""

import logging
import re
import secrets
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, DetokenizationResult, TokenizationRecord, TokenizationResult

logger = logging.getLogger(__name__)


class Tokenizemon:
    """
    Tokenizemon - Tokenization Engine (Mega)

    Descripción:
        Tokeniza datos sensibles con múltiples formatos (UUID, random, sequential),
        preservación de formato y detokenización reversible (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Tokenizemon.

        Args:
            config: Diccionario de configuración opcional:
                - token_format: Formato de token (uuid/random/sequential) (default: "uuid")
                - preserve_format: Preservar formato (default: True)
                - token_mapping_backend: Backend de mapeo (default: "memory")
                - enable_detokenization: Habilitar detokenización (default: True)
                - token_prefix: Prefijo opcional para tokens (default: None)
        """
        self.name = "Tokenizemon"
        self.mission = "Paradise Mercifully Departed"
        self.role = "tokenization-engine"
        self.config = config or {}

        self.token_format = self.config.get("token_format", "uuid")
        self.preserve_format = bool(self.config.get("preserve_format", True))
        self.token_mapping_backend = self.config.get("token_mapping_backend", "memory")
        self.enable_detokenization = bool(self.config.get("enable_detokenization", True))
        self.token_prefix = self.config.get("token_prefix")

        # Mapeo token -> valor original (si detokenización está habilitada)
        self.token_mapping: Dict[str, str] = {}
        self.sequential_counter = 0

        logger.info(
            "Initialized %s - %s (format=%s, detokenization=%s)",
            self.name,
            self.role,
            self.token_format,
            self.enable_detokenization,
        )

    def _generate_token(self, original_value: str = "") -> str:
        """
        Genera un token según el formato configurado.

        Args:
            original_value: Valor original (para contexto)

        Returns:
            Token generado
        """
        if self.token_format == "uuid":
            token = str(uuid.uuid4())
        elif self.token_format == "random":
            token = secrets.token_urlsafe(16)
        elif self.token_format == "sequential":
            self.sequential_counter += 1
            token = f"SEQ_{self.sequential_counter:08d}"
        else:
            token = secrets.token_urlsafe(16)  # Fallback

        if self.token_prefix:
            token = f"{self.token_prefix}_{token}"

        return token

    def _detect_data_type(self, value: str) -> str:
        """Detecta el tipo de dato."""
        if "@" in value:
            return "email"
        elif re.match(r"^\d{3}-\d{2}-\d{4}$", value):
            return "ssn"
        elif re.match(r"^\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}$", value.replace(" ", "").replace("-", "")):
            return "credit_card"
        elif re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value):
            return "ip"
        elif re.match(r"^\+?[\d\s\-\(\)]+$", value):
            return "phone"
        else:
            return "generic"

    def tokenize_value(self, value: str) -> str:
        """
        Tokeniza un valor individual.

        Args:
            value: Valor a tokenizar

        Returns:
            Token generado
        """
        token = self._generate_token(value)

        if self.enable_detokenization:
            self.token_mapping[token] = value

        return token

    def tokenize_text(self, text: str, pii_patterns: Optional[Dict[str, str]] = None) -> TokenizationResult:
        """
        Tokeniza PII en un texto.

        Args:
            text: Texto a tokenizar
            pii_patterns: Patrones PII personalizados (opcional)

        Returns:
            TokenizationResult con resultados
        """
        if pii_patterns is None:
            pii_patterns = {
                "email": r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
                "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
                "credit_card": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                "ip": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                "phone": r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            }

        tokenized_text = text
        records: List[TokenizationRecord] = []
        tokens_by_type: Dict[str, int] = defaultdict(int)

        for pii_type, pattern in pii_patterns.items():
            matches = list(re.finditer(pattern, tokenized_text, re.IGNORECASE))

            # Tokenizar de atrás hacia adelante para preservar índices
            for match in reversed(matches):
                start, end = match.span()
                original_value = match.group(0)
                token = self.tokenize_value(original_value)

                # Crear registro
                record = TokenizationRecord(
                    record_id=secrets.token_urlsafe(8),
                    original_value=original_value[:30],  # Truncar
                    token=token,
                    token_type=pii_type,
                    created_at=datetime.now().isoformat(),
                    reversible=self.enable_detokenization,
                )
                records.append(record)

                # Aplicar tokenización
                tokenized_text = tokenized_text[:start] + token + tokenized_text[end:]
                tokens_by_type[pii_type] += 1

        total_tokens = sum(tokens_by_type.values())

        return TokenizationResult(
            original_data=text,
            tokenized_data=tokenized_text,
            total_tokens=total_tokens,
            tokens_by_type=dict(tokens_by_type),
            tokenization_records=records,
            statistics={
                "token_format": self.token_format,
                "preserve_format": self.preserve_format,
                "detokenization_enabled": self.enable_detokenization,
            },
        )

    def detokenize(self, token: str) -> DetokenizationResult:
        """
        Detokeniza un token.

        Args:
            token: Token a detokenizar

        Returns:
            DetokenizationResult con resultado
        """
        if not self.enable_detokenization:
            return DetokenizationResult(
                token=token,
                original_value=None,
                found=False,
                message="Detokenization is disabled",
            )

        if token in self.token_mapping:
            return DetokenizationResult(
                token=token,
                original_value=self.token_mapping[token],
                found=True,
                message="Token successfully detokenized",
            )
        else:
            return DetokenizationResult(
                token=token,
                original_value=None,
                found=False,
                message="Token not found in mapping",
            )

    def analyze(self, text: Optional[str] = None, token: Optional[str] = None) -> AnalysisResult:
        """
        Ejecuta análisis: tokenizar texto o detokenizar token.

        Args:
            text: Texto a tokenizar
            token: Token a detokenizar

        Returns:
            AnalysisResult con resultados
        """
        if token:
            # Detokenización
            result = self.detokenize(token)
            return AnalysisResult(
                status="success" if result.found else "error",
                message=result.message,
                data=result.model_dump(),
            )

        elif text:
            # Tokenización
            result = self.tokenize_text(text)
            return AnalysisResult(
                status="success",
                message=f"Tokenized {result.total_tokens} items",
                data=result.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No text or token provided",
            data={},
            errors=["missing_input"],
        )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, str):
            return bool(data)
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "token_format": self.token_format,
            "enable_detokenization": str(self.enable_detokenization),
        }


# Alias para retrocompatibilidad
Digimon = Tokenizemon

