"""
Unit tests for SimplicialSwarm (Production)
"""

import pytest

from simplicial_swarm.core import SimplicialSwarm
from simplicial_swarm.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return SimplicialSwarm()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Simplicial Swarm"
        assert module.mission == "The Noblest of Men"
        assert module.role == "botnet-tracker"

    def test_init_with_config(self):
        mod = SimplicialSwarm(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "c2_contact_attempts": 15,
    "peer_fanout": 22,
    "domain_flux_detected": True,
    "synchronized_beacons": True,
}
        report = module.track_botnet(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "c2_contact_attempts": 15,
    "peer_fanout": 22,
    "domain_flux_detected": True,
    "synchronized_beacons": True,
}
        result = module.analyze(traffic_data=data)
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
        assert info["name"] == "Simplicial Swarm"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
