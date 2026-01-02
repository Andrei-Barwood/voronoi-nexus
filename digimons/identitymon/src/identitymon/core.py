"""
Core functionality for Identitymon (Mega)

Identitymon gestiona identidades digitales con validación y políticas.
Misión: The Gunslinger
Rol: identity-manager
"""

import logging
from collections import defaultdict
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, Identity, IdentityAnalysis

logger = logging.getLogger(__name__)


class Identitymon:
    """
    Identitymon - Identity Manager (Mega)

    Descripción:
        Gestiona identidades digitales con validación de atributos,
        asignación de roles y cumplimiento de políticas (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Identitymon.

        Args:
            config: Diccionario de configuración opcional:
                - validate_attributes: Validar atributos (default: True)
                - check_roles: Verificar roles (default: True)
                - enforce_policies: Aplicar políticas (default: True)
        """
        self.name = "Identitymon"
        self.mission = "The Gunslinger"
        self.role = "identity-manager"
        self.config = config or {}

        self.validate_attributes = bool(self.config.get("validate_attributes", True))
        self.check_roles = bool(self.config.get("check_roles", True))
        self.enforce_policies = bool(self.config.get("enforce_policies", True))

        # Políticas de identidad
        self.policies = {
            "require_email": True,
            "min_roles": 0,
            "max_roles": 10,
            "required_attributes": ["user_id", "username"],
        }

        logger.info(
            "Initialized %s - %s (validate_attrs=%s, check_roles=%s)",
            self.name,
            self.role,
            self.validate_attributes,
            self.check_roles,
        )

    def validate_identity(self, identity_data: Dict[str, Any]) -> Identity:
        """
        Valida y crea una identidad.

        Args:
            identity_data: Datos de la identidad

        Returns:
            Identity validada
        """
        user_id = identity_data.get("user_id", "")
        username = identity_data.get("username", "")
        email = identity_data.get("email")
        roles = identity_data.get("roles", [])
        attributes = identity_data.get("attributes", {})
        status = identity_data.get("status", "active")

        # Validación básica
        if not user_id or not username:
            raise ValueError("user_id and username are required")

        return Identity(
            user_id=user_id,
            username=username,
            email=email,
            roles=roles if isinstance(roles, list) else [],
            attributes=attributes if isinstance(attributes, dict) else {},
            status=status,
        )

    def analyze_identities(self, identities: List[Dict[str, Any]]) -> IdentityAnalysis:
        """
        Analiza múltiples identidades.

        Args:
            identities: Lista de identidades

        Returns:
            IdentityAnalysis con resultados
        """
        valid_identities: List[Identity] = []
        roles_dist: Dict[str, int] = defaultdict(int)
        violations: List[str] = []

        for identity_data in identities:
            try:
                identity = self.validate_identity(identity_data)
                valid_identities.append(identity)

                # Distribución de roles
                for role in identity.roles:
                    roles_dist[role] += 1

                # Verificar políticas
                if self.enforce_policies:
                    if self.policies["require_email"] and not identity.email:
                        violations.append(f"{identity.user_id}: missing email")
                    if len(identity.roles) > self.policies["max_roles"]:
                        violations.append(f"{identity.user_id}: too many roles ({len(identity.roles)})")

            except Exception as e:
                violations.append(f"Validation error: {str(e)}")

        active = sum(1 for i in valid_identities if i.status == "active")
        inactive = len(valid_identities) - active

        return IdentityAnalysis(
            total_identities=len(valid_identities),
            active_identities=active,
            inactive_identities=inactive,
            roles_distribution=dict(roles_dist),
            policy_violations=violations[:50],  # Limitar a 50
            analysis_summary={
                "total_processed": len(identities),
                "valid_count": len(valid_identities),
                "violation_count": len(violations),
                "most_common_role": max(roles_dist.items(), key=lambda x: x[1])[0] if roles_dist else None,
            },
        )

    def analyze(self, identity: Optional[Dict[str, Any]] = None, identities: Optional[List[Dict[str, Any]]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: una identidad o múltiples.

        Args:
            identity: Identidad individual
            identities: Lista de identidades

        Returns:
            AnalysisResult con resultados
        """
        if identities:
            analysis = self.analyze_identities(identities)
            status = "warning" if analysis.policy_violations else "success"
            return AnalysisResult(
                status=status,
                message=f"Analyzed {analysis.total_identities} identities",
                data=analysis.model_dump(),
            )

        elif identity:
            try:
                validated = self.validate_identity(identity)
                status = "success"
                return AnalysisResult(
                    status=status,
                    message="Identity validated successfully",
                    data=validated.model_dump(),
                )
            except Exception as e:
                return AnalysisResult(
                    status="error",
                    message="Identity validation failed",
                    data={},
                    errors=[str(e)],
                )

        return AnalysisResult(
            status="error",
            message="No identity data provided",
            data={},
            errors=["missing_input"],
        )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, dict):
            return "user_id" in data and "username" in data
        if isinstance(data, list):
            return all(isinstance(item, dict) and "user_id" in item and "username" in item for item in data)
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "validate_attributes": str(self.validate_attributes),
        }


# Alias para retrocompatibilidad
Digimon = Identitymon

