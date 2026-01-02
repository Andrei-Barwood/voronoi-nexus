"""
Core functionality for Policymon (Mega)

Policymon valida cumplimiento de políticas de seguridad.
Misión: Charlotte Balfour
Rol: policy-enforcer
"""

import logging
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, PolicyAudit, PolicyCheck

logger = logging.getLogger(__name__)


class Policymon:
    """
    Policymon - Policy Enforcer (Mega)

    Descripción:
        Valida cumplimiento de políticas de seguridad con verificación
        de permisos, encriptación y reglas configuradas (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Policymon.

        Args:
            config: Diccionario de configuración opcional:
                - strict_mode: Modo estricto (default: True)
                - check_permissions: Verificar permisos (default: True)
                - check_encryption: Verificar encriptación (default: True)
        """
        self.name = "Policymon"
        self.mission = "Charlotte Balfour"
        self.role = "policy-enforcer"
        self.config = config or {}

        self.strict_mode = bool(self.config.get("strict_mode", True))
        self.check_permissions = bool(self.config.get("check_permissions", True))
        self.check_encryption = bool(self.config.get("check_encryption", True))

        # Políticas predefinidas
        self.policies = {
            "password_policy": {
                "min_length": 12,
                "require_uppercase": True,
                "require_lowercase": True,
                "require_numbers": True,
                "require_special": True,
            },
            "encryption_policy": {"min_key_bits": 256, "require_aead": True},
            "permission_policy": {"max_file_permissions": 0o644, "max_dir_permissions": 0o755},
        }

        logger.info(
            "Initialized %s - %s (strict=%s, check_perms=%s, check_enc=%s)",
            self.name,
            self.role,
            self.strict_mode,
            self.check_permissions,
            self.check_encryption,
        )

    def check_policy(self, policy_name: str, data: Dict[str, Any]) -> PolicyCheck:
        """
        Verifica una política específica.

        Args:
            policy_name: Nombre de la política
            data: Datos a verificar

        Returns:
            PolicyCheck con resultados
        """
        violations: List[str] = []
        warnings: List[str] = []
        recommendations: List[str] = []

        if policy_name == "password_policy" and policy_name in self.policies:
            policy = self.policies[policy_name]
            password = data.get("password", "")

            if len(password) < policy["min_length"]:
                violations.append(f"Password length < {policy['min_length']}")

            if policy["require_uppercase"] and not any(c.isupper() for c in password):
                violations.append("Password missing uppercase character")

            if policy["require_lowercase"] and not any(c.islower() for c in password):
                violations.append("Password missing lowercase character")

            if policy["require_numbers"] and not any(c.isdigit() for c in password):
                violations.append("Password missing number")

            if policy["require_special"] and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
                violations.append("Password missing special character")

        elif policy_name == "encryption_policy" and policy_name in self.policies:
            policy = self.policies[policy_name]
            key_bits = data.get("key_bits", 0)
            is_aead = data.get("is_aead", False)

            if key_bits < policy["min_key_bits"]:
                violations.append(f"Key length {key_bits} < {policy['min_key_bits']} bits")

            if policy["require_aead"] and not is_aead:
                violations.append("Encryption mode is not AEAD")

        elif policy_name == "permission_policy" and policy_name in self.policies:
            policy = self.policies[policy_name]
            file_perms = data.get("file_permissions", 0)
            dir_perms = data.get("dir_permissions", 0)

            if file_perms > policy["max_file_permissions"]:
                violations.append(f"File permissions {oct(file_perms)} exceed maximum")

            if dir_perms > policy["max_dir_permissions"]:
                violations.append(f"Directory permissions {oct(dir_perms)} exceed maximum")

        compliant = len(violations) == 0

        if not compliant and self.strict_mode:
            recommendations.append(f"Review and fix {policy_name} violations")

        return PolicyCheck(
            policy_name=policy_name,
            compliant=compliant,
            violations=violations,
            warnings=warnings,
            recommendations=recommendations,
        )

    def audit_policies(self, checks: List[Dict[str, Any]]) -> PolicyAudit:
        """
        Audita múltiples políticas.

        Args:
            checks: Lista de verificaciones de política

        Returns:
            PolicyAudit con resultados
        """
        policy_checks: List[PolicyCheck] = []
        passed = 0
        failed = 0

        for check_data in checks:
            policy_name = check_data.get("policy_name", "unknown")
            data = check_data.get("data", {})
            check_result = self.check_policy(policy_name, data)
            policy_checks.append(check_result)

            if check_result.compliant:
                passed += 1
            else:
                failed += 1

        return PolicyAudit(
            total_checks=len(checks),
            passed_checks=passed,
            failed_checks=failed,
            checks=policy_checks,
            audit_summary={
                "compliance_rate": (passed / len(checks) * 100) if checks else 0,
                "strict_mode": self.strict_mode,
            },
        )

    def analyze(self, policy_check: Optional[Dict[str, Any]] = None, policy_checks: Optional[List[Dict[str, Any]]] = None) -> AnalysisResult:
        """
        Ejecuta verificación: una política o múltiples.

        Args:
            policy_check: Verificación individual
            policy_checks: Lista de verificaciones

        Returns:
            AnalysisResult con resultados
        """
        if policy_checks:
            audit = self.audit_policies(policy_checks)
            status = "warning" if audit.failed_checks > 0 else "success"
            return AnalysisResult(
                status=status,
                message=f"Policy audit completed: {audit.passed_checks}/{audit.total_checks} passed",
                data=audit.model_dump(),
            )

        elif policy_check:
            policy_name = policy_check.get("policy_name", "unknown")
            data = policy_check.get("data", {})
            check_result = self.check_policy(policy_name, data)
            status = "success" if check_result.compliant else "warning"
            return AnalysisResult(
                status=status,
                message=f"Policy check completed: {'compliant' if check_result.compliant else 'non-compliant'}",
                data=check_result.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No policy check provided",
            data={},
            errors=["missing_input"],
        )

    def validate(self, data: Any) -> bool:
        """
        Valida datos de entrada.
        """
        if data is None:
            return False
        if isinstance(data, dict):
            return "policy_name" in data and "data" in data
        if isinstance(data, list):
            return all(isinstance(item, dict) and "policy_name" in item and "data" in item for item in data)
        return False

    def get_info(self) -> Dict[str, str]:
        """
        Obtener información del Digimon.
        """
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "strict_mode": str(self.strict_mode),
        }


# Alias para retrocompatibilidad
Digimon = Policymon
