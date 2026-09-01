"""Smoke tests for krice CLI, theming, terminal sync, and core modules."""

from pathlib import Path
from typer.testing import CliRunner

from krice.cli import app
from krice.presets.builtin_presets import PRESETS as MOTION_PRESETS
from krice.presets.terminal_palettes import TERMINAL_PALETTES
from krice.presets.theme_presets import RICE_PRESETS
from krice.snapshot import SnapshotManager
from krice.theme_ctl import ThemeController

runner = CliRunner()


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "krice" in result.output
    assert "theme" in result.output
    assert "terminal" in result.output
    assert "motion" in result.output
    assert "snapshot" in result.output


def test_status_dashboard() -> None:
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Active KDE Theme" in result.output or "Active Theme" in result.output
    assert "Terminal & Shell Tooling" in result.output


def test_check_deps() -> None:
    result = runner.invoke(app, ["check-deps"])
    assert result.exit_code == 0
    assert "klassy-qt6" in result.output
    assert "starship" in result.output
    assert "fastfetch" in result.output


def test_theme_commands() -> None:
    result_list = runner.invoke(app, ["theme", "list"])
    assert result_list.exit_code == 0
    assert "cachy-nord" in result_list.output
    assert "catppuccin-mocha" in result_list.output

    result_colors = runner.invoke(app, ["theme", "colors"])
    assert result_colors.exit_code == 0

    result_dry_run = runner.invoke(app, ["theme", "apply", "cachy-nord", "--dry-run"])
    assert result_dry_run.exit_code == 0
    assert "Applying Unified Style" in result_dry_run.output
    assert "Synchronizing Terminal Themes" in result_dry_run.output


def test_terminal_commands() -> None:
    result_list = runner.invoke(app, ["terminal", "list"])
    assert result_list.exit_code == 0
    assert "cachy-nord" in result_list.output

    result_apply = runner.invoke(app, ["terminal", "apply", "cachy-nord", "--dry-run"])
    assert result_apply.exit_code == 0
    assert "Applying Terminal Palette" in result_apply.output


def test_motion_presets_validity() -> None:
    assert "denial" in MOTION_PRESETS
    denial = MOTION_PRESETS["denial"]
    assert "scale" in denial.enabled_plugins
    assert "fade" in denial.disabled_plugins


def test_snapshot_roundtrip(tmp_path: Path) -> None:
    home_dir = tmp_path / "user"
    home_dir.mkdir()
    config_dir = home_dir / ".config"
    config_dir.mkdir()
    (config_dir / "kwinrc").write_text("[Plugins]\nscaleEnabled=true\n")
    (config_dir / "alacritty").mkdir()
    (config_dir / "alacritty" / "alacritty.toml").write_text("[window]\n")

    manager = SnapshotManager(dry_run=False, home_dir=home_dir)
    out_file = tmp_path / "test.pmz"
    created = manager.create_snapshot(output_path=out_file, name="unit-test")
    assert created.exists()

    info = manager.inspect_snapshot(created)
    assert info["name"] == "unit-test"
    assert "files" in info
    assert any("kwinrc" in f for f in info["files"])
    assert any("alacritty" in f for f in info["files"])
