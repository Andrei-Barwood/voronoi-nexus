"""
Unit tests for Vulnemon (Mega)
"""

import pytest

from vulnemon.core import Vulnemon
from vulnemon.models import AnalysisResult, ScanResult


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Vulnemon"""
    return Vulnemon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Vulnemon"
        assert digimon.mission == "Paradise Mercifully Departed"
        assert digimon.role == "vuln-scanner"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"severity_threshold": "high", "scan_depth": 10}
        digimon = Vulnemon(config=config)
        assert digimon.severity_threshold == "high"
        assert digimon.scan_depth == 10


class TestScanning:
    """Tests para escaneo de vulnerabilidades"""

    def test_scan_target_with_vulns(self, digimon):
        """Test escaneo de objetivo con vulnerabilidades"""
        result = digimon.scan_target("openssl-1.0.2")
        assert isinstance(result, ScanResult)
        assert result.total_vulnerabilities > 0

    def test_scan_target_no_vulns(self, digimon):
        """Test escaneo de objetivo sin vulnerabilidades"""
        result = digimon.scan_target("unknown-component")
        assert result.total_vulnerabilities == 0


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_single_target(self, digimon):
        """Test analyze con un objetivo"""
        result = digimon.analyze(target="openssl-1.0.2")
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning"]

    def test_analyze_multiple_targets(self, digimon):
        """Test analyze con múltiples objetivos"""
        result = digimon.analyze(targets=["openssl-1.0.2", "apache-2.4.41"])
        assert result.status == "success"
        assert result.data["total_targets"] == 2

    def test_analyze_no_input(self, digimon):
        """Test analyze sin input"""
        result = digimon.analyze()
        assert result.status == "error"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("target") is True

    def test_validate_list(self, digimon):
        """Test validación con lista"""
        assert digimon.validate(["target1", "target2"]) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Vulnemon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
