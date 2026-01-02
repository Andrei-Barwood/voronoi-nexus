"""
Unit tests for Scrapingmon (Mega)
"""

import pytest

from scrapingmon.core import Scrapingmon
from scrapingmon.models import AnalysisResult, ScrapingAttempt


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Scrapingmon"""
    return Scrapingmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Scrapingmon"
        assert digimon.mission == "All Debts Are Paid"
        assert digimon.role == "anti-scraping-tool"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"rate_limit_threshold": 50, "block_duration_minutes": 30}
        digimon = Scrapingmon(config=config)
        assert digimon.rate_limit_threshold == 50
        assert digimon.block_duration_minutes == 30


class TestScrapingDetection:
    """Tests para detección de scraping"""

    def test_analyze_request_normal(self, digimon):
        """Test análisis de request normal"""
        attempt = digimon.analyze_request("192.168.1.1", "Mozilla/5.0")
        assert isinstance(attempt, ScrapingAttempt)
        assert attempt.severity in ["low", "medium", "high", "critical"]

    def test_analyze_request_suspicious_ua(self, digimon):
        """Test análisis de request con user agent sospechoso"""
        attempt = digimon.analyze_request("192.168.1.1", "bot/1.0")
        assert attempt.detection_method in ["user_agent", "none"]


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_requests(self, digimon):
        """Test analyze con lista de requests"""
        requests = [
            {"ip_address": "192.168.1.1", "user_agent": "Mozilla/5.0"},
            {"ip_address": "192.168.1.2", "user_agent": "bot/1.0"},
        ]
        result = digimon.analyze(requests=requests)
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning", "error"]


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_requests(self, digimon):
        """Test validación con lista de requests válida"""
        requests = [{"ip_address": "192.168.1.1", "user_agent": "Mozilla/5.0"}]
        assert digimon.validate(requests) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Scrapingmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

