"""Tests for the unified snocomm CLI."""

import json

import pytest
from click.testing import CliRunner

from snocomm.cli import main
from snocomm.manifest import load_manifest, resolve_module
from snocomm.runner import run_analyze, run_info


@pytest.fixture
def runner():
    return CliRunner()


def test_manifest_loads_77_modules():
    modules = load_manifest()
    assert len(modules) == 77


def test_resolve_module_accepts_hyphen_and_underscore():
    modules = load_manifest()
    assert resolve_module("helix-filter", modules) is not None
    assert resolve_module("helix_filter", modules) is not None
    assert resolve_module("nonexistent", modules) is None


def test_cli_list(runner):
    result = runner.invoke(main, ["list"])
    assert result.exit_code == 0
    assert "helix-filter" in result.output
    assert "77 módulos" in result.output


def test_cli_list_json(runner):
    result = runner.invoke(main, ["list", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 77


def test_cli_info(runner):
    result = runner.invoke(main, ["info", "helix-filter", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["display_name"] == "Helix Filter"
    assert payload["info"]["status"] == "Production"


def test_cli_run_helix_filter(runner):
    result = runner.invoke(
        main,
        ["run", "helix-filter", "--iocs", "evil-snake-oil.com,google.com", "--json"],
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["result"]["status"] in {"success", "warning", "error"}


def test_cli_run_default_analyze():
    modules = load_manifest()
    meta = resolve_module("tesseract_covenant", modules)
    assert meta is not None
    payload = run_analyze(meta)
    assert "result" in payload
    assert payload["result"]["status"]


def test_cli_run_info():
    modules = load_manifest()
    meta = resolve_module("simplex_secret", modules)
    assert meta is not None
    info = run_info(meta)
    assert info["status"] == "Production"


def test_cli_pipeline_safe(runner):
    result = runner.invoke(
        main,
        ["pipeline", "--urls", "google.com,github.com", "--content", "test@example.com", "--json"],
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["status"] == "SAFE"


def test_cli_pipeline_blocked(runner):
    result = runner.invoke(
        main,
        ["pipeline", "--urls", "evil-snake-oil.com", "--content", "ignored", "--json"],
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["status"] == "BLOCKED"


def test_cli_unknown_module(runner):
    result = runner.invoke(main, ["run", "no-such-module"])
    assert result.exit_code == 1
    assert "no encontrado" in result.output.lower()


def test_cli_domains(runner):
    result = runner.invoke(main, ["domains"])
    assert result.exit_code == 0
    assert "threat-intel" in result.output


def test_cli_posture(runner):
    result = runner.invoke(main, ["posture", "--json"])
    assert result.exit_code == 0
    report = json.loads(result.output)
    assert report["report_type"] == "infrastructure_security_posture"
    assert report["summary"]["total_checks"] == 17
    assert "posture_level" in report
    assert "overall_score" in report


def test_cli_posture_output_file(runner, tmp_path):
    out = tmp_path / "posture.json"
    result = runner.invoke(main, ["posture", "--output", str(out)])
    assert result.exit_code == 0
    assert out.exists()
    report = json.loads(out.read_text())
    assert len(report["checks"]) == 17
