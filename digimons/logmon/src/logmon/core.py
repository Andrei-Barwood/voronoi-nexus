"""
Core functionality for Logmon (Mega)

Logmon centraliza y analiza logs de seguridad con correlación avanzada.
Misión: Goodbye, Dear Friend
Rol: log-analyzer
"""

import logging
import re
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, LogAnalysis, LogEntry

logger = logging.getLogger(__name__)


class Logmon:
    """
    Logmon - Log Analyzer (Mega)

    Descripción:
        Centraliza y analiza logs de seguridad con correlación de eventos,
        detección de patrones y análisis de niveles (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Logmon.

        Args:
            config: Diccionario de configuración opcional:
                - log_levels: Niveles a procesar (default: ERROR, WARN, INFO, DEBUG)
                - pattern_detection: Detectar patrones (default: True)
                - correlation_window: Ventana de correlación en segundos (default: 300)
        """
        self.name = "Logmon"
        self.mission = "Goodbye, Dear Friend"
        self.role = "log-analyzer"
        self.config = config or {}

        self.log_levels = self.config.get("log_levels", ["ERROR", "WARN", "INFO", "DEBUG"])
        self.pattern_detection = bool(self.config.get("pattern_detection", True))
        self.correlation_window = int(self.config.get("correlation_window", 300))

        # Patrones comunes de seguridad
        self.security_patterns = [
            re.compile(r"(?i)(failed|denied|unauthorized|forbidden)", re.IGNORECASE),
            re.compile(r"(?i)(attack|intrusion|breach|compromise)", re.IGNORECASE),
            re.compile(r"(?i)(sql injection|xss|csrf)", re.IGNORECASE),
        ]

        logger.info(
            "Initialized %s - %s (levels=%s, correlation=%ds)",
            self.name,
            self.role,
            len(self.log_levels),
            self.correlation_window,
        )

    def parse_log_entry(self, log_line: str, source: Optional[str] = None) -> Optional[LogEntry]:
        """
        Parsea una línea de log.

        Args:
            log_line: Línea de log a parsear
            source: Fuente del log (opcional)

        Returns:
            LogEntry o None si no se puede parsear
        """
        # Patrón simple para logs comunes
        pattern = re.compile(r"(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2})[\s-]+(\w+)[\s:]+(.+)")
        match = pattern.match(log_line.strip())

        if not match:
            # Intentar parsear sin timestamp
            level_match = re.search(r"\b(ERROR|WARN|INFO|DEBUG|WARNING)\b", log_line, re.IGNORECASE)
            if level_match:
                level = level_match.group(1).upper()
                message = log_line
                timestamp = datetime.now().isoformat()
                return LogEntry(
                    timestamp=timestamp, level=level, message=message, source=source, metadata={}
                )
            return None

        timestamp, level, message = match.groups()
        return LogEntry(
            timestamp=timestamp, level=level.upper(), message=message, source=source, metadata={}
        )

    def analyze_logs(self, log_lines: List[str], source: Optional[str] = None) -> LogAnalysis:
        """
        Analiza múltiples líneas de log.

        Args:
            log_lines: Lista de líneas de log
            source: Fuente del log (opcional)

        Returns:
            LogAnalysis con resultados
        """
        entries: List[LogEntry] = []
        entries_by_level: Dict[str, int] = defaultdict(int)
        errors: List[LogEntry] = []
        warnings: List[LogEntry] = []
        patterns_detected: List[str] = []

        for line in log_lines:
            entry = self.parse_log_entry(line, source)
            if entry:
                entries.append(entry)
                entries_by_level[entry.level] += 1

                if entry.level == "ERROR":
                    errors.append(entry)
                elif entry.level in ["WARN", "WARNING"]:
                    warnings.append(entry)

                # Detectar patrones
                if self.pattern_detection:
                    for pattern in self.security_patterns:
                        if pattern.search(entry.message):
                            patterns_detected.append(entry.message[:100])  # Primeros 100 chars
                            break

        return LogAnalysis(
            total_entries=len(entries),
            entries_by_level=dict(entries_by_level),
            patterns_detected=patterns_detected[:50],  # Limitar a 50
            errors_found=errors,
            warnings_found=warnings,
            analysis_summary={
                "total_entries": len(entries),
                "error_count": len(errors),
                "warning_count": len(warnings),
                "pattern_count": len(patterns_detected),
                "most_common_level": max(entries_by_level.items(), key=lambda x: x[1])[0]
                if entries_by_level
                else None,
            },
        )

    def analyze(self, log_data: Optional[str] = None, log_lines: Optional[List[str]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: string o lista de líneas.

        Args:
            log_data: String con logs (será dividido en líneas)
            log_lines: Lista de líneas de log

        Returns:
            AnalysisResult con resultados
        """
        if log_lines:
            analysis = self.analyze_logs(log_lines)
        elif log_data:
            lines = log_data.splitlines()
            analysis = self.analyze_logs(lines)
        else:
            return AnalysisResult(
                status="error",
                message="No log data provided",
                data={},
                errors=["missing_input"],
            )

        status = "warning" if analysis.errors_found or analysis.patterns_detected else "success"

        return AnalysisResult(
            status=status,
            message=f"Log analysis completed: {analysis.total_entries} entries processed",
            data=analysis.model_dump(),
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
            "log_levels": ", ".join(self.log_levels),
            "correlation_window": str(self.correlation_window),
        }


# Alias para retrocompatibilidad
Digimon = Logmon
