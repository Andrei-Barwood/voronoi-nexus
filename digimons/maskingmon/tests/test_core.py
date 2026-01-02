"""
Unit tests for Maskingmon (Mega)
"""

import pytest

from maskingmon.core import Maskingmon
from maskingmon.models import AnalysisResult, MaskingResult


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Maskingmon"""
    return Maskingmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Maskingmon"
        assert digimon.mission == "Good, Honest Snake Oil"
        assert digimon.role == "data-masker"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"mask_character": "X", "preserve_format": False}
        digimon = Maskingmon(config=config)
        assert digimon.mask_character == "X"
        assert digimon.preserve_format is False


class TestMasking:
    """Tests para enmascarado"""

    def test_mask_text_email(self, digimon):
        """Test enmascarado de email"""
        text = "Contact: test@example.com"
        result = digimon.mask_text(text)
        assert isinstance(result, MaskingResult)
        assert "test@example.com" not in result.masked_text
        assert "@example.com" in result.masked_text  # Dominio preservado

    def test_mask_text_credit_card(self, digimon):
        """Test enmascarado de tarjeta de crédito"""
        text = "Card: 1234-5678-9012-3456"
        result = digimon.mask_text(text)
        assert result.total_masked >= 1
        assert "3456" in result.masked_text  # Últimos 4 dígitos preservados


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_single_text(self, digimon):
        """Test analyze con un texto"""
        text = "Email: test@example.com"
        result = digimon.analyze(text=text)
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_multiple_texts(self, digimon):
        """Test analyze con múltiples textos"""
        texts = ["Email: test@example.com", "Phone: 555-1234"]
        result = digimon.analyze(texts=texts)
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("valid text") is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Maskingmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

