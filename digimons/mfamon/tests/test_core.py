"""
Unit tests for MFAmon (Mega)
"""

import pytest

from mfamon.core import MFAmon
from mfamon.models import AnalysisResult, MFAAnalysis, MFAChallenge


@pytest.fixture
def digimon():
    """Fixture para crear instancia de MFAmon"""
    return MFAmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "MFAmon"
        assert digimon.mission == "Red Dead Redemption"
        assert digimon.role == "mfa-enforcer"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"code_expiry": 600, "max_attempts": 5}
        digimon = MFAmon(config=config)
        assert digimon.code_expiry == 600
        assert digimon.max_attempts == 5


class TestMFAOperations:
    """Tests para operaciones MFA"""

    def test_create_challenge(self, digimon):
        """Test crear desafío MFA"""
        challenge = digimon.create_challenge("user1", "totp")
        assert isinstance(challenge, MFAChallenge)
        assert challenge.user_id == "user1"

    def test_verify_challenge(self, digimon):
        """Test verificar código MFA"""
        challenge = digimon.create_challenge("user1", "totp")
        if challenge.code:
            result = digimon.verify_challenge(challenge.challenge_id, challenge.code)
            assert result is True

    def test_analyze_mfa(self, digimon):
        """Test análisis de MFA"""
        digimon.create_challenge("user1")
        analysis = digimon.analyze_mfa()
        assert isinstance(analysis, MFAAnalysis)
        assert analysis.total_challenges >= 1


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_mfa(self, digimon):
        """Test analyze con analyze action"""
        result = digimon.analyze(action="analyze")
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_create(self, digimon):
        """Test analyze con create action"""
        challenge_data = {"user_id": "user1", "method": "totp"}
        result = digimon.analyze(action="create", challenge_data=challenge_data)
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        data = {"user_id": "user1"}
        assert digimon.validate(data) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "MFAmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

