"""
Unit tests for Permissionmon (Mega)
"""

from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from permissionmon.core import Permissionmon
from permissionmon.models import AnalysisResult, PermissionCheck


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Permissionmon"""
    return Permissionmon()


@pytest.fixture
def temp_file():
    """Crea un archivo temporal para testing"""
    with NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")
        f.flush()
        yield f.name
    Path(f.name).unlink(missing_ok=True)


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Permissionmon"
        assert digimon.mission == "American Distillation"
        assert digimon.role == "permission-checker"


class TestPermissionChecking:
    """Tests para verificación de permisos"""

    def test_check_permission_file(self, digimon, temp_file):
        """Test verificación de permisos de archivo"""
        result = digimon.check_permission(temp_file, "read")
        assert isinstance(result, PermissionCheck)
        assert result.resource_type == "file"

    def test_check_permission_nonexistent(self, digimon):
        """Test verificación de recurso inexistente"""
        result = digimon.check_permission("/nonexistent/file", "read")
        assert result.granted is False


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_single_resource(self, digimon, temp_file):
        """Test analyze con un recurso"""
        result = digimon.analyze(resource=temp_file)
        assert isinstance(result, AnalysisResult)

    def test_analyze_multiple_resources(self, digimon, temp_file):
        """Test analyze con múltiples recursos"""
        resources = [{"resource": temp_file, "permission": "read"}]
        result = digimon.analyze(resources=resources)
        assert result.status in ["success", "warning"]


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("/path/to/file") is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Permissionmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

