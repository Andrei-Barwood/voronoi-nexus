"""
Core functionality for Encryptionmon (Mega)

Encryptionmon gestiona claves de cifrado con rotación y almacenamiento seguro.
Misión: Forced Proximity
Rol: encryption-manager
"""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, EncryptionKey, KeyManagementResult

logger = logging.getLogger(__name__)


class Encryptionmon:
    """
    Encryptionmon - Encryption Manager (Mega)

    Descripción:
        Gestiona claves de cifrado con rotación automática, almacenamiento
        seguro y derivación de claves (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Encryptionmon.

        Args:
            config: Diccionario de configuración opcional:
                - default_algorithm: Algoritmo por defecto (default: "AES-256-GCM")
                - key_rotation_days: Días para rotación (default: 90)
                - key_storage_backend: Backend de almacenamiento (default: "memory")
                - enable_key_derivation: Habilitar derivación (default: True)
        """
        self.name = "Encryptionmon"
        self.mission = "Forced Proximity"
        self.role = "encryption-manager"
        self.config = config or {}

        self.default_algorithm = self.config.get("default_algorithm", "AES-256-GCM")
        self.key_rotation_days = int(self.config.get("key_rotation_days", 90))
        self.key_storage_backend = self.config.get("key_storage_backend", "memory")
        self.enable_key_derivation = bool(self.config.get("enable_key_derivation", True))

        # Almacenamiento de claves (simulado)
        self.keys: Dict[str, EncryptionKey] = {}

        logger.info(
            "Initialized %s - %s (algorithm=%s, rotation_days=%d)",
            self.name,
            self.role,
            self.default_algorithm,
            self.key_rotation_days,
        )

    def generate_key(self, algorithm: Optional[str] = None, key_type: str = "symmetric") -> EncryptionKey:
        """
        Genera una nueva clave de cifrado.

        Args:
            algorithm: Algoritmo a usar (None = default)
            key_type: Tipo de clave (symmetric/asymmetric)

        Returns:
            EncryptionKey generada
        """
        algorithm = algorithm or self.default_algorithm
        key_id = secrets.token_urlsafe(16)

        now = datetime.now()
        expires_at = (now + timedelta(days=self.key_rotation_days)).isoformat()

        key = EncryptionKey(
            key_id=key_id,
            algorithm=algorithm,
            key_type=key_type,
            created_at=now.isoformat(),
            expires_at=expires_at,
            rotation_count=0,
            metadata={
                "storage_backend": self.key_storage_backend,
                "key_derivation_enabled": self.enable_key_derivation,
            },
        )

        self.keys[key_id] = key
        logger.info("Generated encryption key: %s (%s)", key_id, algorithm)

        return key

    def rotate_key(self, key_id: str) -> KeyManagementResult:
        """
        Rota una clave existente.

        Args:
            key_id: ID de la clave a rotar

        Returns:
            KeyManagementResult con resultado
        """
        if key_id not in self.keys:
            return KeyManagementResult(
                operation="rotate",
                key_id=key_id,
                success=False,
                message=f"Key {key_id} not found",
                keys_active=len(self.keys),
            )

        old_key = self.keys[key_id]
        new_key = self.generate_key(algorithm=old_key.algorithm, key_type=old_key.key_type)
        new_key.rotation_count = old_key.rotation_count + 1

        # Reemplazar clave
        del self.keys[key_id]
        self.keys[new_key.key_id] = new_key

        logger.info("Rotated key %s -> %s", key_id, new_key.key_id)

        return KeyManagementResult(
            operation="rotate",
            key_id=new_key.key_id,
            success=True,
            message=f"Key rotated: {key_id} -> {new_key.key_id}",
            keys_active=len(self.keys),
            keys_rotated=1,
        )

    def revoke_key(self, key_id: str) -> KeyManagementResult:
        """
        Revoca una clave.

        Args:
            key_id: ID de la clave a revocar

        Returns:
            KeyManagementResult con resultado
        """
        if key_id not in self.keys:
            return KeyManagementResult(
                operation="revoke",
                key_id=key_id,
                success=False,
                message=f"Key {key_id} not found",
                keys_active=len(self.keys),
            )

        del self.keys[key_id]
        logger.info("Revoked key: %s", key_id)

        return KeyManagementResult(
            operation="revoke",
            key_id=key_id,
            success=True,
            message=f"Key {key_id} revoked",
            keys_active=len(self.keys),
            keys_revoked=1,
        )

    def list_keys(self) -> List[EncryptionKey]:
        """
        Lista todas las claves activas.

        Returns:
            Lista de EncryptionKey
        """
        return list(self.keys.values())

    def check_expired_keys(self) -> List[str]:
        """
        Verifica claves expiradas.

        Returns:
            Lista de IDs de claves expiradas
        """
        now = datetime.now()
        expired = []

        for key_id, key in self.keys.items():
            if key.expires_at:
                expires_at = datetime.fromisoformat(key.expires_at)
                if expires_at < now:
                    expired.append(key_id)

        return expired

    def analyze(self, operation: Optional[str] = None, key_id: Optional[str] = None) -> AnalysisResult:
        """
        Ejecuta análisis: operaciones de gestión de claves.

        Args:
            operation: Operación a realizar (generate/rotate/revoke/list)
            key_id: ID de clave (para rotate/revoke)

        Returns:
            AnalysisResult con resultados
        """
        if operation == "generate":
            key = self.generate_key()
            return AnalysisResult(
                status="success",
                message=f"Generated encryption key: {key.key_id}",
                data=key.model_dump(),
            )

        elif operation == "rotate":
            if not key_id:
                return AnalysisResult(
                    status="error",
                    message="key_id required for rotate operation",
                    data={},
                    errors=["missing_key_id"],
                )
            result = self.rotate_key(key_id)
            return AnalysisResult(
                status="success" if result.success else "error",
                message=result.message,
                data=result.model_dump(),
            )

        elif operation == "revoke":
            if not key_id:
                return AnalysisResult(
                    status="error",
                    message="key_id required for revoke operation",
                    data={},
                    errors=["missing_key_id"],
                )
            result = self.revoke_key(key_id)
            return AnalysisResult(
                status="success" if result.success else "error",
                message=result.message,
                data=result.model_dump(),
            )

        elif operation == "list" or operation is None:
            keys = self.list_keys()
            expired = self.check_expired_keys()
            return AnalysisResult(
                status="success",
                message=f"Found {len(keys)} active keys, {len(expired)} expired",
                data={
                    "keys": [k.model_dump() for k in keys],
                    "total_keys": len(keys),
                    "expired_keys": expired,
                },
            )

        return AnalysisResult(
            status="error",
            message=f"Unknown operation: {operation}",
            data={},
            errors=["unknown_operation"],
        )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, dict):
            return "operation" in data
        if isinstance(data, str):
            return data in ["generate", "rotate", "revoke", "list"]
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "default_algorithm": self.default_algorithm,
            "key_rotation_days": str(self.key_rotation_days),
        }


# Alias para retrocompatibilidad
Digimon = Encryptionmon

