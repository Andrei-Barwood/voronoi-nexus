"""
Unit tests for Forensimon (Mega)
"""

from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from forensimon.core import Forensimon
from forensimon.models import AnalysisResult, ArtifactAnalysis


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Forensimon"""
    return Forensimon()


@pytest.fixture
def sample_log_file():
    """Crea un archivo de log temporal para testing"""
    content = """2025-01-15 10:30:45 User login from 192.168.1.100
2025-01-15 10:31:22 Email sent to user@example.com
2025-01-15 10:32:10 Failed login from 10.0.0.1
api_key: secret123
password: admin123
2025-01-15 10:33:00 Connection from 192.168.1.200"""
    with NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    Path(f.name).unlink(missing_ok=True)


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Forensimon"
        assert digimon.mission == "The New South"
        assert digimon.role == "forensics-analyzer"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"max_file_size_mb": 200, "extract_timestamps": False}
        digimon = Forensimon(config=config)
        assert digimon.max_file_size_mb == 200
        assert digimon.extract_timestamps is False


class TestArtifactAnalysis:
    """Tests para análisis de artifacts"""

    def test_analyze_artifact_extracts_ips(self, digimon, sample_log_file):
        """Test que analyze_artifact extrae IPs"""
        result = digimon.analyze_artifact(sample_log_file)
        assert isinstance(result, ArtifactAnalysis)
        assert len(result.ips_found) > 0
        assert "192.168.1.100" in result.ips_found

    def test_analyze_artifact_extracts_emails(self, digimon, sample_log_file):
        """Test que analyze_artifact extrae emails"""
        result = digimon.analyze_artifact(sample_log_file)
        assert "user@example.com" in result.emails_found

    def test_analyze_artifact_finds_suspicious(self, digimon, sample_log_file):
        """Test que analyze_artifact encuentra patrones sospechosos"""
        result = digimon.analyze_artifact(sample_log_file)
        assert len(result.suspicious_patterns) > 0

    def test_analyze_artifact_nonexistent(self, digimon):
        """Test que analyze_artifact maneja archivos inexistentes"""
        result = digimon.analyze_artifact("/nonexistent/file.log")
        assert result.file_size == 0


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_single_artifact(self, digimon, sample_log_file):
        """Test analyze con un artifact"""
        result = digimon.analyze(artifact_path=sample_log_file)
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_multiple_artifacts(self, digimon, sample_log_file):
        """Test analyze con múltiples artifacts"""
        result = digimon.analyze(artifact_paths=[sample_log_file, sample_log_file])
        assert result.status == "success"
        assert result.data["total"] == 2

    def test_analyze_no_input(self, digimon):
        """Test analyze sin input"""
        result = digimon.analyze()
        assert result.status == "error"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("/path/to/file.log") is True

    def test_validate_list(self, digimon):
        """Test validación con lista"""
        assert digimon.validate(["/path1.log", "/path2.log"]) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Forensimon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
