"""
Unit tests for SSOmon (Mega)
"""

import pytest

from ssomon.core import SSOmon
from ssomon.models import AnalysisResult, SSOAnalysis, SSOSession


@pytest.fixture
def digimon():
    """Fixture para crear instancia de SSOmon"""
    return SSOmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "SSOmon"
        assert digimon.mission == "Goodbye, Dear Friend"
        assert digimon.role == "sso-manager"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"enable_saml": False, "idp_url": "https://idp.example.com"}
        digimon = SSOmon(config=config)
        assert digimon.enable_saml is False
        assert digimon.idp_url == "https://idp.example.com"


class TestSSOOperations:
    """Tests para operaciones SSO"""

    def test_create_sso_session(self, digimon):
        """Test crear sesión SSO"""
        session = digimon.create_sso_session("user1", "idp1", "SAML")
        assert isinstance(session, SSOSession)
        assert session.user_id == "user1"

    def test_analyze_sso(self, digimon):
        """Test análisis de SSO"""
        digimon.create_sso_session("user1", "idp1", "SAML")
        analysis = digimon.analyze_sso()
        assert isinstance(analysis, SSOAnalysis)
        assert analysis.active_sessions >= 1


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_sso(self, digimon):
        """Test analyze con analyze action"""
        result = digimon.analyze(action="analyze")
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_create(self, digimon):
        """Test analyze con create action"""
        session_data = {"user_id": "user1", "idp": "idp1", "protocol": "SAML"}
        result = digimon.analyze(action="create", session_data=session_data)
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        data = {"user_id": "user1", "protocol": "SAML"}
        assert digimon.validate(data) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "SSOmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

