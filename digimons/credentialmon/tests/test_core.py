"""
Unit tests for Credentialmon (Mega)
"""

import pytest

from credentialmon.core import Credentialmon
from credentialmon.models import AnalysisResult, Credential, CredentialVault


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Credentialmon"""
    return Credentialmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Credentialmon"
        assert digimon.mission == "Good Intentions"
        assert digimon.role == "credential-vault"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"encryption_enabled": False, "key_rotation_days": 30}
        digimon = Credentialmon(config=config)
        assert digimon.encryption_enabled is False
        assert digimon.key_rotation_days == 30


class TestCredentialOperations:
    """Tests para operaciones con credenciales"""

    def test_store_credential(self, digimon):
        """Test almacenar credencial"""
        cred = digimon.store_credential("cred1", "user1", "service1", "password123")
        assert isinstance(cred, Credential)
        assert cred.credential_id == "cred1"

    def test_analyze_vault(self, digimon):
        """Test análisis de vault"""
        digimon.store_credential("cred1", "user1", "service1", "pass1")
        vault = digimon.analyze_vault()
        assert isinstance(vault, CredentialVault)
        assert vault.total_credentials == 1


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_vault(self, digimon):
        """Test analyze con analyze action"""
        result = digimon.analyze(action="analyze")
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_store(self, digimon):
        """Test analyze con store action"""
        cred_data = {
            "credential_id": "cred1",
            "username": "user1",
            "service": "service1",
            "password": "password123",
        }
        result = digimon.analyze(action="store", credential_data=cred_data)
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        data = {"credential_id": "cred1", "service": "service1", "password": "pass1"}
        assert digimon.validate(data) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Credentialmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

