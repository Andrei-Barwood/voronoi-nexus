"""
Unit tests for OAuthmon (Mega)
"""

import pytest

from oauthmon.core import OAuthmon
from oauthmon.models import AnalysisResult, OAuthAnalysis, OAuthToken


@pytest.fixture
def digimon():
    """Fixture para crear instancia de OAuthmon"""
    return OAuthmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "OAuthmon"
        assert digimon.mission == "Marko Dragic"
        assert digimon.role == "oauth-handler"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"client_id": "client123", "authorization_url": "https://auth.example.com"}
        digimon = OAuthmon(config=config)
        assert digimon.client_id == "client123"
        assert digimon.authorization_url == "https://auth.example.com"


class TestOAuthOperations:
    """Tests para operaciones OAuth"""

    def test_generate_token(self, digimon):
        """Test generar token OAuth"""
        token = digimon.generate_token("authorization_code", "read write")
        assert isinstance(token, OAuthToken)
        assert token.token_type == "Bearer"

    def test_validate_token(self, digimon):
        """Test validar token"""
        token = digimon.generate_token()
        assert digimon.validate_token(token.access_token) is True

    def test_analyze_oauth(self, digimon):
        """Test análisis de OAuth"""
        digimon.generate_token()
        analysis = digimon.analyze_oauth()
        assert isinstance(analysis, OAuthAnalysis)
        assert analysis.active_tokens >= 1


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_oauth(self, digimon):
        """Test analyze con analyze action"""
        result = digimon.analyze(action="analyze")
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_generate(self, digimon):
        """Test analyze con generate action"""
        token_data = {"flow_type": "authorization_code", "scope": "read"}
        result = digimon.analyze(action="generate", token_data=token_data)
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("token_string") is True

    def test_validate_dict(self, digimon):
        """Test validación con diccionario"""
        assert digimon.validate({"flow_type": "authorization_code"}) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "OAuthmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

