"""
Core functionality for Credentialmon (Mega)

Credentialmon almacena credenciales de forma segura con encriptación.
Misión: Good Intentions
Rol: credential-vault
"""

import base64
import hashlib
import logging
import secrets
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, Credential, CredentialVault

logger = logging.getLogger(__name__)


class Credentialmon:
    """
    Credentialmon - Credential Vault (Mega)

    Descripción:
        Almacena credenciales de forma segura con encriptación,
        rotación de llaves y gestión de secretos (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Credentialmon.

        Args:
            config: Diccionario de configuración opcional:
                - encryption_enabled: Habilitar encriptación (default: True)
                - key_rotation_days: Días para rotación de llaves (default: 90)
                - hash_algorithm: Algoritmo de hash (default: "sha256")
        """
        self.name = "Credentialmon"
        self.mission = "Good Intentions"
        self.role = "credential-vault"
        self.config = config or {}

        self.encryption_enabled = bool(self.config.get("encryption_enabled", True))
        self.key_rotation_days = int(self.config.get("key_rotation_days", 90))
        self.hash_algorithm = self.config.get("hash_algorithm", "sha256")

        # Simulación de almacenamiento (en producción usar DB/HSM)
        self.vault: Dict[str, Dict[str, Any]] = {}
        self.encryption_key = secrets.token_bytes(32) if self.encryption_enabled else None

        logger.info(
            "Initialized %s - %s (encryption=%s, rotation=%dd)",
            self.name,
            self.role,
            self.encryption_enabled,
            self.key_rotation_days,
        )

    def _hash_credential(self, value: str) -> str:
        """Hash de credencial para almacenamiento seguro."""
        if self.hash_algorithm == "sha256":
            return hashlib.sha256(value.encode("utf-8")).hexdigest()
        return value

    def store_credential(self, credential_id: str, username: Optional[str], service: str, password: str) -> Credential:
        """
        Almacena una credencial de forma segura.

        Args:
            credential_id: ID único de la credencial
            username: Nombre de usuario (opcional)
            service: Nombre del servicio
            password: Contraseña (se hasheará/encriptará)

        Returns:
            Credential almacenada
        """
        now = datetime.now().isoformat()

        # Hash/encriptar contraseña
        if self.encryption_enabled:
            # Simulación: hash en lugar de encriptación real
            hashed_password = self._hash_credential(password)
        else:
            hashed_password = password  # NO recomendado en producción

        # Almacenar en vault
        self.vault[credential_id] = {
            "credential_id": credential_id,
            "username": username,
            "service": service,
            "password_hash": hashed_password,
            "encrypted": self.encryption_enabled,
            "created_at": now,
            "last_rotated": None,
        }

        return Credential(
            credential_id=credential_id,
            username=username,
            service=service,
            encrypted=self.encryption_enabled,
            created_at=now,
            last_rotated=None,
        )

    def analyze_vault(self) -> CredentialVault:
        """
        Analiza el vault de credenciales.

        Returns:
            CredentialVault con análisis
        """
        credentials = []
        encrypted = 0
        unencrypted = 0

        for cred_id, cred_data in self.vault.items():
            cred = Credential(
                credential_id=cred_data["credential_id"],
                username=cred_data.get("username"),
                service=cred_data["service"],
                encrypted=cred_data.get("encrypted", False),
                created_at=cred_data["created_at"],
                last_rotated=cred_data.get("last_rotated"),
            )
            credentials.append(cred)

            if cred.encrypted:
                encrypted += 1
            else:
                unencrypted += 1

        return CredentialVault(
            total_credentials=len(credentials),
            encrypted_count=encrypted,
            unencrypted_count=unencrypted,
            expired_keys=0,  # Simplificado
            credentials=credentials,
            vault_summary={
                "encryption_enabled": self.encryption_enabled,
                "key_rotation_days": self.key_rotation_days,
                "hash_algorithm": self.hash_algorithm,
            },
        )

    def analyze(self, action: str = "analyze", credential_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: analizar vault o almacenar credencial.

        Args:
            action: Acción ("analyze" o "store")
            credential_data: Datos de credencial (si action="store")

        Returns:
            AnalysisResult con resultados
        """
        if action == "analyze":
            vault = self.analyze_vault()
            status = "warning" if vault.unencrypted_count > 0 else "success"
            return AnalysisResult(
                status=status,
                message=f"Vault analyzed: {vault.total_credentials} credentials",
                data=vault.model_dump(),
            )

        elif action == "store" and credential_data:
            cred_id = credential_data.get("credential_id", "")
            username = credential_data.get("username")
            service = credential_data.get("service", "")
            password = credential_data.get("password", "")

            if not cred_id or not service or not password:
                return AnalysisResult(
                    status="error",
                    message="Missing required fields",
                    data={},
                    errors=["missing_fields"],
                )

            credential = self.store_credential(cred_id, username, service, password)
            return AnalysisResult(
                status="success",
                message="Credential stored successfully",
                data=credential.model_dump(),
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
            return "credential_id" in data and "service" in data and "password" in data
        return True  # Para análisis

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "encryption_enabled": str(self.encryption_enabled),
            "key_rotation_days": str(self.key_rotation_days),
        }


# Alias para retrocompatibilidad
Digimon = Credentialmon

