"""Smoke tests for krice CLI, theming, and core modules."""

from pathlib import Path
from typer.testing import CliRunner

from krice.cli import app
from krice.presets.builtin_presets import PRESETS as MOTION_PRESETS
from krice.presets.theme_presets import RICE_PRESETS
from krice.snapshot import SnapshotManager
from krice.theme_ctl import ThemeController

runner = CliRunner()


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "krice" in result.output
    assert "theme" in result.output
    assert "motion" in result.output
    assert "snapshot" in result.output


def test_status_dashboard() -> None:
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Active Theme" in result.output or "KWin Motion" in result.output


def test_theme_commands() -> None:
    result_list = runner.invoke(app, ["theme", "list"])
    assert result_list.exit_code == 0
    assert "cachy-nord" in result_list.output

    result_colors = runner.invoke(app, ["theme", "colors"])
    assert result_colors.exit_code == 0

    result_dry_run = runner.invoke(app, ["theme", "apply", "cachy-nord", "--dry-run"])
    assert result_dry_run.exit_code == 0
    assert "Applying Unified Style" in result_dry_run.output


def test_motion_presets_validity() -> None:
    assert "denial" in MOTION_PRESETS
    denial = MOTION_PRESETS["denial"]
    assert "scale" in denial.enabled_plugins
    assert "fade" in denial.disabled_plugins


def test_snapshot_roundtrip(tmp_path: Path) -> None:
    manager = SnapshotManager(dry_run=True)
    out_file = tmp_path / "test.pmz"
    created = manager.create_snapshot(output_path=out_file, name="unit-test")
    assert created.exists()

    info = manager.inspect_snapshot(created)
    assert info["name"] == "unit-test"
    assert "files" in info
