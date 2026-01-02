"""
Unit tests for Identitymon (Mega)
"""

import pytest

from identitymon.core import Identitymon
from identitymon.models import AnalysisResult, Identity, IdentityAnalysis


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Identitymon"""
    return Identitymon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Identitymon"
        assert digimon.mission == "The Gunslinger"
        assert digimon.role == "identity-manager"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"validate_attributes": False, "enforce_policies": False}
        digimon = Identitymon(config=config)
        assert digimon.validate_attributes is False
        assert digimon.enforce_policies is False


class TestIdentityValidation:
    """Tests para validación de identidades"""

    def test_validate_identity(self, digimon):
        """Test validación de identidad"""
        identity_data = {"user_id": "user1", "username": "testuser", "email": "test@example.com"}
        identity = digimon.validate_identity(identity_data)
        assert isinstance(identity, Identity)
        assert identity.user_id == "user1"

    def test_analyze_identities(self, digimon):
        """Test análisis de múltiples identidades"""
        identities = [
            {"user_id": "user1", "username": "user1", "roles": ["admin"]},
            {"user_id": "user2", "username": "user2", "roles": ["user"]},
        ]
        analysis = digimon.analyze_identities(identities)
        assert isinstance(analysis, IdentityAnalysis)
        assert analysis.total_identities == 2


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_single_identity(self, digimon):
        """Test analyze con una identidad"""
        identity = {"user_id": "user1", "username": "testuser"}
        result = digimon.analyze(identity=identity)
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_multiple_identities(self, digimon):
        """Test analyze con múltiples identidades"""
        # Agregar email para evitar violaciones de política (la política requiere email)
        identities = [{"user_id": "user1", "username": "user1", "email": "user1@example.com"}]
        result = digimon.analyze(identities=identities)
        assert result.status == "success"
        assert result.data["total_identities"] == 1

    def test_analyze_no_input(self, digimon):
        """Test analyze sin input"""
        result = digimon.analyze()
        assert result.status == "error"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        data = {"user_id": "user1", "username": "testuser"}
        assert digimon.validate(data) is True

    def test_validate_list(self, digimon):
        """Test validación con lista válida"""
        data = [{"user_id": "user1", "username": "user1"}]
        assert digimon.validate(data) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Identitymon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

