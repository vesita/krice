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
    assert "KDE" in result.output
    assert "终端" in result.output or "Terminal" in result.output


def test_check_deps() -> None:
    result = runner.invoke(app, ["check-deps"])
    assert result.exit_code == 0
    assert "kitty" in result.output
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
    assert "正在应用全局桌面方案" in result_dry_run.output


def test_terminal_commands() -> None:
    result_list = runner.invoke(app, ["terminal", "list"])
    assert result_list.exit_code == 0
    assert "cachy-nord" in result_list.output

    result_apply = runner.invoke(app, ["terminal", "apply", "cachy-nord", "--dry-run"])
    assert result_apply.exit_code == 0
    assert "正在应用终端调色板" in result_apply.output


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
    (config_dir / "kitty").mkdir()
    (config_dir / "kitty" / "kitty.conf").write_text("# kitty config\n")

    manager = SnapshotManager(dry_run=False, home_dir=home_dir)
    out_file = tmp_path / "test.pmz"
    created = manager.create_snapshot(output_path=out_file, name="unit-test")
    assert created.exists()

    info = manager.inspect_snapshot(created)
    assert info["name"] == "unit-test"
    assert "files" in info
    assert any("kwinrc" in f for f in info["files"])
    assert any("kitty" in f for f in info["files"])


def test_snapshot_niri_support(tmp_path: Path) -> None:
    home_dir = tmp_path / "user"
    home_dir.mkdir()
    config_dir = home_dir / ".config"
    config_dir.mkdir()
    (config_dir / "niri").mkdir()
    (config_dir / "niri" / "config.kdl").write_text("// niri config\n")
    (config_dir / "waybar").mkdir()
    (config_dir / "waybar" / "config.jsonc").write_text("{}\n")
    (home_dir / ".vscode").mkdir()
    (home_dir / ".vscode" / "argv.json").write_text('{"password-store": "basic"}\n')

    manager = SnapshotManager(dry_run=False, home_dir=home_dir)
    out_file = tmp_path / "niri_test.pmz"
    created = manager.create_snapshot(output_path=out_file, name="niri-test")
    assert created.exists()

    info = manager.inspect_snapshot(created)
    assert info["name"] == "niri-test"
    assert any("niri" in f for f in info["files"])
    assert any("waybar" in f for f in info["files"])
    assert any("argv.json" in f for f in info["files"])
