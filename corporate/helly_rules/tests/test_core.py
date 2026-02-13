"""
Unit tests for HellyRules (Production)
"""

import pytest

from helly_rules.core import HellyRules
from helly_rules.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return HellyRules()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Helly Rules"
        assert module.mission == "Charlotte Balfour"
        assert module.role == "yara-rule-engine"

    def test_init_with_config(self):
        mod = HellyRules(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "rules_compiled": 24,
    "syntax_errors": 0,
    "high_confidence_matches": 3,
    "suspicious_strings_detected": 11,
}
        report = module.execute_yara(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "rules_compiled": 24,
    "syntax_errors": 0,
    "high_confidence_matches": 3,
    "suspicious_strings_detected": 11,
}
        result = module.analyze(rule_data=data)
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
        assert info["name"] == "Helly Rules"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
