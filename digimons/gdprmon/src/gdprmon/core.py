"""
Core functionality for GDPRmon (Mega)

GDPRmon cumple regulaciones GDPR con verificaciones específicas.
Misión: Charlotte Balfour
Rol: gdpr-enforcer
"""

import logging
import secrets
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, GDPRCheck, GDPRComplianceReport

logger = logging.getLogger(__name__)


class GDPRmon:
    """
    GDPRmon - GDPR Enforcer (Mega)

    Descripción:
        Cumple regulaciones GDPR con verificaciones específicas de artículos,
        derechos de sujetos de datos y gestión de consentimiento (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar GDPRmon.

        Args:
            config: Diccionario de configuración opcional:
                - strict_mode: Modo estricto (default: True)
                - check_data_subject_rights: Verificar derechos de sujetos (default: True)
                - check_data_breach_notification: Verificar notificación de brechas (default: True)
                - check_consent_management: Verificar gestión de consentimiento (default: True)
        """
        self.name = "GDPRmon"
        self.mission = "Charlotte Balfour"
        self.role = "gdpr-enforcer"
        self.config = config or {}

        self.strict_mode = bool(self.config.get("strict_mode", True))
        self.check_data_subject_rights = bool(self.config.get("check_data_subject_rights", True))
        self.check_data_breach_notification = bool(self.config.get("check_data_breach_notification", True))
        self.check_consent_management = bool(self.config.get("check_consent_management", True))

        # Requisitos GDPR (simulados)
        self.gdpr_articles: List[Dict[str, Any]] = [
            {"article": "Art. 5", "requirement": "Lawful processing", "severity": "critical"},
            {"article": "Art. 6", "requirement": "Legal basis for processing", "severity": "critical"},
            {"article": "Art. 7", "requirement": "Consent management", "severity": "high"},
            {"article": "Art. 15", "requirement": "Right of access", "severity": "high"},
            {"article": "Art. 17", "requirement": "Right to erasure (right to be forgotten)", "severity": "high"},
            {"article": "Art. 20", "requirement": "Right to data portability", "severity": "medium"},
            {"article": "Art. 32", "requirement": "Security of processing", "severity": "critical"},
            {"article": "Art. 33", "requirement": "Data breach notification to authority", "severity": "critical"},
            {"article": "Art. 35", "requirement": "Data protection impact assessment", "severity": "high"},
        ]

        logger.info(
            "Initialized %s - %s (strict=%s, articles=%d)",
            self.name,
            self.role,
            self.strict_mode,
            len(self.gdpr_articles),
        )

    def _check_article(self, article: Dict[str, Any], target_data: Dict[str, Any]) -> GDPRCheck:
        """
        Verifica cumplimiento de un artículo GDPR.

        Args:
            article: Artículo a verificar
            target_data: Datos del objetivo a auditar

        Returns:
            GDPRCheck con resultado
        """
        check_id = secrets.token_urlsafe(8)
        article_num = article.get("article", "Unknown")
        requirement = article.get("requirement", "Unknown")
        severity = article.get("severity", "medium")

        # Simulación de verificación
        status = "pass"
        remediation = None

        # Verificaciones específicas
        if "consent" in requirement.lower() and not target_data.get("consent_management_enabled", False):
            status = "fail" if self.strict_mode else "warning"
            remediation = f"Implement consent management system for {article_num}"
        elif "breach" in requirement.lower() and not target_data.get("breach_notification_procedures", False):
            status = "fail" if self.strict_mode else "warning"
            remediation = f"Establish data breach notification procedures for {article_num}"
        elif "erasure" in requirement.lower() or "forgotten" in requirement.lower():
            if not target_data.get("data_erasure_capability", False):
                status = "fail" if self.strict_mode else "warning"
                remediation = f"Implement data erasure capability for {article_num}"
        elif "security" in requirement.lower() and not target_data.get("encryption_enabled", False):
            status = "fail" if self.strict_mode else "warning"
            remediation = f"Enable encryption for {article_num}"

        return GDPRCheck(
            check_id=check_id,
            article=article_num,
            requirement=requirement,
            status=status,
            severity=severity,
            description=f"Check {requirement} compliance for {article_num}",
            remediation=remediation,
            evidence={"target": target_data.get("name", "unknown")},
        )

    def audit_compliance(self, target_data: Dict[str, Any]) -> GDPRComplianceReport:
        """
        Audita cumplimiento GDPR de un objetivo.

        Args:
            target_data: Datos del objetivo a auditar

        Returns:
            GDPRComplianceReport con resultados
        """
        report_id = secrets.token_urlsafe(8)
        checks: List[GDPRCheck] = []
        passed = 0
        failed = 0
        warnings = 0

        for article in self.gdpr_articles:
            check = self._check_article(article, target_data)
            checks.append(check)

            if check.status == "pass":
                passed += 1
            elif check.status == "fail":
                failed += 1
            else:
                warnings += 1

        total_checks = len(checks)
        compliance_score = (passed / total_checks * 100) if total_checks > 0 else 0.0

        # Estado de derechos de sujetos de datos
        data_subject_rights_status = {
            "right_of_access": target_data.get("data_subject_access_rights", False),
            "right_to_erasure": target_data.get("data_erasure_capability", False),
            "right_to_portability": target_data.get("data_portability_capability", False),
            "right_to_rectification": target_data.get("data_rectification_capability", False),
        }

        return GDPRComplianceReport(
            report_id=report_id,
            total_checks=total_checks,
            passed_checks=passed,
            failed_checks=failed,
            warning_checks=warnings,
            compliance_score=compliance_score,
            checks=checks,
            data_subject_rights_status=data_subject_rights_status,
            summary={
                "audit_timestamp": datetime.now().isoformat(),
                "strict_mode": self.strict_mode,
                "gdpr_articles_checked": len(self.gdpr_articles),
            },
        )

    def analyze(self, target_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: auditoría GDPR.

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

        report = self.audit_compliance(target_data)

        status = "success" if report.compliance_score >= 80 else "warning"
        if report.failed_checks > 0 and self.strict_mode:
            status = "error"

        return AnalysisResult(
            status=status,
            message=f"GDPR compliance audit completed: {report.compliance_score:.1f}% score, {report.failed_checks} failures",
            data=report.model_dump(),
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
            "strict_mode": str(self.strict_mode),
        }


# Alias para retrocompatibilidad
Digimon = GDPRmon

