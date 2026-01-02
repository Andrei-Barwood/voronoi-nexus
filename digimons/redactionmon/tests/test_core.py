"""
Unit tests for Redactionmon (Mega)
"""

import pytest

from redactionmon.core import Redactionmon
from redactionmon.models import AnalysisResult, RedactionResult


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Redactionmon"""
    return Redactionmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Redactionmon"
        assert digimon.mission == "Outlaws from the West"
        assert digimon.role == "data-redactor"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"redaction_style": "tokenize", "preserve_structure": False}
        digimon = Redactionmon(config=config)
        assert digimon.redaction_style == "tokenize"
        assert digimon.preserve_structure is False


class TestRedaction:
    """Tests para redacción"""

    def test_redact_text_email(self, digimon):
        """Test redacción de email"""
        text = "Contact: test@example.com"
        result = digimon.redact_text(text)
        assert isinstance(result, RedactionResult)
        assert "test@example.com" not in result.redacted_text

    def test_redact_text_multiple_pii(self, digimon):
        """Test redacción de múltiples tipos de PII"""
        text = "Email: test@example.com, Phone: 555-123-4567"
        result = digimon.redact_text(text)
        assert result.total_redactions >= 1


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
        assert info["name"] == "Redactionmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

