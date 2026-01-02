"""
Unit tests for Bandidmon (Mega)
"""

import pytest

from bandidmon.core import Bandidmon
from bandidmon.models import AnalysisResult, RedactionResult


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Bandidmon"""
    return Bandidmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Bandidmon"
        assert digimon.mission == "Outlaws from the West"
        assert digimon.role == "data-protector"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"redaction_mode": "tokenize", "enable_ip_detection": False}
        digimon = Bandidmon(config=config)
        assert digimon.redaction_mode == "tokenize"
        assert digimon.enable_ip_detection is False


class TestRedaction:
    """Tests para redacción de PII"""

    def test_redact_email(self, digimon):
        """Test redacción de emails"""
        text = "Contact me at test@example.com for more info."
        result = digimon.redact_pii(text)
        assert isinstance(result, RedactionResult)
        assert "test@example.com" not in result.safe_text
        assert result.total_redacted >= 1

    def test_redact_credit_card(self, digimon):
        """Test redacción de tarjetas de crédito"""
        text = "My card is 1234-5678-9012-3456."
        result = digimon.redact_pii(text)
        assert "1234-5678-9012-3456" not in result.safe_text
        assert result.total_redacted >= 1

    def test_no_pii(self, digimon):
        """Test texto sin PII"""
        text = "Hello world, everything is safe here."
        result = digimon.redact_pii(text)
        assert result.total_redacted == 0
        assert result.safe_text == text


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
        texts = ["Email: test@example.com", "Card: 1234-5678-9012-3456"]
        result = digimon.analyze(texts=texts)
        assert result.status == "success"
        assert "total_redacted" in result.data


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("valid text") is True

    def test_validate_list(self, digimon):
        """Test validación con lista"""
        assert digimon.validate(["text1", "text2"]) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Bandidmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
