"""Tests for expanded KDE Theming Controller & CLI commands."""

from pathlib import Path
from typer.testing import CliRunner

from krice.cli import app
from krice.presets.theme_presets import RICE_PRESETS
from krice.theme_ctl import ThemeController

runner = CliRunner()


def test_theme_presets_rich_catalog() -> None:
    assert len(RICE_PRESETS) >= 10
    assert "cachy-nord" in RICE_PRESETS
    assert "catppuccin-mocha" in RICE_PRESETS
    assert "catppuccin-latte" in RICE_PRESETS
    assert "tokyo-night" in RICE_PRESETS
    assert "dracula" in RICE_PRESETS
    assert "gruvbox-dark" in RICE_PRESETS
    assert "orchis-dark" in RICE_PRESETS

    cachy = RICE_PRESETS["cachy-nord"]
    assert cachy.widget_style == "kvantum"
    assert cachy.kvantum_theme == "Nordic"
    assert cachy.terminal_palette == "cachy-nord"
    assert cachy.motion_preset == "denial"


def test_theme_controller_features(tmp_path: Path) -> None:
    home_dir = tmp_path / "user"
    home_dir.mkdir()
    theme_ctl = ThemeController(dry_run=False, home_dir=home_dir)

    # 1. Widget style list & apply
    styles = theme_ctl.list_widget_styles()
    assert "Breeze" in styles

    ok_ws, _ = theme_ctl.apply_widget_style("kvantum")
    assert ok_ws is True
    assert theme_ctl.get_current_widget_style() == "kvantum"

    # 2. Kvantum apply
    ok_kv, _ = theme_ctl.apply_kvantum_theme("Nordic")
    assert ok_kv is True
    assert theme_ctl.get_current_kvantum_theme() == "Nordic"

    # 3. Klassy configure
    ok_kl, _ = theme_ctl.configure_klassy(corner_radius=12, blur=True)
    assert ok_kl is True

    # 4. GTK sync
    ok_gtk, _ = theme_ctl.sync_gtk_theme(gtk_theme="Nordic", dark_mode=True)
    assert ok_gtk is True
    assert theme_ctl.get_gtk_theme() == "Nordic"

    # 5. Fonts
    fonts = theme_ctl.get_fonts()
    assert "General" in fonts

    # 6. Splash
    ok_sp, _ = theme_ctl.apply_splash_theme("org.kde.breeze.desktop")
    assert ok_sp is True
    curr_sp, _ = theme_ctl.get_current_splash()
    assert curr_sp == "org.kde.breeze.desktop"


def test_theme_cli_commands() -> None:
    # 1. List
    res_list = runner.invoke(app, ["theme", "list"])
    assert res_list.exit_code == 0
    assert "cachy-nord" in res_list.output
    assert "catppuccin-mocha" in res_list.output

    # 2. Apply with dry-run
    res_apply = runner.invoke(app, ["theme", "apply", "cachy-nord", "--dry-run"])
    assert res_apply.exit_code == 0
    assert "Applying Unified Style" in res_apply.output
    assert "Global Theme" in res_apply.output
    assert "Widget Style" in res_apply.output

    # 3. Granular commands
    res_ws = runner.invoke(app, ["theme", "widget-styles"])
    assert res_ws.exit_code == 0

    res_kv = runner.invoke(app, ["theme", "kvantum-themes"])
    assert res_kv.exit_code == 0

    res_deco = runner.invoke(app, ["theme", "decorations"])
    assert res_deco.exit_code == 0

    res_fonts = runner.invoke(app, ["theme", "fonts"])
    assert res_fonts.exit_code == 0

    res_splash = runner.invoke(app, ["theme", "splash"])
    assert res_splash.exit_code == 0

    res_gtk = runner.invoke(app, ["theme", "gtk"])
    assert res_gtk.exit_code == 0

    res_sync_gtk = runner.invoke(app, ["theme", "sync-gtk", "--dry-run"])
    assert res_sync_gtk.exit_code == 0

    res_pal = runner.invoke(app, ["theme", "palette"])
    assert res_pal.exit_code == 0
    assert "Active KDE Color Palette Summary" in res_pal.output
