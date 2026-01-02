"""
Core functionality for LDAPmon (Mega)

LDAPmon gestiona directorios LDAP con búsquedas y análisis de seguridad.
Misión: American Distillation
Rol: ldap-manager
"""

import logging
from collections import defaultdict
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, LDAPAnalysis, LDAPEntry

logger = logging.getLogger(__name__)


class LDAPmon:
    """
    LDAPmon - LDAP Manager (Mega)

    Descripción:
        Gestiona directorios LDAP con búsquedas seguras, análisis
        de entradas y verificación de configuración (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar LDAPmon.

        Args:
            config: Diccionario de configuración opcional:
                - ldap_url: URL del servidor LDAP (opcional)
                - base_dn: Base DN para búsquedas (opcional)
                - use_tls: Usar TLS (default: True)
                - timeout: Timeout de conexión (default: 30)
        """
        self.name = "LDAPmon"
        self.mission = "American Distillation"
        self.role = "ldap-manager"
        self.config = config or {}

        self.ldap_url = self.config.get("ldap_url")
        self.base_dn = self.config.get("base_dn")
        self.use_tls = bool(self.config.get("use_tls", True))
        self.timeout = int(self.config.get("timeout", 30))

        # Simulación de almacenamiento de entradas (en producción usar conexión LDAP real)
        self.entries: List[Dict[str, Any]] = []

        logger.info(
            "Initialized %s - %s (use_tls=%s, timeout=%ds)",
            self.name,
            self.role,
            self.use_tls,
            self.timeout,
        )

    def search_entries(self, filter_str: str = "(objectClass=*)", attributes: Optional[List[str]] = None) -> List[LDAPEntry]:
        """
        Busca entradas LDAP.

        Args:
            filter_str: Filtro LDAP (default: "(objectClass=*)")
            attributes: Atributos a retornar (opcional)

        Returns:
            Lista de LDAPEntry encontradas
        """
        # Simulación de búsqueda (en producción usar biblioteca LDAP)
        results = []
        for entry_data in self.entries:
            # Filtrar según filter_str (simplificado)
            if "(objectClass=*)" in filter_str or "user" in filter_str.lower():
                entry = LDAPEntry(
                    dn=entry_data.get("dn", ""),
                    attributes=entry_data.get("attributes", {}),
                    entry_type=entry_data.get("entry_type", "unknown"),
                )
                results.append(entry)

        return results

    def analyze_directory(self) -> LDAPAnalysis:
        """
        Analiza el directorio LDAP.

        Returns:
            LDAPAnalysis con resultados
        """
        entries_by_type: Dict[str, int] = defaultdict(int)
        violations: List[str] = []

        for entry_data in self.entries:
            entry_type = entry_data.get("entry_type", "unknown")
            entries_by_type[entry_type] += 1

            # Verificar violaciones de seguridad
            if not self.use_tls:
                violations.append("LDAP connection not using TLS (security risk)")

        connection_status = "connected" if self.ldap_url else "not_configured"

        return LDAPAnalysis(
            total_entries=len(self.entries),
            entries_by_type=dict(entries_by_type),
            connection_status=connection_status,
            violations=violations,
            analysis_summary={
                "ldap_url": self.ldap_url,
                "base_dn": self.base_dn,
                "use_tls": self.use_tls,
                "violation_count": len(violations),
            },
        )

    def analyze(self, action: str = "analyze", search_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: analizar directorio o buscar entradas.

        Args:
            action: Acción ("analyze" o "search")
            search_data: Datos de búsqueda (si action="search")

        Returns:
            AnalysisResult con resultados
        """
        if action == "analyze":
            analysis = self.analyze_directory()
            status = "warning" if analysis.violations else "success"
            return AnalysisResult(
                status=status,
                message=f"LDAP analysis completed: {analysis.total_entries} entries",
                data=analysis.model_dump(),
            )

        elif action == "search" and search_data:
            filter_str = search_data.get("filter", "(objectClass=*)")
            attributes = search_data.get("attributes")
            entries = self.search_entries(filter_str, attributes)
            return AnalysisResult(
                status="success",
                message=f"LDAP search completed: {len(entries)} entries found",
                data={"entries": [e.model_dump() for e in entries], "count": len(entries)},
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
            return True  # Configuración o datos de búsqueda
        return True

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "use_tls": str(self.use_tls),
            "timeout": str(self.timeout),
        }


# Alias para retrocompatibilidad
Digimon = LDAPmon

