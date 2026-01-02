"""
Core functionality for Thirstmon (Mega)

Thirstmon filtra indicadores de compromiso maliciosos con análisis avanzado.
Misión: Good, Honest Snake Oil
Rol: threat-filter
"""

import hashlib
import logging
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, IOCMatch, ThreatAnalysis

logger = logging.getLogger(__name__)


class Thirstmon:
    """
    Thirstmon - Threat Filter (Mega)

    Descripción:
        Filtra indicadores de compromiso (IOCs) con detección avanzada de
        múltiples tipos (IPs, dominios, URLs, hashes, emails) y categorización (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Thirstmon.

        Args:
            config: Diccionario de configuración opcional:
                - threat_types: Tipos de IOCs a detectar (default: ip, domain, url, hash, email)
                - confidence_threshold: Umbral de confianza mínimo (default: 0.7)
                - enable_reputation_check: Habilitar verificación de reputación (default: True)
        """
        self.name = "Thirstmon"
        self.mission = "Good, Honest Snake Oil"
        self.role = "threat-filter"
        self.config = config or {}

        self.threat_types = self.config.get("threat_types", ["ip", "domain", "url", "hash", "email"])
        self.confidence_threshold = float(self.config.get("confidence_threshold", 0.7))
        self.enable_reputation_check = bool(self.config.get("enable_reputation_check", True))

        # Base de datos de amenazas conocidas (simulada, en producción usar feeds reales)
        self.threat_database: Dict[str, Dict[str, Any]] = {
            "evil-snake-oil.com": {"type": "domain", "category": "malware", "confidence": 0.95},
            "192.168.66.6": {"type": "ip", "category": "botnet", "confidence": 0.90},
            "malware-download.net": {"type": "domain", "category": "malware", "confidence": 0.85},
            "phishing-bank.com": {"type": "domain", "category": "phishing", "confidence": 0.95},
            "ransomware-host.io": {"type": "domain", "category": "ransomware", "confidence": 0.90},
            "http://evil.com/malware.exe": {"type": "url", "category": "malware", "confidence": 0.85},
            "5d41402abc4b2a76b9719d911017c592": {"type": "hash", "category": "malware", "confidence": 0.80},
        }

        logger.info(
            "Initialized %s - %s (types=%s, threshold=%.2f, db_size=%d)",
            self.name,
            self.role,
            len(self.threat_types),
            self.confidence_threshold,
            len(self.threat_database),
        )

    def _classify_ioc_type(self, ioc: str) -> str:
        """
        Clasifica el tipo de IOC.

        Args:
            ioc: Indicator of Compromise

        Returns:
            Tipo de IOC (ip/domain/url/hash/email/unknown)
        """
        ioc_lower = ioc.lower().strip()

        # URL
        if ioc_lower.startswith(("http://", "https://", "ftp://")):
            return "url"

        # IP address
        ip_pattern = r'^(?:\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, ioc_lower):
            return "ip"

        # Hash (MD5, SHA1, SHA256)
        hash_pattern = r'^[a-f0-9]{32}$|^[a-f0-9]{40}$|^[a-f0-9]{64}$'
        if re.match(hash_pattern, ioc_lower):
            return "hash"

        # Email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, ioc_lower):
            return "email"

        # Domain
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'
        if re.match(domain_pattern, ioc_lower):
            return "domain"

        return "unknown"

    def _check_threat(self, ioc: str) -> Optional[Dict[str, Any]]:
        """
        Verifica si un IOC es una amenaza conocida.

        Args:
            ioc: Indicator of Compromise

        Returns:
            Información de la amenaza si es conocida, None en caso contrario
        """
        ioc_lower = ioc.lower().strip()

        # Verificación directa
        if ioc_lower in self.threat_database:
            threat_info = self.threat_database[ioc_lower].copy()
            threat_info["ioc"] = ioc
            return threat_info

        # Verificación por dominio (para URLs)
        if "/" in ioc_lower:
            domain = ioc_lower.split("/")[2] if "//" in ioc_lower else ioc_lower.split("/")[0]
            if domain in self.threat_database:
                threat_info = self.threat_database[domain].copy()
                threat_info["ioc"] = ioc
                return threat_info

        return None

    def analyze_threats(self, iocs: List[str]) -> ThreatAnalysis:
        """
        Analiza una lista de IOCs.

        Args:
            iocs: Lista de IOCs a analizar

        Returns:
            ThreatAnalysis con resultados
        """
        matches: List[IOCMatch] = []
        threats_by_type: Dict[str, int] = defaultdict(int)
        threats_by_category: Dict[str, int] = defaultdict(int)

        for ioc in iocs:
            ioc_type = self._classify_ioc_type(ioc)

            # Verificar si es amenaza conocida
            threat_info = self._check_threat(ioc)

            if threat_info and threat_info.get("confidence", 0.0) >= self.confidence_threshold:
                category = threat_info.get("category", "unknown")
                confidence = threat_info.get("confidence", 0.5)
                source = "threat_database"

                match = IOCMatch(
                    ioc=ioc,
                    ioc_type=ioc_type,
                    threat_category=category,
                    confidence=confidence,
                    source=source,
                )
                matches.append(match)

                threats_by_type[ioc_type] += 1
                threats_by_category[category] += 1

        clean_count = len(iocs) - len(matches)

        return ThreatAnalysis(
            total_scanned=len(iocs),
            threats_detected=len(matches),
            clean_count=clean_count,
            matches=matches,
            threats_by_type=dict(threats_by_type),
            threats_by_category=dict(threats_by_category),
            analysis_summary={
                "confidence_threshold": self.confidence_threshold,
                "reputation_check_enabled": self.enable_reputation_check,
                "database_size": len(self.threat_database),
            },
        )

    def analyze(self, iocs: Optional[List[str]] = None, ioc: Optional[str] = None) -> AnalysisResult:
        """
        Ejecuta análisis: un IOC o múltiples.

        Args:
            iocs: Lista de IOCs
            ioc: IOC individual

        Returns:
            AnalysisResult con resultados
        """
        if iocs:
            analysis = self.analyze_threats(iocs)
            status = "warning" if analysis.threats_detected > 0 else "success"
            return AnalysisResult(
                status=status,
                message=f"Threat analysis completed: {analysis.threats_detected} threats detected",
                data=analysis.model_dump(),
            )

        elif ioc:
            analysis = self.analyze_threats([ioc])
            status = "warning" if analysis.threats_detected > 0 else "success"
            return AnalysisResult(
                status=status,
                message="Threat analysis completed",
                data=analysis.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No IOC provided",
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
            return all(isinstance(item, str) and item for item in data)
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "threat_types": ", ".join(self.threat_types),
            "confidence_threshold": str(self.confidence_threshold),
        }


# Alias para retrocompatibilidad
Digimon = Thirstmon
