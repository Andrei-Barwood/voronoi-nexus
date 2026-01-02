"""
Core functionality for Compliancemon (Mega)

Compliancemon audita cumplimiento de regulaciones con múltiples frameworks.
Misión: Revenge
Rol: compliance-checker
"""

import logging
import secrets
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, ComplianceAudit, ComplianceCheck

logger = logging.getLogger(__name__)


class Compliancemon:
    """
    Compliancemon - Compliance Checker (Mega)

    Descripción:
        Audita cumplimiento de regulaciones con múltiples frameworks (GDPR,
        HIPAA, PCI-DSS, SOX, ISO27001) y reportes detallados (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Compliancemon.

        Args:
            config: Diccionario de configuración opcional:
                - compliance_frameworks: Frameworks a verificar (default: GDPR, HIPAA, PCI-DSS, SOX, ISO27001)
                - strict_mode: Modo estricto (default: True)
                - auto_remediation: Remediation automática (default: False)
                - report_format: Formato de reporte (default: "json")
        """
        self.name = "Compliancemon"
        self.mission = "Revenge"
        self.role = "compliance-checker"
        self.config = config or {}

        self.compliance_frameworks = self.config.get(
            "compliance_frameworks", ["GDPR", "HIPAA", "PCI-DSS", "SOX", "ISO27001"]
        )
        self.strict_mode = bool(self.config.get("strict_mode", True))
        self.auto_remediation = bool(self.config.get("auto_remediation", False))
        self.report_format = self.config.get("report_format", "json")

        # Requisitos de compliance (simulados)
        self.requirements: Dict[str, List[Dict[str, Any]]] = {
            "GDPR": [
                {"requirement": "Data encryption", "severity": "high"},
                {"requirement": "Right to be forgotten", "severity": "medium"},
                {"requirement": "Data breach notification", "severity": "critical"},
            ],
            "HIPAA": [
                {"requirement": "PHI encryption", "severity": "critical"},
                {"requirement": "Access controls", "severity": "high"},
                {"requirement": "Audit logs", "severity": "high"},
            ],
            "PCI-DSS": [
                {"requirement": "Card data encryption", "severity": "critical"},
                {"requirement": "Network segmentation", "severity": "high"},
                {"requirement": "Vulnerability scanning", "severity": "medium"},
            ],
            "SOX": [
                {"requirement": "Financial data integrity", "severity": "critical"},
                {"requirement": "Access controls", "severity": "high"},
                {"requirement": "Change management", "severity": "medium"},
            ],
            "ISO27001": [
                {"requirement": "Information security policy", "severity": "high"},
                {"requirement": "Risk assessment", "severity": "high"},
                {"requirement": "Incident management", "severity": "medium"},
            ],
        }

        logger.info(
            "Initialized %s - %s (frameworks=%s, strict=%s)",
            self.name,
            self.role,
            len(self.compliance_frameworks),
            self.strict_mode,
        )

    def _check_requirement(self, framework: str, requirement: Dict[str, Any], target_data: Dict[str, Any]) -> ComplianceCheck:
        """
        Verifica un requisito individual.

        Args:
            framework: Framework de compliance
            requirement: Requisito a verificar
            target_data: Datos del objetivo a auditar

        Returns:
            ComplianceCheck con resultado
        """
        check_id = secrets.token_urlsafe(8)
        req_name = requirement.get("requirement", "Unknown")
        severity = requirement.get("severity", "medium")

        # Simulación de verificación
        # En producción, esto haría verificaciones reales
        status = "pass"
        if self.strict_mode and severity in ["critical", "high"]:
            # En modo estricto, algunos checks pueden fallar
            if "encryption" in req_name.lower() and not target_data.get("encryption_enabled", False):
                status = "fail"
            elif "access" in req_name.lower() and not target_data.get("access_controls", False):
                status = "warning"

        remediation = None
        if status != "pass":
            remediation = f"Implement {req_name} according to {framework} requirements"

        return ComplianceCheck(
            check_id=check_id,
            framework=framework,
            requirement=req_name,
            status=status,
            severity=severity,
            description=f"Check {req_name} compliance for {framework}",
            remediation=remediation,
            evidence={"target": target_data.get("name", "unknown")},
        )

    def audit_target(self, target_data: Dict[str, Any]) -> ComplianceAudit:
        """
        Audita un objetivo para cumplimiento.

        Args:
            target_data: Datos del objetivo a auditar

        Returns:
            ComplianceAudit con resultados
        """
        audit_id = secrets.token_urlsafe(8)
        checks: List[ComplianceCheck] = []
        passed = 0
        failed = 0
        warnings = 0

        for framework in self.compliance_frameworks:
            if framework not in self.requirements:
                continue

            for requirement in self.requirements[framework]:
                check = self._check_requirement(framework, requirement, target_data)
                checks.append(check)

                if check.status == "pass":
                    passed += 1
                elif check.status == "fail":
                    failed += 1
                else:
                    warnings += 1

        total_checks = len(checks)
        compliance_score = (passed / total_checks * 100) if total_checks > 0 else 0.0

        return ComplianceAudit(
            audit_id=audit_id,
            frameworks_checked=self.compliance_frameworks,
            total_checks=total_checks,
            passed_checks=passed,
            failed_checks=failed,
            warning_checks=warnings,
            compliance_score=compliance_score,
            checks=checks,
            summary={
                "audit_timestamp": datetime.now().isoformat(),
                "strict_mode": self.strict_mode,
                "auto_remediation": self.auto_remediation,
            },
        )

    def analyze(self, target_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: auditoría de compliance.

        Args:
            target_data: Datos del objetivo a auditar

        Returns:
            AnalysisResult con resultados
        """
        if not target_data:
            return AnalysisResult(
                status="error",
                message="No target data provided",
                data={},
                errors=["missing_target_data"],
            )

        audit = self.audit_target(target_data)

        status = "success" if audit.compliance_score >= 80 else "warning"
        if audit.failed_checks > 0 and self.strict_mode:
            status = "error"

        return AnalysisResult(
            status=status,
            message=f"Compliance audit completed: {audit.compliance_score:.1f}% score, {audit.failed_checks} failures",
            data=audit.model_dump(),
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
            "compliance_frameworks": ", ".join(self.compliance_frameworks),
            "strict_mode": str(self.strict_mode),
        }


# Alias para retrocompatibilidad
Digimon = Compliancemon

