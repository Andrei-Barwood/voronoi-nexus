"""
Core functionality for Permissionmon (Mega)

Permissionmon valida permisos y accesos con principios de seguridad.
Misión: American Distillation
Rol: permission-checker
"""

import logging
import stat
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, PermissionCheck

logger = logging.getLogger(__name__)


class Permissionmon:
    """
    Permissionmon - Permission Checker (Mega)

    Descripción:
        Valida permisos y accesos aplicando principio de menor privilegio
        y verificando permisos de archivos/directorios (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Permissionmon.

        Args:
            config: Diccionario de configuración opcional:
                - check_file_permissions: Verificar permisos de archivos (default: True)
                - check_directory_permissions: Verificar permisos de directorios (default: True)
                - enforce_least_privilege: Aplicar menor privilegio (default: True)
        """
        self.name = "Permissionmon"
        self.mission = "American Distillation"
        self.role = "permission-checker"
        self.config = config or {}

        self.check_file_permissions = bool(self.config.get("check_file_permissions", True))
        self.check_directory_permissions = bool(self.config.get("check_directory_permissions", True))
        self.enforce_least_privilege = bool(self.config.get("enforce_least_privilege", True))

        # Límites de permisos seguros (2025-2026)
        self.max_file_perms = 0o644  # rw-r--r--
        self.max_dir_perms = 0o755  # rwxr-xr-x

        logger.info(
            "Initialized %s - %s (check_file=%s, check_dir=%s, least_priv=%s)",
            self.name,
            self.role,
            self.check_file_permissions,
            self.check_directory_permissions,
            self.enforce_least_privilege,
        )

    def check_permission(self, resource: str, required_permission: str) -> PermissionCheck:
        """
        Verifica permisos de un recurso.

        Args:
            resource: Ruta al recurso
            required_permission: Permiso requerido (read/write/execute)

        Returns:
            PermissionCheck con resultado
        """
        path = Path(resource)
        violations: List[str] = []
        granted = True
        resource_type = "unknown"
        current_perms = None

        if not path.exists():
            violations.append(f"Resource does not exist: {resource}")
            granted = False
        else:
            if path.is_file():
                resource_type = "file"
                if self.check_file_permissions:
                    perms = path.stat().st_mode & 0o777
                    current_perms = oct(perms)

                    # Verificar que no sea world-writable
                    if self.enforce_least_privilege and (perms & 0o002):
                        violations.append("File is world-writable (security risk)")
                        granted = False

                    if perms > self.max_file_perms:
                        violations.append(f"File permissions {current_perms} exceed maximum {oct(self.max_file_perms)}")
                        granted = False

                    # Verificar permiso específico
                    if required_permission == "read" and not (perms & 0o044):
                        violations.append("File is not readable")
                        granted = False
                    elif required_permission == "write" and not (perms & 0o022):
                        violations.append("File is not writable")
                        granted = False

            elif path.is_dir():
                resource_type = "directory"
                if self.check_directory_permissions:
                    perms = path.stat().st_mode & 0o777
                    current_perms = oct(perms)

                    if perms > self.max_dir_perms:
                        violations.append(f"Directory permissions {current_perms} exceed maximum {oct(self.max_dir_perms)}")
                        granted = False

        return PermissionCheck(
            resource=resource,
            resource_type=resource_type,
            required_permission=required_permission,
            granted=granted,
            current_permissions=current_perms,
            violations=violations,
        )

    def analyze(self, resource: Optional[str] = None, resources: Optional[List[Dict[str, str]]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: un recurso o múltiples.

        Args:
            resource: Recurso individual
            resources: Lista de recursos con permisos requeridos

        Returns:
            AnalysisResult con resultados
        """
        if resources:
            checks = []
            for res_data in resources:
                res_path = res_data.get("resource", "")
                req_perm = res_data.get("permission", "read")
                check = self.check_permission(res_path, req_perm)
                checks.append(check.model_dump())

            total_granted = sum(1 for c in checks if c["granted"])
            status = "success" if total_granted == len(checks) else "warning"

            return AnalysisResult(
                status=status,
                message=f"Checked {len(checks)} resources: {total_granted}/{len(checks)} granted",
                data={"checks": checks, "total": len(checks), "granted": total_granted},
            )

        elif resource:
            check = self.check_permission(resource, "read")
            status = "success" if check.granted else "warning"
            return AnalysisResult(
                status=status,
                message="Permission check completed",
                data=check.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No resource provided",
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
            return all(isinstance(item, dict) and "resource" in item for item in data)
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "enforce_least_privilege": str(self.enforce_least_privilege),
        }


# Alias para retrocompatibilidad
Digimon = Permissionmon

