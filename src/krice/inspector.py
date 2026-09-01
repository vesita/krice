"""Inspector for current KDE Plasma 6 desktop, theme, motion, and terminal environment."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from krice.kwin_ctl import KWinController
from krice.terminal_ctl import TerminalController
from krice.theme_ctl import ThemeController


@dataclass
class DesktopReport:
    session_type: str
    plasma_version: str
    global_theme: str
    color_scheme: str
    cursor_theme: str
    cursor_size: int
    icon_theme: str
    plasma_style: str
    widget_style: str
    kvantum_theme: str
    window_decoration: str
    gtk_theme: str
    splash_theme: str
    animation_factor: float
    window_open_close_effect: str
    window_minimize_effect: str
    blur_enabled: bool
    morphing_popups: bool
    wobbly_windows: bool
    klassy_installed: bool
    kvantum_installed: bool
    forceblur_installed: bool
    installed_terminals: list[str] = field(default_factory=list)
    starship_installed: bool = False
    fastfetch_installed: bool = False


class DesktopInspector:
    """Diagnoses and reports KDE Plasma visual settings, themes, motion effects, and terminal integrations."""

    def __init__(self) -> None:
        self.kwin = KWinController()
        self.theme = ThemeController()
        self.term = TerminalController()

    def inspect(self) -> DesktopReport:
        session_type = os.environ.get("XDG_SESSION_TYPE", "unknown").upper()

        # Plasma version
        plasmashell_bin = shutil.which("plasmashell")
        plasma_ver = "Unknown"
        if plasmashell_bin:
            try:
                out = subprocess.check_output([plasmashell_bin, "--version"], text=True, stderr=subprocess.DEVNULL)
                plasma_ver = out.strip().replace("plasmashell ", "")
            except Exception:
                pass

        # Theming
        global_theme = self.theme.get_current_global_theme()
        color_scheme = self.theme.get_current_colorscheme()
        cursor_theme = self.theme.get_current_cursor_theme()
        cursor_size = self.theme.get_current_cursor_size()
        icon_theme = self.theme.get_current_icon_theme()
        plasma_style = self.theme.get_current_plasma_style()
        widget_style = self.theme.get_current_widget_style()
        kvantum_theme = self.theme.get_current_kvantum_theme()
        deco_lib, deco_theme = self.theme.get_window_decoration()
        deco_str = f"{deco_lib} ({deco_theme})" if deco_theme else deco_lib
        gtk_theme = self.theme.get_gtk_theme()
        splash_theme, _ = self.theme.get_current_splash()

        # Motion & Effects
        animation_factor = self.kwin.get_animation_factor()
        open_close = []
        if self.kwin.get_plugin_status("scale"):
            open_close.append("Scale")
        if self.kwin.get_plugin_status("glide"):
            open_close.append("Glide")
        if self.kwin.get_plugin_status("fade"):
            open_close.append("Fade")
        open_str = ", ".join(open_close) if open_close else "Default (Fade/None)"

        min_effects = []
        if self.kwin.get_plugin_status("squash"):
            min_effects.append("Squash")
        if self.kwin.get_plugin_status("magiclamp"):
            min_effects.append("Magic Lamp")
        min_str = ", ".join(min_effects) if min_effects else "None (Instant)"

        blur_on = self.kwin.get_plugin_status("blur")
        morphing_on = self.kwin.get_plugin_status("morphingpopups")
        wobbly_on = self.kwin.get_plugin_status("wobblywindows")

        # Tool installation check
        klassy_installed = shutil.which("klassy-settings") is not None or Path("/usr/lib/qt6/plugins/org.kde.kdecoration2/klassy.so").exists()
        kvantum_installed = shutil.which("kvantummanager") is not None
        forceblur_installed = self.kwin.get_plugin_status("kwin4_effect_forceblur") or Path("/usr/lib/qt6/plugins/kwin/effects/configs/kwin_forceblur_config.so").exists()

        # Terminals check
        detected_terms = self.term.detect_installed_terminals()
        active_terms = [t.capitalize() for t, ok in detected_terms.items() if ok and t not in ("starship", "fastfetch")]
        starship_ok = detected_terms.get("starship", False)
        fastfetch_ok = detected_terms.get("fastfetch", False)

        return DesktopReport(
            session_type=session_type,
            plasma_version=plasma_ver,
            global_theme=global_theme,
            color_scheme=color_scheme,
            cursor_theme=cursor_theme,
            cursor_size=cursor_size,
            icon_theme=icon_theme,
            plasma_style=plasma_style,
            widget_style=widget_style,
            kvantum_theme=kvantum_theme,
            window_decoration=deco_str,
            gtk_theme=gtk_theme,
            splash_theme=splash_theme,
            animation_factor=animation_factor,
            window_open_close_effect=open_str,
            window_minimize_effect=min_str,
            blur_enabled=blur_on,
            morphing_popups=morphing_on,
            wobbly_windows=wobbly_on,
            klassy_installed=klassy_installed,
            kvantum_installed=kvantum_installed,
            forceblur_installed=forceblur_installed,
            installed_terminals=active_terms,
            starship_installed=starship_ok,
            fastfetch_installed=fastfetch_ok,
        )
