"""
Unit tests for GeodesicPursuit (Production)
"""

import pytest

from geodesic_pursuit.core import GeodesicPursuit
from geodesic_pursuit.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return GeodesicPursuit()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Geodesic Pursuit"
        assert module.mission == "American Venom"
        assert module.role == "apt-hunter"

    def test_init_with_config(self):
        mod = GeodesicPursuit(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "lateral_movement_events": 7,
    "privilege_escalations": 2,
    "beaconing_detected": True,
    "dwell_time_days": 24,
}
        report = module.hunt_apt(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "lateral_movement_events": 7,
    "privilege_escalations": 2,
    "beaconing_detected": True,
    "dwell_time_days": 24,
}
        result = module.analyze(telemetry_data=data)
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
        assert info["name"] == "Geodesic Pursuit"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
