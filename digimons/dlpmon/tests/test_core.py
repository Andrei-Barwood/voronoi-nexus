"""
Unit tests for DLPmon (Mega)
"""

import pytest

from dlpmon.core import DLPmon
from dlpmon.models import AnalysisResult, PolicyViolation


@pytest.fixture
def digimon():
    """Fixture para crear instancia de DLPmon"""
    return DLPmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "DLPmon"
        assert digimon.mission == "The New Austin"
        assert digimon.role == "data-loss-prevention"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"sensitivity_level": "high", "enable_blocking": False}
        digimon = DLPmon(config=config)
        assert digimon.sensitivity_level == "high"
        assert digimon.enable_blocking is False


class TestContentScanning:
    """Tests para escaneo de contenido"""

    def test_scan_content_credit_card(self, digimon):
        """Test detección de tarjeta de crédito"""
        content = "My card is 1234-5678-9012-3456"
        violations = digimon.scan_content(content)
        assert len(violations) >= 1
        assert any(v.policy_name == "credit_card" for v in violations)

    def test_scan_content_ssn(self, digimon):
        """Test detección de SSN"""
        content = "SSN: 123-45-6789"
        violations = digimon.scan_content(content)
        assert len(violations) >= 1
        assert any(v.policy_name == "ssn" for v in violations)

    def test_scan_content_clean(self, digimon):
        """Test contenido limpio"""
        content = "This is clean text with no sensitive data"
        violations = digimon.scan_content(content)
        assert len(violations) == 0


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_single_content(self, digimon):
        """Test analyze con un contenido"""
        content = "Email: test@example.com"
        result = digimon.analyze(content=content)
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning"]

    def test_analyze_multiple_contents(self, digimon):
        """Test analyze con múltiples contenidos"""
        contents = ["Email: test@example.com", "Card: 1234-5678-9012-3456"]
        result = digimon.analyze(contents=contents)
        assert result.status in ["success", "warning", "error"]


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("valid content") is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "DLPmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

