"""
Unit tests for Anonymizemon (Mega)
"""

import pytest

from anonymizemon.core import Anonymizemon
from anonymizemon.models import AnalysisResult, AnonymizationResult


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Anonymizemon"""
    return Anonymizemon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Anonymizemon"
        assert digimon.mission == "Charlotte Balfour"
        assert digimon.role == "anonymizer"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"anonymization_method": "generalize", "reversible": True}
        digimon = Anonymizemon(config=config)
        assert digimon.anonymization_method == "generalize"
        assert digimon.reversible is True


class TestAnonymization:
    """Tests para anonimización"""

    def test_anonymize_data(self, digimon):
        """Test anonimización de datos"""
        data = {"name": "John Doe", "email": "john@example.com", "age": "30"}
        result = digimon.anonymize_data(data)
        assert isinstance(result, AnonymizationResult)
        assert result.anonymized_fields >= 1

    def test_anonymize_specific_fields(self, digimon):
        """Test anonimización de campos específicos"""
        data = {"name": "John", "email": "john@example.com", "public": "data"}
        result = digimon.anonymize_data(data, fields_to_anonymize=["email"])
        assert "email" in result.anonymized_data
        assert result.anonymized_data["email"] != "john@example.com"


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_data(self, digimon):
        """Test analyze con datos"""
        data = {"name": "John", "email": "john@example.com"}
        result = digimon.analyze(data=data)
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        assert digimon.validate({"name": "John"}) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Anonymizemon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

