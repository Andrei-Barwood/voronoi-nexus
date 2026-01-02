"""
Core functionality for Scrapingmon (Mega)

Scrapingmon previene web scraping con detección avanzada y bloqueo.
Misión: All Debts Are Paid
Rol: anti-scraping-tool
"""

import logging
import re
import secrets
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, ScrapingAttempt, ScrapingAnalysis

logger = logging.getLogger(__name__)


class Scrapingmon:
    """
    Scrapingmon - Anti-Scraping Tool (Mega)

    Descripción:
        Previene web scraping con detección avanzada basada en rate limiting,
        user agents, patrones y comportamiento (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Scrapingmon.

        Args:
            config: Diccionario de configuración opcional:
                - detection_methods: Métodos de detección (default: rate_limit, user_agent, pattern, behavior)
                - rate_limit_threshold: Umbral de requests por minuto (default: 100)
                - block_duration_minutes: Duración de bloqueo (default: 60)
                - enable_captcha: Habilitar CAPTCHA (default: False)
                - suspicious_patterns: Patrones sospechosos en user agents (default: bot, crawler, scraper, spider)
        """
        self.name = "Scrapingmon"
        self.mission = "All Debts Are Paid"
        self.role = "anti-scraping-tool"
        self.config = config or {}

        self.detection_methods = self.config.get("detection_methods", ["rate_limit", "user_agent", "pattern", "behavior"])
        self.rate_limit_threshold = int(self.config.get("rate_limit_threshold", 100))
        self.block_duration_minutes = int(self.config.get("block_duration_minutes", 60))
        self.enable_captcha = bool(self.config.get("enable_captcha", False))
        self.suspicious_patterns = self.config.get("suspicious_patterns", ["bot", "crawler", "scraper", "spider"])

        # Tracking de requests (simulado)
        self.request_tracking: Dict[str, List[datetime]] = {}
        self.blocked_ips: Dict[str, datetime] = {}

        logger.info(
            "Initialized %s - %s (methods=%s, threshold=%d)",
            self.name,
            self.role,
            len(self.detection_methods),
            self.rate_limit_threshold,
        )

    def _check_rate_limit(self, ip_address: str) -> bool:
        """Verifica si una IP excede el rate limit."""
        now = datetime.now()
        one_minute_ago = datetime.fromtimestamp(now.timestamp() - 60)

        if ip_address not in self.request_tracking:
            self.request_tracking[ip_address] = []

        # Limpiar requests antiguos
        self.request_tracking[ip_address] = [
            req_time for req_time in self.request_tracking[ip_address] if req_time > one_minute_ago
        ]

        # Agregar request actual
        self.request_tracking[ip_address].append(now)

        return len(self.request_tracking[ip_address]) > self.rate_limit_threshold

    def _check_user_agent(self, user_agent: str) -> bool:
        """Verifica si el user agent es sospechoso."""
        user_agent_lower = user_agent.lower()
        return any(pattern.lower() in user_agent_lower for pattern in self.suspicious_patterns)

    def _check_behavior_pattern(self, ip_address: str) -> bool:
        """Verifica patrones de comportamiento sospechosos."""
        if ip_address not in self.request_tracking:
            return False

        requests = self.request_tracking[ip_address]
        if len(requests) < 5:
            return False

        # Verificar si hay requests muy regulares (patrón de bot)
        intervals = []
        for i in range(1, len(requests)):
            interval = (requests[i] - requests[i - 1]).total_seconds()
            intervals.append(interval)

        if len(intervals) < 3:
            return False

        # Si los intervalos son muy similares, es sospechoso
        avg_interval = sum(intervals) / len(intervals)
        variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
        return variance < 1.0  # Baja varianza = comportamiento robótico

    def analyze_request(self, ip_address: str, user_agent: str) -> ScrapingAttempt:
        """
        Analiza una request individual.

        Args:
            ip_address: IP de la request
            user_agent: User agent string

        Returns:
            ScrapingAttempt con resultado
        """
        attempt_id = secrets.token_urlsafe(8)
        detection_method = "none"
        severity = "low"
        blocked = False

        # Verificar si está bloqueado
        if ip_address in self.blocked_ips:
            blocked = True
            severity = "critical"
            detection_method = "blocked"

        # Rate limit check
        elif "rate_limit" in self.detection_methods and self._check_rate_limit(ip_address):
            detection_method = "rate_limit"
            severity = "high"
            blocked = True
            self.blocked_ips[ip_address] = datetime.now()

        # User agent check
        elif "user_agent" in self.detection_methods and self._check_user_agent(user_agent):
            detection_method = "user_agent"
            severity = "medium"

        # Behavior pattern check
        elif "behavior" in self.detection_methods and self._check_behavior_pattern(ip_address):
            detection_method = "behavior"
            severity = "high"
            blocked = True
            self.blocked_ips[ip_address] = datetime.now()

        request_count = len(self.request_tracking.get(ip_address, []))

        return ScrapingAttempt(
            attempt_id=attempt_id,
            ip_address=ip_address,
            user_agent=user_agent[:100],  # Truncar
            request_count=request_count,
            detection_method=detection_method,
            severity=severity,
            timestamp=datetime.now().isoformat(),
            blocked=blocked,
        )

    def analyze(self, requests: Optional[List[Dict[str, str]]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: analizar requests.

        Args:
            requests: Lista de requests con 'ip_address' y 'user_agent'

        Returns:
            AnalysisResult con resultados
        """
        if not requests:
            return AnalysisResult(
                status="error",
                message="No requests provided",
                data={},
                errors=["missing_requests"],
            )

        attempts: List[ScrapingAttempt] = []
        attempts_by_severity: Dict[str, int] = defaultdict(int)
        attempts_by_method: Dict[str, int] = defaultdict(int)
        blocked_count = 0

        for req in requests:
            ip_address = req.get("ip_address", "unknown")
            user_agent = req.get("user_agent", "unknown")

            attempt = self.analyze_request(ip_address, user_agent)
            attempts.append(attempt)

            attempts_by_severity[attempt.severity] += 1
            attempts_by_method[attempt.detection_method] += 1

            if attempt.blocked:
                blocked_count += 1

        status = "warning" if attempts else "success"
        if blocked_count > 0:
            status = "error"

        return AnalysisResult(
            status=status,
            message=f"Analyzed {len(requests)} requests: {len(attempts)} scraping attempts detected, {blocked_count} blocked",
            data={
                "total_requests": len(requests),
                "scraping_attempts": len(attempts),
                "blocked_attempts": blocked_count,
                "attempts_by_severity": dict(attempts_by_severity),
                "attempts_by_method": dict(attempts_by_method),
                "attempts": [a.model_dump() for a in attempts[:100]],  # Limitar
                "statistics": {
                    "rate_limit_threshold": self.rate_limit_threshold,
                    "block_duration_minutes": self.block_duration_minutes,
                    "detection_methods": self.detection_methods,
                },
            },
        )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, list):
            return all(isinstance(item, dict) and "ip_address" in item for item in data)
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "detection_methods": ", ".join(self.detection_methods),
            "rate_limit_threshold": str(self.rate_limit_threshold),
        }


# Alias para retrocompatibilidad
Digimon = Scrapingmon

