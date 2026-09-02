"""Tests for KDE Theme & Look-and-Feel Controller."""

from pathlib import Path
from typer.testing import CliRunner

from krice.cli import app
from krice.theme_ctl import ThemeController

runner = CliRunner()


def test_theme_controller_initialization(tmp_path: Path) -> None:
    home_dir = tmp_path / "user"
    home_dir.mkdir()
    config_dir = home_dir / ".config"
    config_dir.mkdir()

    theme_ctl = ThemeController(dry_run=False, home_dir=home_dir)
    assert theme_ctl.home == home_dir
    assert theme_ctl.kdeglobals == config_dir / "kdeglobals"
    assert theme_ctl.kwinrc == config_dir / "kwinrc"


def test_theme_controller_features(tmp_path: Path) -> None:
    home_dir = tmp_path / "user"
    home_dir.mkdir()
    config_dir = home_dir / ".config"
    config_dir.mkdir()
    (config_dir / "kdeglobals").write_text("[KDE]\nLookAndFeelPackage=com.github.vinceliuice.Orchis\nwidgetStyle=Breeze\n")
    (config_dir / "kwinrc").write_text("[org.kde.kdecoration2]\nlibrary=org.kde.breeze\ntheme=Breeze\n")

    theme_ctl = ThemeController(dry_run=False, home_dir=home_dir)
    assert theme_ctl.get_current_global_theme() == "com.github.vinceliuice.Orchis"
    assert theme_ctl.get_current_widget_style() == "Breeze"
    lib, _ = theme_ctl.get_window_decoration()
    assert lib == "org.kde.breeze"


def test_theme_cli_commands() -> None:
    # 1. List
    res_list = runner.invoke(app, ["theme", "list"])
    assert res_list.exit_code == 0
    assert "cachy-nord" in res_list.output
    assert "catppuccin-mocha" in res_list.output

    # 2. Apply with dry-run
    res_apply = runner.invoke(app, ["theme", "apply", "cachy-nord", "--dry-run"])
    assert res_apply.exit_code == 0
    assert "正在应用全局桌面方案" in res_apply.output
    assert "全局外观" in res_apply.output
    assert "控件样式" in res_apply.output

    # 3. Granular commands
    res_ws = runner.invoke(app, ["theme", "widget-styles"])
    assert res_ws.exit_code == 0

    res_kv = runner.invoke(app, ["theme", "kvantum-themes"])
    assert res_kv.exit_code == 0

    res_deco = runner.invoke(app, ["theme", "decorations"])
    assert res_deco.exit_code == 0

    res_fonts = runner.invoke(app, ["theme", "fonts"])
    assert res_fonts.exit_code == 0

    res_colors = runner.invoke(app, ["theme", "colors"])
    assert res_colors.exit_code == 0
