"""Tests for Terminal & Shell Prompt Theming Controller."""

from pathlib import Path
from typer.testing import CliRunner

from krice.cli import app
from krice.presets.prompt_presets import generate_fastfetch_config, generate_starship_config
from krice.presets.terminal_palettes import CACHY_NORD, NORD_LIGHT, TERMINAL_PALETTES, TerminalPalette
from krice.terminal_ctl import TerminalController, hex_to_rgb, parse_kde_rgb, rgb_to_hex

runner = CliRunner()


def test_color_utilities() -> None:
    assert hex_to_rgb("#FFFFFF") == (255, 255, 255)
    assert hex_to_rgb("#000000") == (0, 0, 0)
    assert hex_to_rgb("#2E3440") == (46, 52, 64)
    assert hex_to_rgb("#FFF") == (255, 255, 255)

    assert rgb_to_hex(46, 52, 64) == "#2E3440"
    assert parse_kde_rgb("46,52,64") == "#2E3440"
    assert parse_kde_rgb("invalid", "#123456") == "#123456"


def test_terminal_palettes_catalog() -> None:
    assert "cachy-nord" in TERMINAL_PALETTES
    assert "catppuccin-mocha" in TERMINAL_PALETTES
    assert "tokyo-night" in TERMINAL_PALETTES
    assert "dracula" in TERMINAL_PALETTES
    assert "gruvbox-dark" in TERMINAL_PALETTES

    nord = TERMINAL_PALETTES["cachy-nord"]
    assert nord.is_dark is True
    ansi = nord.to_ansi_list()
    assert len(ansi) == 16
    assert ansi[0] == nord.black
    assert ansi[15] == nord.bright_white


def test_prompt_generators() -> None:
    starship_cfg = generate_starship_config(CACHY_NORD)
    assert "directory" in starship_cfg
    assert "git_branch" in starship_cfg
    assert CACHY_NORD.cyan in starship_cfg or CACHY_NORD.blue in starship_cfg

    fastfetch_cfg = generate_fastfetch_config(NORD_LIGHT)
    assert "logo" in fastfetch_cfg
    assert "modules" in fastfetch_cfg


def test_terminal_controller_file_generation(tmp_path: Path) -> None:
    home_dir = tmp_path / "user"
    home_dir.mkdir()
    term_ctl = TerminalController(dry_run=False, home_dir=home_dir)

    # 1. Test Konsole apply
    ok, msg = term_ctl.apply_konsole(CACHY_NORD)
    assert ok is True
    scheme_file = term_ctl.data_dir / "konsole" / f"krice-{CACHY_NORD.name}.colorscheme"
    assert scheme_file.exists()
    assert "[Background]" in scheme_file.read_text()
    assert (term_ctl.config_dir / "konsolerc").exists()

    # 2. Test Alacritty apply
    ok, msg = term_ctl.apply_alacritty(CACHY_NORD)
    assert ok is True
    alacritty_file = term_ctl.config_dir / "alacritty" / "alacritty.toml"
    assert alacritty_file.exists()
    alacritty_txt = alacritty_file.read_text()
    assert "[colors.primary]" in alacritty_txt
    assert CACHY_NORD.background in alacritty_txt

    # 3. Test Kitty apply
    ok, msg = term_ctl.apply_kitty(CACHY_NORD)
    assert ok is True
    kitty_theme = term_ctl.config_dir / "kitty" / "current-theme.conf"
    assert kitty_theme.exists()
    assert f"background {CACHY_NORD.background}" in kitty_theme.read_text()

    # 4. Test Ghostty apply
    ok, msg = term_ctl.apply_ghostty(CACHY_NORD)
    assert ok is True
    ghostty_theme = term_ctl.config_dir / "ghostty" / "themes" / f"krice-{CACHY_NORD.name}"
    assert ghostty_theme.exists()

    # 5. Test Foot apply
    ok, msg = term_ctl.apply_foot(CACHY_NORD)
    assert ok is True
    foot_cfg = term_ctl.config_dir / "foot" / "foot.ini"
    assert foot_cfg.exists()
    assert "[colors]" in foot_cfg.read_text()

    # 6. Test WezTerm apply
    ok, msg = term_ctl.apply_wezterm(CACHY_NORD)
    assert ok is True
    wezterm_theme = term_ctl.config_dir / "wezterm" / "colors" / f"krice-{CACHY_NORD.name}.toml"
    assert wezterm_theme.exists()

    # 7. Test Starship & Fastfetch
    ok_s, _ = term_ctl.apply_starship(CACHY_NORD)
    assert ok_s is True
    assert (term_ctl.config_dir / "starship.toml").exists()

    ok_f, _ = term_ctl.apply_fastfetch(CACHY_NORD)
    assert ok_f is True
    assert (term_ctl.config_dir / "fastfetch" / "config.jsonc").exists()


def test_extract_palette_from_mock_kde(tmp_path: Path) -> None:
    home_dir = tmp_path / "user"
    home_dir.mkdir()
    config_dir = home_dir / ".config"
    config_dir.mkdir(parents=True)
    kdeglobals = config_dir / "kdeglobals"
    kdeglobals.write_text("""[Colors:Window]
BackgroundNormal=33,37,43
ForegroundNormal=171,178,191

[Colors:Selection]
BackgroundNormal=97,175,239
ForegroundNormal=255,255,255

[Colors:Button]
BackgroundNormal=40,44,52
ForegroundNormal=171,178,191
""")
    term_ctl = TerminalController(dry_run=False, home_dir=home_dir)
    extracted = term_ctl.extract_palette_from_kde()
    assert extracted.background == "#21252B"
    assert extracted.foreground == "#ABB2BF"
    assert extracted.blue == "#61AFEF"
    assert extracted.is_dark is True


def test_terminal_cli_commands() -> None:
    res_list = runner.invoke(app, ["terminal", "list"])
    assert res_list.exit_code == 0
    assert "cachy-nord" in res_list.output
    assert "catppuccin-mocha" in res_list.output

    res_apply = runner.invoke(app, ["terminal", "apply", "cachy-nord", "--dry-run"])
    assert res_apply.exit_code == 0
    assert "Applying Terminal Palette" in res_apply.output

    res_sync = runner.invoke(app, ["terminal", "sync", "--dry-run"])
    assert res_sync.exit_code == 0
    assert "Dynamically Synthesizing Palette" in res_sync.output

    res_export = runner.invoke(app, ["terminal", "export-palette", "dracula"])
    assert res_export.exit_code == 0
    assert "Dracula" in res_export.output

    res_konsole = runner.invoke(app, ["terminal", "set-konsole", "cachy-nord", "--dry-run"])
    assert res_konsole.exit_code == 0
