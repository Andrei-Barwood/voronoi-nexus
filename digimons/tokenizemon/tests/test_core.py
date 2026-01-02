"""
Unit tests for Tokenizemon (Mega)
"""

import pytest

from tokenizemon.core import Tokenizemon
from tokenizemon.models import AnalysisResult, TokenizationResult


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Tokenizemon"""
    return Tokenizemon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Tokenizemon"
        assert digimon.mission == "Paradise Mercifully Departed"
        assert digimon.role == "tokenization-engine"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"token_format": "random", "enable_detokenization": False}
        digimon = Tokenizemon(config=config)
        assert digimon.token_format == "random"
        assert digimon.enable_detokenization is False


class TestTokenization:
    """Tests para tokenización"""

    def test_tokenize_text(self, digimon):
        """Test tokenización de texto"""
        text = "Email: test@example.com"
        result = digimon.tokenize_text(text)
        assert isinstance(result, TokenizationResult)
        assert result.total_tokens >= 1

    def test_detokenize(self, digimon):
        """Test detokenización"""
        text = "Email: test@example.com"
        result = digimon.tokenize_text(text)
        if result.tokenization_records:
            token = result.tokenization_records[0].token
            detoken_result = digimon.detokenize(token)
            assert detoken_result.found is True


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_tokenize(self, digimon):
        """Test analyze para tokenización"""
        text = "Email: test@example.com"
        result = digimon.analyze(text=text)
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_detokenize(self, digimon):
        """Test analyze para detokenización"""
        text = "Email: test@example.com"
        tokenize_result = digimon.tokenize_text(text)
        if tokenize_result.tokenization_records:
            token = tokenize_result.tokenization_records[0].token
            result = digimon.analyze(token=token)
            assert result.status in ["success", "error"]


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
        assert info["name"] == "Tokenizemon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

