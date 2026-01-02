"""
Unit tests for Sessionmon (Mega)
"""

import pytest

from sessionmon.core import Sessionmon
from sessionmon.models import AnalysisResult, SessionAnalysis, Session


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Sessionmon"""
    return Sessionmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Sessionmon"
        assert digimon.mission == "Polite Society"
        assert digimon.role == "session-manager"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"session_timeout": 1800, "max_concurrent_sessions": 5}
        digimon = Sessionmon(config=config)
        assert digimon.session_timeout == 1800
        assert digimon.max_concurrent_sessions == 5


class TestSessionOperations:
    """Tests para operaciones con sesiones"""

    def test_create_session(self, digimon):
        """Test crear sesión"""
        session = digimon.create_session("user1")
        assert isinstance(session, Session)
        assert session.user_id == "user1"

    def test_validate_session(self, digimon):
        """Test validar sesión"""
        session = digimon.create_session("user1")
        assert digimon.validate_session(session.session_id) is True

    def test_analyze_sessions(self, digimon):
        """Test análisis de sesiones"""
        digimon.create_session("user1")
        analysis = digimon.analyze_sessions()
        assert isinstance(analysis, SessionAnalysis)
        assert analysis.active_sessions >= 1


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_sessions(self, digimon):
        """Test analyze con analyze action"""
        result = digimon.analyze(action="analyze")
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_create(self, digimon):
        """Test analyze con create action"""
        result = digimon.analyze(action="create", user_id="user1")
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("session_id") is True

    def test_validate_dict(self, digimon):
        """Test validación con diccionario"""
        assert digimon.validate({"user_id": "user1"}) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Sessionmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

