"""
Unit tests for VoronoiReclaim (Production)
"""

import pytest

from voronoi_reclaim.core import VoronoiReclaim
from voronoi_reclaim.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return VoronoiReclaim()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Voronoi Reclaim"
        assert module.mission == "Revenge"
        assert module.role == "ransomware-detector"

    def test_init_with_config(self):
        mod = VoronoiReclaim(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "mass_file_changes": 180,
    "entropy_spike": True,
    "shadow_copy_deleted": True,
    "suspicious_extension_ratio": 0.62,
}
        report = module.detect_ransomware(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "mass_file_changes": 180,
    "entropy_spike": True,
    "shadow_copy_deleted": True,
    "suspicious_extension_ratio": 0.62,
}
        result = module.analyze(event_data=data)
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
        assert info["name"] == "Voronoi Reclaim"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
