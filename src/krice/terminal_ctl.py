"""Terminal & Shell Prompt Theming Controller for krice."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Union

from krice.presets.prompt_presets import generate_fastfetch_config, generate_starship_config
from krice.presets.terminal_palettes import TERMINAL_PALETTES, TerminalPalette


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Converts #RRGGBB to (r, g, b)."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join([c * 2 for c in hex_str])
    return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Converts (r, g, b) to #RRGGBB."""
    return f"#{max(0, min(255, r)):02X}{max(0, min(255, g)):02X}{max(0, min(255, b)):02X}"


def parse_kde_rgb(val: str, default_hex: str = "#000000") -> str:
    """Parses KDE 'r,g,b' string to #RRGGBB."""
    try:
        parts = [int(p.strip()) for p in val.split(",") if p.strip()]
        if len(parts) >= 3:
            return rgb_to_hex(parts[0], parts[1], parts[2])
    except Exception:
        pass
    return default_hex


class TerminalController:
    """Manages color themes and synchronization for terminal emulators and CLI prompt tools."""

    def __init__(self, dry_run: bool = False, home_dir: Optional[Path] = None) -> None:
        self.dry_run = dry_run
        self.home = home_dir or Path.home()
        self.config_dir = Path(os.environ.get("XDG_CONFIG_HOME", str(self.home / ".config")))
        self.data_dir = Path(os.environ.get("XDG_DATA_HOME", str(self.home / ".local" / "share")))

    # --- Palettes Discovery ---

    def list_palettes(self) -> list[str]:
        """Returns list of built-in terminal palette names."""
        return sorted(list(TERMINAL_PALETTES.keys()))

    def get_palette(self, name: str) -> Optional[TerminalPalette]:
        """Retrieves a palette by name."""
        return TERMINAL_PALETTES.get(name)

    # --- Active KDE Color Scheme -> Terminal Palette Synthesis ---

    def extract_palette_from_kde(self) -> TerminalPalette:
        """Extracts colors from current kdeglobals / KDE color scheme and synthesizes a TerminalPalette."""
        kdeglobals = self.config_dir / "kdeglobals"
        bg = "#2E3440"
        fg = "#ECEFF4"
        sel_bg = "#5E81AC"
        sel_fg = "#ECEFF4"
        btn_bg = "#3B4252"
        btn_fg = "#D8DEE9"

        if kdeglobals.exists():
            content = kdeglobals.read_text(encoding="utf-8", errors="ignore")
            # Parse [Colors:Window] BackgroundNormal
            m_bg = re.search(r"\[Colors:Window\][^\[]*?BackgroundNormal=([0-9, ]+)", content)
            if m_bg:
                bg = parse_kde_rgb(m_bg.group(1), bg)

            m_fg = re.search(r"\[Colors:Window\][^\[]*?ForegroundNormal=([0-9, ]+)", content)
            if m_fg:
                fg = parse_kde_rgb(m_fg.group(1), fg)

            m_sel_bg = re.search(r"\[Colors:Selection\][^\[]*?BackgroundNormal=([0-9, ]+)", content)
            if m_sel_bg:
                sel_bg = parse_kde_rgb(m_sel_bg.group(1), sel_bg)

            m_sel_fg = re.search(r"\[Colors:Selection\][^\[]*?ForegroundNormal=([0-9, ]+)", content)
            if m_sel_fg:
                sel_fg = parse_kde_rgb(m_sel_fg.group(1), sel_fg)

            m_btn_bg = re.search(r"\[Colors:Button\][^\[]*?BackgroundNormal=([0-9, ]+)", content)
            if m_btn_bg:
                btn_bg = parse_kde_rgb(m_btn_bg.group(1), btn_bg)

            m_btn_fg = re.search(r"\[Colors:Button\][^\[]*?ForegroundNormal=([0-9, ]+)", content)
            if m_btn_fg:
                btn_fg = parse_kde_rgb(m_btn_fg.group(1), btn_fg)

        # Determine light or dark
        r, g, b = hex_to_rgb(bg)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        is_dark = luminance < 128

        # Synthesize harmonious ANSI colors based on accent and background
        if is_dark:
            red = "#BF616A"
            green = "#A3BE8C"
            yellow = "#EBCB8B"
            blue = sel_bg
            magenta = "#B48EAD"
            cyan = "#88C0D0"
            black = btn_bg
            white = fg
            bright_black = "#555E70"
            bright_red = "#D08770"
            bright_green = "#8FBCBB"
            bright_yellow = "#EBCB8B"
            bright_blue = sel_bg
            bright_magenta = "#B48EAD"
            bright_cyan = "#8FBCBB"
            bright_white = "#FFFFFF"
        else:
            red = "#BF616A"
            green = "#8FBCBB"
            yellow = "#D08770"
            blue = sel_bg
            magenta = "#B48EAD"
            cyan = "#88C0D0"
            black = fg
            white = btn_bg
            bright_black = "#4C566A"
            bright_red = "#A9555E"
            bright_green = "#7EABA0"
            bright_yellow = "#C27A63"
            bright_blue = sel_bg
            bright_magenta = "#A07C9A"
            bright_cyan = "#6E9FA7"
            bright_white = bg

        return TerminalPalette(
            name="kde-extracted",
            display_name="Extracted from KDE Theme",
            background=bg,
            foreground=fg,
            dim_foreground=bright_black,
            bright_foreground=bright_white,
            cursor=sel_bg,
            cursor_text=bg,
            selection_bg=sel_bg,
            selection_fg=sel_fg,
            black=black,
            red=red,
            green=green,
            yellow=yellow,
            blue=blue,
            magenta=magenta,
            cyan=cyan,
            white=white,
            bright_black=bright_black,
            bright_red=bright_red,
            bright_green=bright_green,
            bright_yellow=bright_yellow,
            bright_blue=bright_blue,
            bright_magenta=bright_magenta,
            bright_cyan=bright_cyan,
            bright_white=bright_white,
            is_dark=is_dark,
        )

    # --- Terminal Detection ---

    def detect_installed_terminals(self) -> dict[str, bool]:
        """Detects which terminal emulators and CLI tools are installed or configured."""
        return {
            "konsole": shutil.which("konsole") is not None or (self.config_dir / "konsolerc").exists(),
            "alacritty": shutil.which("alacritty") is not None or (self.config_dir / "alacritty").exists(),
            "kitty": shutil.which("kitty") is not None or (self.config_dir / "kitty").exists(),
            "ghostty": shutil.which("ghostty") is not None or (self.config_dir / "ghostty").exists(),
            "foot": shutil.which("foot") is not None or (self.config_dir / "foot").exists(),
            "wezterm": shutil.which("wezterm") is not None or (self.config_dir / "wezterm").exists(),
            "zellij": shutil.which("zellij") is not None or (self.config_dir / "zellij").exists(),
            "starship": shutil.which("starship") is not None or (self.home / ".local" / "bin" / "starship").exists() or (self.config_dir / "starship.toml").exists(),
            "fastfetch": shutil.which("fastfetch") is not None or (self.config_dir / "fastfetch").exists(),
        }
    # --- Terminal Applications Application Logic ---

    # 1. Konsole (KDE Native)
    def apply_konsole(self, palette: TerminalPalette) -> tuple[bool, str]:
        """Applies theme to KDE Konsole by writing colorscheme and updating konsolerc / profiles."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply Konsole color scheme: krice-{palette.name}"

        scheme_dir = self.data_dir / "konsole"
        scheme_dir.mkdir(parents=True, exist_ok=True)
        scheme_file = scheme_dir / f"krice-{palette.name}.colorscheme"

        # Convert hex to RGB for Konsole format
        def hex_rgb_str(hex_val: str) -> str:
            r, g, b = hex_to_rgb(hex_val)
            return f"{r},{g},{b}"

        lines = [
            "[General]",
            f"Description=krice {palette.display_name}",
            "Blur=true",
            "Opacity=0.94",
            "",
            "[Background]",
            f"Color={hex_rgb_str(palette.background)}",
            "",
            "[Foreground]",
            f"Color={hex_rgb_str(palette.foreground)}",
            "",
            "[BackgroundIntense]",
            f"Color={hex_rgb_str(palette.background)}",
            "",
            "[ForegroundIntense]",
            f"Color={hex_rgb_str(palette.bright_foreground)}",
            "",
            "[Color0]",
            f"Color={hex_rgb_str(palette.black)}",
            "[Color1]",
            f"Color={hex_rgb_str(palette.red)}",
            "[Color2]",
            f"Color={hex_rgb_str(palette.green)}",
            "[Color3]",
            f"Color={hex_rgb_str(palette.yellow)}",
            "[Color4]",
            f"Color={hex_rgb_str(palette.blue)}",
            "[Color5]",
            f"Color={hex_rgb_str(palette.magenta)}",
            "[Color6]",
            f"Color={hex_rgb_str(palette.cyan)}",
            "[Color7]",
            f"Color={hex_rgb_str(palette.white)}",
            "[Color0Intense]",
            f"Color={hex_rgb_str(palette.bright_black)}",
            "[Color1Intense]",
            f"Color={hex_rgb_str(palette.bright_red)}",
            "[Color2Intense]",
            f"Color={hex_rgb_str(palette.bright_green)}",
            "[Color3Intense]",
            f"Color={hex_rgb_str(palette.bright_yellow)}",
            "[Color4Intense]",
            f"Color={hex_rgb_str(palette.bright_blue)}",
            "[Color5Intense]",
            f"Color={hex_rgb_str(palette.bright_magenta)}",
            "[Color6Intense]",
            f"Color={hex_rgb_str(palette.bright_cyan)}",
            "[Color7Intense]",
            f"Color={hex_rgb_str(palette.bright_white)}",
            "",
        ]
        try:
            scheme_file.write_text("\n".join(lines), encoding="utf-8")
        except Exception as e:
            return False, f"Failed to write Konsole colorscheme: {e}"

        # Update ~/.config/konsolerc
        konsolerc = self.config_dir / "konsolerc"
        try:
            if konsolerc.exists():
                content = konsolerc.read_text(encoding="utf-8")
                if "[UiSettings]" in content:
                    content = re.sub(r"ColorScheme=.*", f"ColorScheme=krice-{palette.name}", content)
                    if "ColorScheme=" not in content:
                        content = content.replace("[UiSettings]", f"[UiSettings]\nColorScheme=krice-{palette.name}")
                else:
                    content += f"\n[UiSettings]\nColorScheme=krice-{palette.name}\n"
                konsolerc.write_text(content, encoding="utf-8")
            else:
                konsolerc.parent.mkdir(parents=True, exist_ok=True)
                konsolerc.write_text(f"[UiSettings]\nColorScheme=krice-{palette.name}\n", encoding="utf-8")
        except Exception as e:
            return False, f"Failed to update konsolerc: {e}"

        # Update default profiles in ~/.local/share/konsole/*.profile
        for prof in scheme_dir.glob("*.profile"):
            try:
                txt = prof.read_text(encoding="utf-8")
                if "[Appearance]" in txt:
                    txt = re.sub(r"ColorScheme=.*", f"ColorScheme=krice-{palette.name}", txt)
                else:
                    txt += f"\n[Appearance]\nColorScheme=krice-{palette.name}\n"
                prof.write_text(txt, encoding="utf-8")
            except Exception:
                pass

        return True, f"Konsole theme set to 'krice-{palette.name}'."

    # 2. Alacritty
    def apply_alacritty(self, palette: TerminalPalette) -> tuple[bool, str]:
        """Applies theme to Alacritty by updating alacritty.toml [colors] section."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply Alacritty color theme: {palette.name}"

        alacritty_dir = self.config_dir / "alacritty"
        alacritty_dir.mkdir(parents=True, exist_ok=True)
        config_path = alacritty_dir / "alacritty.toml"

        colors_toml = f"""[colors.primary]
background = "{palette.background}"
foreground = "{palette.foreground}"
dim_foreground = "{palette.dim_foreground}"
bright_foreground = "{palette.bright_foreground}"

[colors.cursor]
text = "{palette.cursor_text}"
cursor = "{palette.cursor}"

[colors.vi_mode_cursor]
text = "{palette.cursor_text}"
cursor = "{palette.bright_red}"

[colors.search.matches]
foreground = "{palette.cursor_text}"
background = "{palette.blue}"

[colors.search.focused_match]
foreground = "{palette.cursor_text}"
background = "{palette.cyan}"

[colors.footer_bar]
background = "{palette.selection_bg}"
foreground = "{palette.foreground}"

[colors.hints.start]
foreground = "{palette.cursor_text}"
background = "{palette.yellow}"

[colors.hints.end]
foreground = "{palette.cursor_text}"
background = "{palette.red}"

[colors.selection]
text = "{palette.selection_fg}"
background = "{palette.selection_bg}"

[colors.normal]
black = "{palette.black}"
red = "{palette.red}"
green = "{palette.green}"
yellow = "{palette.yellow}"
blue = "{palette.blue}"
magenta = "{palette.magenta}"
cyan = "{palette.cyan}"
white = "{palette.white}"

[colors.bright]
black = "{palette.bright_black}"
red = "{palette.bright_red}"
green = "{palette.bright_green}"
yellow = "{palette.bright_yellow}"
blue = "{palette.bright_blue}"
magenta = "{palette.bright_magenta}"
cyan = "{palette.bright_cyan}"
white = "{palette.bright_white}"

[colors.dim]
black = "{palette.bright_black}"
red = "{palette.bright_red}"
green = "{palette.bright_green}"
yellow = "{palette.bright_yellow}"
blue = "{palette.bright_blue}"
magenta = "{palette.bright_magenta}"
cyan = "{palette.bright_cyan}"
white = "{palette.bright_white}"
"""

        try:
            if config_path.exists():
                content = config_path.read_text(encoding="utf-8")
                # Remove any existing [colors...] tables
                # Split at first [colors and rejoin before next top-level table or append
                cleaned = re.sub(r"\[colors[\s\S]*?(?=\n\[(?!colors)|$)", "", content).strip()
                new_content = cleaned + "\n\n# --- Colors auto-configured by krice ---\n[colors]\ndraw_bold_text_with_bright_colors = true\n\n" + colors_toml
                config_path.write_text(new_content, encoding="utf-8")
            else:
                # Create standard modern Alacritty config
                default_tmpl = f"""# Alacritty Configuration - Managed by krice

[general]
live_config_reload = true

[window]
dimensions = {{ columns = 110, lines = 32 }}
padding = {{ x = 14, y = 12 }}
opacity = 0.94
blur = true
decorations = "Full"

[font]
size = 11.5

[colors]
draw_bold_text_with_bright_colors = true

{colors_toml}
"""
                config_path.write_text(default_tmpl, encoding="utf-8")

            return True, f"Alacritty color theme set to '{palette.name}'."
        except Exception as e:
            return False, f"Failed to update Alacritty theme: {e}"

    # 3. Kitty
    def apply_kitty(self, palette: TerminalPalette) -> tuple[bool, str]:
        """Applies theme to Kitty terminal."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply Kitty color theme: {palette.name}"

        kitty_dir = self.config_dir / "kitty"
        kitty_dir.mkdir(parents=True, exist_ok=True)
        theme_file = kitty_dir / "current-theme.conf"
        main_config = kitty_dir / "kitty.conf"

        theme_content = f"""# Kitty theme - Managed by krice for {palette.display_name}
background {palette.background}
foreground {palette.foreground}
selection_background {palette.selection_bg}
selection_foreground {palette.selection_fg}
cursor {palette.cursor}
cursor_text_color {palette.cursor_text}

# 16 ANSI colors
color0 {palette.black}
color1 {palette.red}
color2 {palette.green}
color3 {palette.yellow}
color4 {palette.blue}
color5 {palette.magenta}
color6 {palette.cyan}
color7 {palette.white}
color8 {palette.bright_black}
color9 {palette.bright_red}
color10 {palette.bright_green}
color11 {palette.bright_yellow}
color12 {palette.bright_blue}
color13 {palette.bright_magenta}
color14 {palette.bright_cyan}
color15 {palette.bright_white}
"""
        try:
            theme_file.write_text(theme_content, encoding="utf-8")
            if main_config.exists():
                main_txt = main_config.read_text(encoding="utf-8")
                if "include current-theme.conf" not in main_txt:
                    main_config.write_text(main_txt + "\ninclude current-theme.conf\n", encoding="utf-8")
            else:
                main_config.write_text("include current-theme.conf\nbackground_opacity 0.94\n", encoding="utf-8")

            # Signal Kitty if running
            try:
                subprocess.run(["pkill", "-USR1", "kitty"], check=False, capture_output=True)
            except Exception:
                pass

            return True, f"Kitty color theme set to '{palette.name}'."
        except Exception as e:
            return False, f"Failed to update Kitty theme: {e}"

    # 4. Ghostty
    def apply_ghostty(self, palette: TerminalPalette) -> tuple[bool, str]:
        """Applies theme to Ghostty terminal."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply Ghostty color theme: {palette.name}"

        ghostty_dir = self.config_dir / "ghostty"
        ghostty_themes = ghostty_dir / "themes"
        ghostty_themes.mkdir(parents=True, exist_ok=True)
        theme_file = ghostty_themes / f"krice-{palette.name}"
        config_path = ghostty_dir / "config"

        theme_content = f"""# Ghostty theme - Managed by krice
background = {palette.background}
foreground = {palette.foreground}
cursor-color = {palette.cursor}
cursor-text = {palette.cursor_text}
selection-background = {palette.selection_bg}
selection-foreground = {palette.selection_fg}

palette = 0={palette.black}
palette = 1={palette.red}
palette = 2={palette.green}
palette = 3={palette.yellow}
palette = 4={palette.blue}
palette = 5={palette.magenta}
palette = 6={palette.cyan}
palette = 7={palette.white}
palette = 8={palette.bright_black}
palette = 9={palette.bright_red}
palette = 10={palette.bright_green}
palette = 11={palette.bright_yellow}
palette = 12={palette.bright_blue}
palette = 13={palette.bright_magenta}
palette = 14={palette.bright_cyan}
palette = 15={palette.bright_white}
"""
        try:
            theme_file.write_text(theme_content, encoding="utf-8")
            if config_path.exists():
                cfg_txt = config_path.read_text(encoding="utf-8")
                if re.search(r"^theme\s*=", cfg_txt, re.MULTILINE):
                    cfg_txt = re.sub(r"^theme\s*=.*", f"theme = krice-{palette.name}", cfg_txt, flags=re.MULTILINE)
                else:
                    cfg_txt += f"\ntheme = krice-{palette.name}\n"
                config_path.write_text(cfg_txt, encoding="utf-8")
            else:
                config_path.write_text(f"theme = krice-{palette.name}\nbackground-opacity = 0.94\n", encoding="utf-8")

            return True, f"Ghostty color theme set to 'krice-{palette.name}'."
        except Exception as e:
            return False, f"Failed to update Ghostty theme: {e}"

    # 5. Foot
    def apply_foot(self, palette: TerminalPalette) -> tuple[bool, str]:
        """Applies theme to Foot terminal."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply Foot color theme: {palette.name}"

        foot_dir = self.config_dir / "foot"
        foot_dir.mkdir(parents=True, exist_ok=True)
        config_path = foot_dir / "foot.ini"

        def clean_hex(h: str) -> str:
            return h.lstrip("#")

        colors_ini = f"""[colors]
background={clean_hex(palette.background)}
foreground={clean_hex(palette.foreground)}
regular0={clean_hex(palette.black)}
regular1={clean_hex(palette.red)}
regular2={clean_hex(palette.green)}
regular3={clean_hex(palette.yellow)}
regular4={clean_hex(palette.blue)}
regular5={clean_hex(palette.magenta)}
regular6={clean_hex(palette.cyan)}
regular7={clean_hex(palette.white)}
bright0={clean_hex(palette.bright_black)}
bright1={clean_hex(palette.bright_red)}
bright2={clean_hex(palette.bright_green)}
bright3={clean_hex(palette.bright_yellow)}
bright4={clean_hex(palette.bright_blue)}
bright5={clean_hex(palette.bright_magenta)}
bright6={clean_hex(palette.bright_cyan)}
bright7={clean_hex(palette.bright_white)}
selection-foreground={clean_hex(palette.selection_fg)}
selection-background={clean_hex(palette.selection_bg)}
"""
        try:
            if config_path.exists():
                content = config_path.read_text(encoding="utf-8")
                cleaned = re.sub(r"\[colors\][\s\S]*?(?=\n\[|$)", "", content).strip()
                new_content = cleaned + "\n\n" + colors_ini
                config_path.write_text(new_content, encoding="utf-8")
            else:
                config_path.write_text(colors_ini, encoding="utf-8")

            return True, f"Foot color theme set to '{palette.name}'."
        except Exception as e:
            return False, f"Failed to update Foot theme: {e}"

    # 6. WezTerm
    def apply_wezterm(self, palette: TerminalPalette) -> tuple[bool, str]:
        """Applies theme to WezTerm terminal."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply WezTerm color theme: {palette.name}"

        wezterm_dir = self.config_dir / "wezterm"
        colors_dir = wezterm_dir / "colors"
        colors_dir.mkdir(parents=True, exist_ok=True)
        theme_file = colors_dir / f"krice-{palette.name}.toml"
        lua_config = wezterm_dir / "wezterm.lua"

        theme_toml = f"""[colors]
foreground = "{palette.foreground}"
background = "{palette.background}"
cursor_bg = "{palette.cursor}"
cursor_fg = "{palette.cursor_text}"
selection_bg = "{palette.selection_bg}"
selection_fg = "{palette.selection_fg}"
ansi = [
  "{palette.black}",
  "{palette.red}",
  "{palette.green}",
  "{palette.yellow}",
  "{palette.blue}",
  "{palette.magenta}",
  "{palette.cyan}",
  "{palette.white}",
]
brights = [
  "{palette.bright_black}",
  "{palette.bright_red}",
  "{palette.bright_green}",
  "{palette.bright_yellow}",
  "{palette.bright_blue}",
  "{palette.bright_magenta}",
  "{palette.bright_cyan}",
  "{palette.bright_white}",
]
"""
        try:
            theme_file.write_text(theme_toml, encoding="utf-8")
            if lua_config.exists():
                lua_txt = lua_config.read_text(encoding="utf-8")
                if "color_scheme" in lua_txt:
                    lua_txt = re.sub(r'config\.color_scheme\s*=\s*["\'].*?["\']', f'config.color_scheme = "krice-{palette.name}"', lua_txt)
                else:
                    lua_txt += f'\nconfig.color_scheme = "krice-{palette.name}"\n'
                lua_config.write_text(lua_txt, encoding="utf-8")
            else:
                lua_config.write_text(f"""local wezterm = require 'wezterm'
local config = wezterm.config_builder()
config.color_scheme = 'krice-{palette.name}'
config.window_background_opacity = 0.94
return config
""", encoding="utf-8")

            return True, f"WezTerm color theme set to 'krice-{palette.name}'."
        except Exception as e:
            return False, f"Failed to update WezTerm theme: {e}"

    # 6b. Zellij (Terminal Multiplexer)
    def apply_zellij(self, palette: TerminalPalette) -> tuple[bool, str]:
        """Applies theme to Zellij terminal multiplexer."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply Zellij color theme: {palette.name}"

        zellij_dir = self.config_dir / "zellij"
        themes_dir = zellij_dir / "themes"
        themes_dir.mkdir(parents=True, exist_ok=True)
        theme_file = themes_dir / f"krice-{palette.name}.kdl"

        theme_kdl = f"""themes {{
    "krice-{palette.name}" {{
        fg "{palette.foreground}"
        bg "{palette.background}"
        black "{palette.black}"
        red "{palette.red}"
        green "{palette.green}"
        yellow "{palette.yellow}"
        blue "{palette.blue}"
        magenta "{palette.magenta}"
        cyan "{palette.cyan}"
        white "{palette.white}"
        orange "{palette.bright_red}"
    }}
}}
"""
        try:
            theme_file.write_text(theme_kdl, encoding="utf-8")
            config_file = zellij_dir / "config.kdl"
            if config_file.exists():
                c_txt = config_file.read_text(encoding="utf-8")
                if "theme " in c_txt:
                    c_txt = re.sub(r'theme\s+["\'].*?["\']', f'theme "krice-{palette.name}"', c_txt)
                else:
                    c_txt = f'theme "krice-{palette.name}"\n' + c_txt
                config_file.write_text(c_txt, encoding="utf-8")
            else:
                config_file.write_text(f'theme "krice-{palette.name}"\n', encoding="utf-8")

            return True, f"Zellij color theme set to 'krice-{palette.name}'."
        except Exception as e:
            return False, f"Failed to update Zellij theme: {e}"

    # 7. Starship Shell Prompt
    def apply_starship(self, palette: TerminalPalette) -> tuple[bool, str]:
        """Applies matching Starship prompt theme."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply Starship prompt theme matching: {palette.name}"

        starship_file = self.config_dir / "starship.toml"
        starship_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            config_content = generate_starship_config(palette)
            starship_file.write_text(config_content, encoding="utf-8")
            return True, f"Starship prompt updated to match '{palette.display_name}'."
        except Exception as e:
            return False, f"Failed to update starship.toml: {e}"

    # 8. Fastfetch
    def apply_fastfetch(self, palette: TerminalPalette) -> tuple[bool, str]:
        """Applies matching Fastfetch display colors."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply Fastfetch theme matching: {palette.name}"

        fastfetch_dir = self.config_dir / "fastfetch"
        fastfetch_dir.mkdir(parents=True, exist_ok=True)
        config_path = fastfetch_dir / "config.jsonc"
        try:
            content = generate_fastfetch_config(palette)
            config_path.write_text(content, encoding="utf-8")
            return True, f"Fastfetch configuration updated to match '{palette.display_name}'."
        except Exception as e:
            return False, f"Failed to update Fastfetch config: {e}"

    # --- Unified Multi-Terminal Apply ---

    def apply_all(self, palette_or_name: Union[str, TerminalPalette]) -> dict[str, tuple[bool, str]]:
        """Synchronously applies the color palette across all detected/installed terminals & CLI tools."""
        if isinstance(palette_or_name, str):
            palette = self.get_palette(palette_or_name)
            if not palette:
                # Try fallback extraction or error
                palette = self.extract_palette_from_kde()
        else:
            palette = palette_or_name

        results: dict[str, tuple[bool, str]] = {}
        detected = self.detect_installed_terminals()

        # Always update Konsole & Alacritty if installed or configs exist
        if detected.get("konsole", True):
            results["Konsole"] = self.apply_konsole(palette)

        if detected.get("alacritty", True):
            results["Alacritty"] = self.apply_alacritty(palette)

        if detected.get("kitty", False) or (self.config_dir / "kitty").exists():
            results["Kitty"] = self.apply_kitty(palette)

        if detected.get("ghostty", False) or (self.config_dir / "ghostty").exists():
            results["Ghostty"] = self.apply_ghostty(palette)

        if detected.get("foot", False) or (self.config_dir / "foot").exists():
            results["Foot"] = self.apply_foot(palette)

        if detected.get("wezterm", False) or (self.config_dir / "wezterm").exists():
            results["WezTerm"] = self.apply_wezterm(palette)

        if detected.get("zellij", False) or (self.config_dir / "zellij").exists():
            results["Zellij"] = self.apply_zellij(palette)

        if detected.get("starship", True):
            results["Starship"] = self.apply_starship(palette)

        if detected.get("fastfetch", True):
            results["Fastfetch"] = self.apply_fastfetch(palette)

        return results
