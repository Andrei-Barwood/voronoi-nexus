"""
Unit tests for PolytopeDetonate (Production)
"""

import pytest

from polytope_detonate.core import PolytopeDetonate
from polytope_detonate.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return PolytopeDetonate()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Polytope Detonate"
        assert module.mission == "Fleeting Joy"
        assert module.role == "sandbox-detonator"

    def test_init_with_config(self):
        mod = PolytopeDetonate(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "process_spawn_count": 18,
    "registry_modifications": 12,
    "network_callbacks": 4,
    "persistence_attempted": True,
}
        report = module.detonate_sample(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "process_spawn_count": 18,
    "registry_modifications": 12,
    "network_callbacks": 4,
    "persistence_attempted": True,
}
        result = module.analyze(sample_data=data)
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning", "error"]


class TestValidation:
    def test_validate_none(self, module):
        assert module.validate(None) is False

    def test_validate_dict(self, module):
        assert module.validate({"k": "v"}) is True


class TestInfo:
    def test_get_info_returns_dict(self, module):
        info = module.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Polytope Detonate"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
