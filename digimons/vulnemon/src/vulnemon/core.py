"""
Core functionality for Vulnemon (Mega)

Vulnemon escanea vulnerabilidades conocidas usando bases de datos CVE.
Misión: Paradise Mercifully Departed
Rol: vuln-scanner
"""

import logging
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, ScanResult, Vulnerability

logger = logging.getLogger(__name__)


class Vulnemon:
    """
    Vulnemon - Vulnerability Scanner (Mega)

    Descripción:
        Escanea vulnerabilidades conocidas usando bases de datos CVE
        y técnicas de detección avanzadas (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Vulnemon.

        Args:
            config: Diccionario de configuración opcional:
                - severity_threshold: Umbral de severidad (default: "medium")
                - check_cves: Verificar CVEs (default: True)
                - scan_depth: Profundidad de escaneo (default: 5)
        """
        self.name = "Vulnemon"
        self.mission = "Paradise Mercifully Departed"
        self.role = "vuln-scanner"
        self.config = config or {}

        self.severity_threshold = self.config.get("severity_threshold", "medium")
        self.check_cves = bool(self.config.get("check_cves", True))
        self.scan_depth = int(self.config.get("scan_depth", 5))

        # Base de datos simulada de vulnerabilidades conocidas
        self.vulnerability_db = {
            "openssl-1.0.2": [
                {
                    "cve_id": "CVE-2021-3450",
                    "severity": "critical",
                    "description": "X.509 certificate verification vulnerability",
                    "recommendation": "Update to OpenSSL 1.1.1 or later",
                }
            ],
            "apache-2.4.41": [
                {
                    "cve_id": "CVE-2021-44228",
                    "severity": "critical",
                    "description": "Log4j remote code execution",
                    "recommendation": "Update to Apache 2.4.50 or later",
                }
            ],
        }

        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        self.severity_threshold_level = severity_order.get(self.severity_threshold.lower(), 2)

        logger.info(
            "Initialized %s - %s (threshold=%s, depth=%d)",
            self.name,
            self.role,
            self.severity_threshold,
            self.scan_depth,
        )

    def scan_target(self, target: str) -> ScanResult:
        """
        Escanea un objetivo en busca de vulnerabilidades.

        Args:
            target: Objetivo a escanear (ej: "openssl-1.0.2")

        Returns:
            ScanResult con vulnerabilidades encontradas
        """
        vulnerabilities: List[Vulnerability] = []
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        # Buscar en base de datos
        if target in self.vulnerability_db:
            for vuln_data in self.vulnerability_db[target]:
                severity = vuln_data["severity"].lower()
                severity_level = {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(severity, 3)

                # Filtrar por umbral
                if severity_level <= self.severity_threshold_level:
                    vuln = Vulnerability(
                        cve_id=vuln_data.get("cve_id"),
                        severity=severity,
                        description=vuln_data["description"],
                        affected_component=target,
                        recommendation=vuln_data.get("recommendation"),
                    )
                    vulnerabilities.append(vuln)
                    severity_counts[severity] += 1

        return ScanResult(
            total_vulnerabilities=len(vulnerabilities),
            critical_count=severity_counts["critical"],
            high_count=severity_counts["high"],
            medium_count=severity_counts["medium"],
            low_count=severity_counts["low"],
            vulnerabilities=vulnerabilities,
            scan_summary={
                "target": target,
                "scan_depth": self.scan_depth,
                "cve_check_enabled": self.check_cves,
                "severity_threshold": self.severity_threshold,
            },
        )

    def analyze(self, target: Optional[str] = None, targets: Optional[List[str]] = None) -> AnalysisResult:
        """
        Ejecuta escaneo: un objetivo o múltiples.

        Args:
            target: Objetivo individual a escanear
            targets: Lista de objetivos a escanear

        Returns:
            AnalysisResult con resultados del escaneo
        """
        if targets:
            results = []
            total_vulns = 0
            for tgt in targets:
                scan = self.scan_target(tgt)
                results.append(scan.model_dump())
                total_vulns += scan.total_vulnerabilities

            return AnalysisResult(
                status="success",
                message=f"Scanned {len(targets)} targets, found {total_vulns} vulnerabilities",
                data={"scans": results, "total_targets": len(targets), "total_vulnerabilities": total_vulns},
            )

        elif target:
            scan = self.scan_target(target)
            status = "warning" if scan.total_vulnerabilities > 0 else "success"
            return AnalysisResult(
                status=status,
                message=f"Scan completed: {scan.total_vulnerabilities} vulnerabilities found",
                data=scan.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No target provided",
            data={},
            errors=["missing_input"],
        )

    def validate(self, data: Any) -> bool:
        """
        Valida datos de entrada.
        """
        if data is None:
            return False
        if isinstance(data, str):
            return bool(data)
        if isinstance(data, list):
            return all(isinstance(item, str) and item for item in data)
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
            "severity_threshold": self.severity_threshold,
            "scan_depth": str(self.scan_depth),
        }


# Alias para retrocompatibilidad
Digimon = Vulnemon
