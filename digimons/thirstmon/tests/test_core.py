"""
Unit tests for Thirstmon (Mega)
"""

import pytest

from thirstmon.core import Thirstmon
from thirstmon.models import AnalysisResult, ThreatAnalysis


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Thirstmon"""
    return Thirstmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Thirstmon"
        assert digimon.mission == "Good, Honest Snake Oil"
        assert isinstance(digimon.threat_database, dict)
        assert "evil-snake-oil.com" in digimon.threat_database

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"confidence_threshold": 0.9, "enable_reputation_check": False}
        digimon = Thirstmon(config=config)
        assert digimon.confidence_threshold == 0.9
        assert digimon.enable_reputation_check is False


class TestThreatAnalysis:
    """Tests para análisis de amenazas"""

    def test_analyze_threats(self, digimon):
        """Test análisis de amenazas"""
        iocs = ["google.com", "evil-snake-oil.com", "malware-download.net"]
        analysis = digimon.analyze_threats(iocs)
        assert isinstance(analysis, ThreatAnalysis)
        assert analysis.total_scanned == 3
        assert analysis.threats_detected >= 1

    def test_analyze_clean_iocs(self, digimon):
        """Test análisis de IOCs limpios"""
        iocs = ["google.com", "example.com"]
        analysis = digimon.analyze_threats(iocs)
        assert analysis.threats_detected == 0
        assert analysis.clean_count == 2


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_list(self, digimon):
        """Test analyze con lista de IOCs"""
        iocs = ["evil-snake-oil.com", "google.com"]
        result = digimon.analyze(iocs=iocs)
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning"]

    def test_analyze_single_ioc(self, digimon):
        """Test analyze con un IOC"""
        result = digimon.analyze(ioc="evil-snake-oil.com")
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning"]


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("example.com") is True

    def test_validate_list(self, digimon):
        """Test validación con lista válida"""
        assert digimon.validate(["google.com", "yahoo.com"]) is True

    def test_validate_invalid_list(self, digimon):
        """Test validación con lista inválida"""
        assert digimon.validate(["google.com", 123]) is False


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Thirstmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
