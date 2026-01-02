"""
Core functionality for Hashmon (Mega)

Hashmon verifica integridad con hashes usando múltiples algoritmos.
Misión: Forever Yours, Arthur
Rol: hash-validator
"""

import hashlib
import hmac
import logging
import time
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, HashResult, VerificationResult

logger = logging.getLogger(__name__)


class Hashmon:
    """
    Hashmon - Hash Validator (Mega)

    Descripción:
        Verifica integridad con hashes usando múltiples algoritmos,
        soporte HMAC y procesamiento eficiente de archivos grandes (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Hashmon.

        Args:
            config: Diccionario de configuración opcional:
                - default_algorithm: Algoritmo por defecto (default: "sha256")
                - supported_algorithms: Algoritmos soportados (default: md5, sha1, sha256, sha512, blake2b)
                - enable_hmac: Habilitar HMAC (default: True)
                - chunk_size: Tamaño de chunk para archivos (default: 8192)
        """
        self.name = "Hashmon"
        self.mission = "Forever Yours, Arthur"
        self.role = "hash-validator"
        self.config = config or {}

        self.default_algorithm = self.config.get("default_algorithm", "sha256")
        self.supported_algorithms = self.config.get(
            "supported_algorithms", ["md5", "sha1", "sha256", "sha512", "blake2b"]
        )
        self.enable_hmac = bool(self.config.get("enable_hmac", True))
        self.chunk_size = int(self.config.get("chunk_size", 8192))

        logger.info(
            "Initialized %s - %s (algorithm=%s, hmac=%s)",
            self.name,
            self.role,
            self.default_algorithm,
            self.enable_hmac,
        )

    def _get_hash_object(self, algorithm: str):
        """
        Obtiene objeto hash para algoritmo dado.

        Args:
            algorithm: Nombre del algoritmo

        Returns:
            Objeto hashlib.Hash
        """
        algorithm_lower = algorithm.lower()

        if algorithm_lower == "md5":
            return hashlib.md5()
        elif algorithm_lower == "sha1":
            return hashlib.sha1()
        elif algorithm_lower == "sha256":
            return hashlib.sha256()
        elif algorithm_lower == "sha512":
            return hashlib.sha512()
        elif algorithm_lower == "blake2b":
            return hashlib.blake2b()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    def compute_hash(self, data: bytes, algorithm: Optional[str] = None, key: Optional[bytes] = None) -> HashResult:
        """
        Calcula hash de datos.

        Args:
            data: Datos a hashear
            algorithm: Algoritmo a usar (None = default)
            key: Clave para HMAC (opcional)

        Returns:
            HashResult con resultado
        """
        algorithm = algorithm or self.default_algorithm

        if algorithm not in self.supported_algorithms:
            raise ValueError(f"Algorithm {algorithm} not supported")

        start_time = time.time()

        if self.enable_hmac and key:
            hash_obj = hmac.new(key, data, algorithm)
            hash_value = hash_obj.hexdigest()
        else:
            hash_obj = self._get_hash_object(algorithm)
            hash_obj.update(data)
            hash_value = hash_obj.hexdigest()

        computation_time = (time.time() - start_time) * 1000  # ms

        return HashResult(
            algorithm=algorithm,
            hash_value=hash_value,
            input_length=len(data),
            computation_time_ms=computation_time,
            metadata={"hmac_used": bool(key) if self.enable_hmac else False},
        )

    def verify_hash(self, data: bytes, expected_hash: str, algorithm: Optional[str] = None, key: Optional[bytes] = None) -> VerificationResult:
        """
        Verifica hash de datos.

        Args:
            data: Datos a verificar
            expected_hash: Hash esperado
            algorithm: Algoritmo a usar (None = default)
            key: Clave para HMAC (opcional)

        Returns:
            VerificationResult con resultado
        """
        algorithm = algorithm or self.default_algorithm
        computed = self.compute_hash(data, algorithm, key)
        match = computed.hash_value.lower() == expected_hash.lower()

        return VerificationResult(
            verified=match,
            algorithm=algorithm,
            expected_hash=expected_hash,
            computed_hash=computed.hash_value,
            match=match,
            message="Hash verified" if match else "Hash mismatch",
        )

    def analyze(self, data: Optional[bytes] = None, expected_hash: Optional[str] = None, algorithm: Optional[str] = None, key: Optional[bytes] = None) -> AnalysisResult:
        """
        Ejecuta análisis: calcular o verificar hash.

        Args:
            data: Datos a procesar
            expected_hash: Hash esperado (para verificación)
            algorithm: Algoritmo a usar
            key: Clave para HMAC (opcional)

        Returns:
            AnalysisResult con resultados
        """
        if data is None:
            return AnalysisResult(
                status="error",
                message="No data provided",
                data={},
                errors=["missing_data"],
            )

        if expected_hash:
            # Verificación
            result = self.verify_hash(data, expected_hash, algorithm, key)
            return AnalysisResult(
                status="success" if result.verified else "error",
                message=result.message,
                data=result.model_dump(),
            )
        else:
            # Cálculo
            result = self.compute_hash(data, algorithm, key)
            return AnalysisResult(
                status="success",
                message=f"Hash computed: {result.algorithm}",
                data=result.model_dump(),
            )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, bytes):
            return len(data) > 0
        if isinstance(data, str):
            try:
                return len(data.encode("utf-8")) > 0
            except (UnicodeEncodeError, AttributeError):
                return False
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "default_algorithm": self.default_algorithm,
            "supported_algorithms": ", ".join(self.supported_algorithms),
        }


# Alias para retrocompatibilidad
Digimon = Hashmon

