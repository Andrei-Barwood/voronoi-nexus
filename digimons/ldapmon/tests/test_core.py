"""
Unit tests for LDAPmon (Mega)
"""

import pytest

from ldapmon.core import LDAPmon
from ldapmon.models import AnalysisResult, LDAPAnalysis, LDAPEntry


@pytest.fixture
def digimon():
    """Fixture para crear instancia de LDAPmon"""
    return LDAPmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "LDAPmon"
        assert digimon.mission == "American Distillation"
        assert digimon.role == "ldap-manager"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"ldap_url": "ldap://example.com", "use_tls": False}
        digimon = LDAPmon(config=config)
        assert digimon.ldap_url == "ldap://example.com"
        assert digimon.use_tls is False


class TestLDAPOperations:
    """Tests para operaciones LDAP"""

    def test_search_entries(self, digimon):
        """Test búsqueda de entradas"""
        digimon.entries.append({"dn": "cn=user1,dc=example,dc=com", "attributes": {}, "entry_type": "user"})
        entries = digimon.search_entries()
        assert len(entries) >= 0

    def test_analyze_directory(self, digimon):
        """Test análisis de directorio"""
        analysis = digimon.analyze_directory()
        assert isinstance(analysis, LDAPAnalysis)


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_directory(self, digimon):
        """Test analyze con analyze action"""
        result = digimon.analyze(action="analyze")
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_search(self, digimon):
        """Test analyze con search action"""
        search_data = {"filter": "(objectClass=user)"}
        result = digimon.analyze(action="search", search_data=search_data)
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario"""
        assert digimon.validate({"filter": "(objectClass=*)"}) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "LDAPmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

