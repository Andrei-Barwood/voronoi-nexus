"""
Core functionality for Forensimon (Mega)

Forensimon analiza logs y artifacts forenses con técnicas avanzadas.
Misión: The New South
Rol: forensics-analyzer
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, ArtifactAnalysis

logger = logging.getLogger(__name__)


class Forensimon:
    """
    Forensimon - Forensics Analyzer (Mega)

    Descripción:
        Analiza logs y artifacts forenses extrayendo timestamps,
        IPs, emails y patrones sospechosos con prácticas 2025-2026.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Forensimon con configuración segura.

        Args:
            config: Diccionario de configuración opcional:
                - max_file_size_mb: Tamaño máximo de archivo (default: 100)
                - supported_formats: Formatos soportados
                - extract_timestamps: Extraer timestamps (default: True)
                - extract_ips: Extraer IPs (default: True)
                - extract_emails: Extraer emails (default: True)
        """
        self.name = "Forensimon"
        self.mission = "The New South"
        self.role = "forensics-analyzer"
        self.config = config or {}

        self.max_file_size_mb = int(self.config.get("max_file_size_mb", 100))
        self.supported_formats = self.config.get(
            "supported_formats", [".log", ".txt", ".json", ".csv", ".xml"]
        )
        self.extract_timestamps = bool(self.config.get("extract_timestamps", True))
        self.extract_ips = bool(self.config.get("extract_ips", True))
        self.extract_emails = bool(self.config.get("extract_emails", True))

        # Patrones regex para extracción (2025-2026 best practices)
        self.ip_pattern = re.compile(
            r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        )
        self.email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
        self.timestamp_patterns = [
            re.compile(r"\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}"),  # ISO 8601
            re.compile(r"\d{2}/\d{2}/\d{4}[\s]\d{2}:\d{2}:\d{2}"),  # Common format
        ]
        self.suspicious_patterns = [
            re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*\S+", re.IGNORECASE),
            re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*\S+", re.IGNORECASE),
            re.compile(r"(?i)(secret|token)\s*[:=]\s*\S+", re.IGNORECASE),
        ]

        logger.info(
            "Initialized %s - %s (max_size=%dMB, formats=%s)",
            self.name,
            self.role,
            self.max_file_size_mb,
            len(self.supported_formats),
        )

    def analyze_artifact(self, artifact_path: str) -> ArtifactAnalysis:
        """
        Analiza un artifact forense (archivo de log, etc).

        Args:
            artifact_path: Ruta al artifact a analizar

        Returns:
            ArtifactAnalysis con resultados del análisis
        """
        path = Path(artifact_path)
        result = {
            "artifact_path": artifact_path,
            "artifact_type": path.suffix.lower() if path.suffix else "unknown",
            "file_size": 0,
            "line_count": 0,
            "timestamps_found": [],
            "ips_found": [],
            "emails_found": [],
            "suspicious_patterns": [],
            "analysis_summary": {},
        }

        if not path.exists():
            return ArtifactAnalysis(**result)

        # Verificar tamaño
        file_size = path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        result["file_size"] = file_size

        if file_size_mb > self.max_file_size_mb:
            logger.warning("File size exceeds limit: %dMB > %dMB", file_size_mb, self.max_file_size_mb)
            return ArtifactAnalysis(**result)

        try:
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.splitlines()
                result["line_count"] = len(lines)

                # Extraer IPs
                if self.extract_ips:
                    ips = set(self.ip_pattern.findall(content))
                    result["ips_found"] = sorted(list(ips))

                # Extraer emails
                if self.extract_emails:
                    emails = set(self.email_pattern.findall(content))
                    result["emails_found"] = sorted(list(emails))

                # Extraer timestamps
                if self.extract_timestamps:
                    timestamps = set()
                    for pattern in self.timestamp_patterns:
                        timestamps.update(pattern.findall(content))
                    result["timestamps_found"] = sorted(list(timestamps))

                # Buscar patrones sospechosos
                suspicious = []
                for pattern in self.suspicious_patterns:
                    matches = pattern.findall(content)
                    if matches:
                        suspicious.extend(matches[:5])  # Limitar a 5 por patrón
                result["suspicious_patterns"] = suspicious[:20]  # Máximo 20 en total

                # Resumen
                result["analysis_summary"] = {
                    "total_lines": len(lines),
                    "unique_ips": len(result["ips_found"]),
                    "unique_emails": len(result["emails_found"]),
                    "unique_timestamps": len(result["timestamps_found"]),
                    "suspicious_count": len(result["suspicious_patterns"]),
                }

        except Exception as e:
            logger.error("Error analyzing artifact %s: %s", artifact_path, e)
            result["analysis_summary"]["error"] = str(e)

        return ArtifactAnalysis(**result)

    def analyze(self, artifact_path: Optional[str] = None, artifact_paths: Optional[List[str]] = None) -> AnalysisResult:
        """
        Ejecuta análisis forense: un artifact o múltiples.

        Args:
            artifact_path: Ruta a un artifact individual
            artifact_paths: Lista de rutas a múltiples artifacts

        Returns:
            AnalysisResult con resultados del análisis
        """
        if artifact_paths:
            results = []
            for path in artifact_paths:
                analysis = self.analyze_artifact(path)
                results.append(analysis.model_dump())

            return AnalysisResult(
                status="success",
                message=f"Analyzed {len(artifact_paths)} artifacts",
                data={"artifacts": results, "total": len(results)},
            )

        elif artifact_path:
            analysis = self.analyze_artifact(artifact_path)
            status = "success" if analysis.file_size > 0 else "error"
            return AnalysisResult(
                status=status,
                message="Artifact analysis completed",
                data=analysis.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No artifact path provided",
            data={},
            errors=["missing_input"],
        )

    def validate(self, data: Any) -> bool:
        """
        Valida datos de entrada (string o lista de strings).
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
            "max_file_size_mb": str(self.max_file_size_mb),
            "supported_formats": ", ".join(self.supported_formats),
        }


# Alias para retrocompatibilidad
Digimon = Forensimon
