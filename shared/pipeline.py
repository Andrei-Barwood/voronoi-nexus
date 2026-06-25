"""
Security Pipeline - Integrates Snocomm modules

Este módulo orquesta el trabajo conjunto de Helix Filter y Simplex Secret
para crear un pipeline de seguridad completo.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Resolve project root (supports PyInstaller bundles via snocomm.paths)
try:
    from snocomm.paths import project_root as _project_root
except ImportError:
    _project_root = lambda: Path(__file__).resolve().parents[1]  # noqa: E731

_CORPORATE_DIR = _project_root() / "corporate"

# Agregar rutas de los módulos Snocomm al path
for _mod in ("helix_filter", "simplex_secret"):
    _src = str(_CORPORATE_DIR / _mod / "src")
    if _src not in sys.path:
        sys.path.insert(0, _src)

from helix_filter.core import HelixFilter
from simplex_secret.core import SimplexSecret

logger = logging.getLogger(__name__)


class SecurityPipeline:
    """
    Pipeline de seguridad que integra múltiples módulos Snocomm.

    Flujo:
    1. Helix Filter filtra amenazas en URLs/IPs
    2. Si el tráfico es limpio, Simplex Secret protege datos sensibles
    3. Retorna un reporte consolidado
    """

    def __init__(self):
        """Inicializar el pipeline con los módulos necesarios"""
        self.threat_filter = HelixFilter()
        self.data_protector = SimplexSecret()

        logger.info("Security Pipeline initialized with Helix Filter + Simplex Secret")

    def process_traffic(self, urls: List[str], content: str) -> Dict[str, Any]:
        """
        Procesa tráfico web completo: URLs + contenido

        Args:
            urls: Lista de URLs/IPs a verificar
            content: Contenido del tráfico (texto, emails, etc)

        Returns:
            Reporte consolidado con resultados de ambas fases
        """
        logger.info(f"Processing {len(urls)} URLs and {len(content)} chars of content")

        # ===== FASE 1: FILTRADO DE AMENAZAS (Helix Filter) =====
        threat_analysis = self.threat_filter.analyze(iocs=urls)

        # Acceder a los datos del AnalysisResult (ahora es objeto Pydantic)
        threats_detected = threat_analysis.data.get('threats_detected', 0)

        # Si se detectaron amenazas, bloquear todo
        if threats_detected > 0:
            logger.warning(f"Threats detected! Blocking traffic.")
            return {
                "status": "BLOCKED",
                "phase_completed": "threat_filtering",
                "threat_analysis": threat_analysis.model_dump(),
                "data_protection": None,
                "summary": {
                    "threats_found": threats_detected,
                    "blocked_urls": threat_analysis.data.get('matches', []),
                    "action": "Traffic blocked by Helix Filter"
                }
            }

        # ===== FASE 2: PROTECCIÓN DE DATOS (Simplex Secret) =====
        logger.info("No threats found. Proceeding to data protection...")
        data_analysis = self.data_protector.analyze(text=content)

        # Acceder a los datos del AnalysisResult
        total_redacted = data_analysis.data.get('total_redacted', 0)
        safe_text = data_analysis.data.get('safe_text', content)

        return {
            "status": "SAFE",
            "phase_completed": "data_protection",
            "threat_analysis": threat_analysis.model_dump(),
            "data_protection": data_analysis.model_dump(),
            "summary": {
                "threats_found": 0,
                "urls_scanned": len(urls),
                "data_redacted": total_redacted,
                "action": "Content processed and sanitized",
                "safe_content": safe_text
            }
        }

    def get_pipeline_info(self) -> Dict[str, Any]:
        """Información sobre los módulos en el pipeline"""
        return {
            "pipeline_version": "0.1.0",
            "modules_active": [
                self.threat_filter.get_info(),
                self.data_protector.get_info()
            ],
            "phases": [
                "1. Threat Filtering (Helix Filter)",
                "2. Data Protection (Simplex Secret)"
            ]
        }
