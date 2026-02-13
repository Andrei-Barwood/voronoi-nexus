"""
Unit tests for PersistentNerve (Production)
"""

import pytest

from persistent_nerve.core import PersistentNerve
from persistent_nerve.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return PersistentNerve()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Persistent Nerve"
        assert module.mission == "The Gilded Cage"
        assert module.role == "behavior-analyzer"

    def test_init_with_config(self):
        mod = PersistentNerve(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "anomalous_process_tree": True,
    "credential_access_attempts": 4,
    "living_off_the_land_score": 0.79,
    "data_staging_events": 3,
}
        report = module.analyze_behavior(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "anomalous_process_tree": True,
    "credential_access_attempts": 4,
    "living_off_the_land_score": 0.79,
    "data_staging_events": 3,
}
        result = module.analyze(behavior_data=data)
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
        assert info["name"] == "Persistent Nerve"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
