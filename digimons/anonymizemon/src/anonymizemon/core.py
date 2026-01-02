"""
Core functionality for Anonymizemon (Mega)

Anonymizemon anonimiza datos de test con múltiples métodos y preservación.
Misión: Charlotte Balfour
Rol: anonymizer
"""

import hashlib
import logging
import secrets
import string
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, AnonymizationRecord, AnonymizationResult

logger = logging.getLogger(__name__)


class Anonymizemon:
    """
    Anonymizemon - Anonymizer (Mega)

    Descripción:
        Anonimiza datos de test con múltiples métodos (pseudonimización,
        generalización, randomización) y opción de reversibilidad (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Anonymizemon.

        Args:
            config: Diccionario de configuración opcional:
                - anonymization_method: Método (pseudonymize/generalize/randomize) (default: "pseudonymize")
                - preserve_format: Preservar formato (default: True)
                - reversible: Habilitar reversibilidad (default: False)
                - seed: Semilla para anonimización determinística (opcional)
        """
        self.name = "Anonymizemon"
        self.mission = "Charlotte Balfour"
        self.role = "anonymizer"
        self.config = config or {}

        self.anonymization_method = self.config.get("anonymization_method", "pseudonymize")
        self.preserve_format = bool(self.config.get("preserve_format", True))
        self.reversible = bool(self.config.get("reversible", False))
        self.seed = self.config.get("seed")

        # Mapeo para reversibilidad (si está habilitada)
        self.mapping: Dict[str, str] = {}

        logger.info(
            "Initialized %s - %s (method=%s, reversible=%s)",
            self.name,
            self.role,
            self.anonymization_method,
            self.reversible,
        )

    def _pseudonymize(self, value: str, field_name: str = "") -> str:
        """
        Pseudonimiza un valor usando hash determinístico.

        Args:
            value: Valor a pseudonimizar
            field_name: Nombre del campo (para contexto)

        Returns:
            Valor pseudonimizado
        """
        if self.reversible and value in self.mapping:
            return self.mapping[value]

        # Hash determinístico
        hash_input = f"{self.seed or 'default'}:{field_name}:{value}"
        hash_obj = hashlib.sha256(hash_input.encode("utf-8"))
        hash_hex = hash_obj.hexdigest()[:16]  # Primeros 16 caracteres

        if self.preserve_format:
            # Intentar preservar formato básico
            if "@" in value:
                return f"user_{hash_hex[:8]}@example.com"
            elif value.replace("-", "").replace(" ", "").isdigit():
                return f"{hash_hex[:4]}-{hash_hex[4:6]}-{hash_hex[6:10]}"
            else:
                return f"anon_{hash_hex[:12]}"
        else:
            return f"anon_{hash_hex}"

    def _generalize(self, value: str, field_name: str = "") -> str:
        """
        Generaliza un valor.

        Args:
            value: Valor a generalizar
            field_name: Nombre del campo

        Returns:
            Valor generalizado
        """
        if field_name.lower() in ["age", "edad"]:
            try:
                age = int(value)
                if age < 18:
                    return "0-17"
                elif age < 30:
                    return "18-29"
                elif age < 50:
                    return "30-49"
                else:
                    return "50+"
            except ValueError:
                pass

        if "@" in value:
            return "[EMAIL_GENERALIZED]"

        return "[GENERALIZED]"

    def _randomize(self, value: str, field_name: str = "") -> str:
        """
        Randomiza un valor.

        Args:
            value: Valor a randomizar
            field_name: Nombre del campo

        Returns:
            Valor randomizado
        """
        if self.preserve_format:
            if "@" in value:
                return f"user_{secrets.token_hex(4)}@example.com"
            elif value.replace("-", "").replace(" ", "").isdigit():
                return f"{secrets.randbelow(9999):04d}-{secrets.randbelow(99):02d}-{secrets.randbelow(9999):04d}"
            else:
                return f"rand_{secrets.token_hex(8)}"
        else:
            return secrets.token_hex(12)

    def anonymize_field(self, field_name: str, value: Any) -> str:
        """
        Anonimiza un campo individual.

        Args:
            field_name: Nombre del campo
            value: Valor a anonimizar

        Returns:
            Valor anonimizado
        """
        if not isinstance(value, str):
            value = str(value)

        if self.anonymization_method == "pseudonymize":
            anonymized = self._pseudonymize(value, field_name)
        elif self.anonymization_method == "generalize":
            anonymized = self._generalize(value, field_name)
        elif self.anonymization_method == "randomize":
            anonymized = self._randomize(value, field_name)
        else:
            anonymized = value  # Sin cambios

        # Guardar mapeo si es reversible
        if self.reversible:
            self.mapping[value] = anonymized

        return anonymized

    def anonymize_data(self, data: Dict[str, Any], fields_to_anonymize: Optional[List[str]] = None) -> AnonymizationResult:
        """
        Anonimiza un diccionario de datos.

        Args:
            data: Datos a anonimizar
            fields_to_anonymize: Lista de campos a anonimizar (None = todos)

        Returns:
            AnonymizationResult con resultados
        """
        anonymized_data = data.copy()
        records: List[AnonymizationRecord] = []
        anonymized_count = 0

        fields_to_process = fields_to_anonymize if fields_to_anonymize else list(data.keys())

        for field_name in fields_to_process:
            if field_name not in data:
                continue

            original_value = str(data[field_name])
            anonymized_value = self.anonymize_field(field_name, original_value)

            anonymized_data[field_name] = anonymized_value
            anonymized_count += 1

            record = AnonymizationRecord(
                record_id=secrets.token_urlsafe(8),
                field_name=field_name,
                original_value=original_value[:50],  # Truncar
                anonymized_value=anonymized_value,
                method=self.anonymization_method,
                reversible=self.reversible,
            )
            records.append(record)

        return AnonymizationResult(
            original_data=data,
            anonymized_data=anonymized_data,
            total_fields=len(fields_to_process),
            anonymized_fields=anonymized_count,
            anonymization_records=records,
            statistics={
                "method": self.anonymization_method,
                "reversible": self.reversible,
                "preserve_format": self.preserve_format,
            },
        )

    def analyze(self, data: Optional[Dict[str, Any]] = None, fields: Optional[List[str]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: anonimizar datos.

        Args:
            data: Datos a anonimizar
            fields: Campos específicos a anonimizar (opcional)

        Returns:
            AnalysisResult con resultados
        """
        if data:
            result = self.anonymize_data(data, fields)
            return AnalysisResult(
                status="success",
                message=f"Anonymized {result.anonymized_fields} fields",
                data=result.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No data provided",
            data={},
            errors=["missing_input"],
        )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, dict):
            return len(data) > 0
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "anonymization_method": self.anonymization_method,
            "reversible": str(self.reversible),
        }


# Alias para retrocompatibilidad
Digimon = Anonymizemon

