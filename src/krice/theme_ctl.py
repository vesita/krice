"""KDE Plasma 6 Theming, Color Schemes, Icons, Cursors & Wallpaper Controller."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from krice.kwin_ctl import KWinController


class ThemeController:
    """Manages global themes, color schemes, icon themes, cursor themes, and wallpapers."""

    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.kwin = KWinController(dry_run=dry_run)
        self.apply_colorscheme_bin = shutil.which("plasma-apply-colorscheme")
        self.apply_lookandfeel_bin = shutil.which("plasma-apply-lookandfeel")
        self.apply_cursortheme_bin = shutil.which("plasma-apply-cursortheme")
        self.apply_wallpaper_bin = shutil.which("plasma-apply-wallpaperimage")

    # --- Color Schemes ---

    def list_colorschemes(self) -> list[str]:
        """Returns all available color schemes installed on the system."""
        if not self.apply_colorscheme_bin:
            return []
        try:
            res = subprocess.run([self.apply_colorscheme_bin, "-l"], capture_output=True, text=True, check=False)
            lines = res.stdout.strip().splitlines()
            schemes = []
            for line in lines:
                cleaned = line.strip().lstrip("*").strip()
                if "(当前配色方案)" in cleaned or "(current color scheme)" in cleaned:
                    cleaned = re.sub(r"\(.*?\)", "", cleaned).strip()
                if cleaned and not cleaned.startswith("您的系统") and not cleaned.startswith("You have"):
                    schemes.append(cleaned)
            return sorted(list(set(schemes)))
        except Exception:
            return []

    def get_current_colorscheme(self) -> str:
        """Returns the name of the active color scheme."""
        return self.kwin.read_config("kdeglobals", "General", "ColorScheme", default="Default")

    def apply_colorscheme(self, scheme_name: str) -> tuple[bool, str]:
        """Applies a color scheme via plasma-apply-colorscheme."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply color scheme: {scheme_name}"
        if not self.apply_colorscheme_bin:
            return False, "plasma-apply-colorscheme command not found."
        try:
            res = subprocess.run([self.apply_colorscheme_bin, scheme_name], capture_output=True, text=True, check=False)
            if res.returncode == 0:
                return True, f"Color scheme '{scheme_name}' applied successfully."
            return False, res.stderr.strip() or res.stdout.strip()
        except Exception as e:
            return False, f"Failed to apply color scheme: {e}"

    # --- Global Look & Feel Themes ---

    def list_global_themes(self) -> list[str]:
        """Returns all available global Look-and-Feel themes."""
        if not self.apply_lookandfeel_bin:
            return []
        try:
            res = subprocess.run([self.apply_lookandfeel_bin, "-l"], capture_output=True, text=True, check=False)
            lines = [line.strip() for line in res.stdout.strip().splitlines() if line.strip()]
            return sorted(lines)
        except Exception:
            return []

    def get_current_global_theme(self) -> str:
        """Returns the current Look-and-Feel package ID."""
        return self.kwin.read_config("kdeglobals", "KDE", "LookAndFeelPackage", default="org.kde.breezedark.desktop")

    def apply_global_theme(self, theme_name: str) -> tuple[bool, str]:
        """Applies a global look-and-feel theme."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply global theme: {theme_name}"
        if not self.apply_lookandfeel_bin:
            return False, "plasma-apply-lookandfeel command not found."
        try:
            res = subprocess.run([self.apply_lookandfeel_bin, "-a", theme_name], capture_output=True, text=True, check=False)
            if res.returncode == 0:
                return True, f"Global theme '{theme_name}' applied successfully."
            return False, res.stderr.strip() or res.stdout.strip()
        except Exception as e:
            return False, f"Failed to apply global theme: {e}"

    # --- Cursor Themes ---

    def list_cursor_themes(self) -> list[str]:
        """Returns all available cursor themes."""
        if not self.apply_cursortheme_bin:
            return []
        try:
            res = subprocess.run([self.apply_cursortheme_bin, "--list-themes"], capture_output=True, text=True, check=False)
            lines = [line.strip().lstrip("*").strip() for line in res.stdout.strip().splitlines() if line.strip()]
            themes = []
            for line in lines:
                if "(当前主题)" in line or "(current theme)" in line:
                    line = re.sub(r"\(.*?\)", "", line).strip()
                if line and not line.startswith("您的系统") and not line.startswith("You have"):
                    themes.append(line)
            return sorted(list(set(themes)))
        except Exception:
            return []

    def get_current_cursor_theme(self) -> str:
        """Returns the current cursor theme name."""
        return self.kwin.read_config("kcminputrc", "Mouse", "cursorTheme", default="breeze_cursors")

    def apply_cursor_theme(self, theme_name: str, size: Optional[int] = None) -> tuple[bool, str]:
        """Applies a cursor theme and optional size."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply cursor theme: {theme_name} (size: {size})"
        if not self.apply_cursortheme_bin:
            return False, "plasma-apply-cursortheme command not found."
        cmd = [self.apply_cursortheme_bin, theme_name]
        if size:
            cmd.extend(["--size", str(size)])
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                return True, f"Cursor theme '{theme_name}' applied successfully."
            return False, res.stderr.strip() or res.stdout.strip()
        except Exception as e:
            return False, f"Failed to apply cursor theme: {e}"

    # --- Icon Themes ---

    def list_icon_themes(self) -> list[str]:
        """Scans standard icon search paths for installed icon themes."""
        icon_dirs = [
            Path("/usr/share/icons"),
            Path.home() / ".local" / "share" / "icons",
        ]
        found: set[str] = set()
        for d in icon_dirs:
            if d.exists():
                for sub in d.iterdir():
                    if sub.is_dir() and (sub / "index.theme").exists():
                        found.add(sub.name)
        return sorted(list(found))

    def get_current_icon_theme(self) -> str:
        """Returns the current icon theme name."""
        return self.kwin.read_config("kdeglobals", "Icons", "Theme", default="breeze-dark")

    def apply_icon_theme(self, theme_name: str) -> tuple[bool, str]:
        """Sets the active icon theme in kdeglobals."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply icon theme: {theme_name}"
        ok = self.kwin.write_config("kdeglobals", "Icons", "Theme", theme_name)
        if ok:
            # Inform kwin / plasma
            self.kwin.reconfigure_kwin()
            return True, f"Icon theme set to '{theme_name}'."
        return False, f"Failed to write icon theme '{theme_name}' to kdeglobals."

    # --- Window Decorations ---

    def get_window_decoration(self) -> tuple[str, str]:
        """Returns (library, theme) for window decoration."""
        lib = self.kwin.read_config("kwinrc", "org.kde.kdecoration2", "library", default="org.kde.breeze")
        theme = self.kwin.read_config("kwinrc", "org.kde.kdecoration2", "theme", default="")
        return lib, theme

    def set_window_decoration(self, library: str, theme: Optional[str] = None) -> tuple[bool, str]:
        """Sets window decoration library (e.g. org.kde.breeze, klassy, org.kde.kwin.aurorae.v2)."""
        if self.dry_run:
            return True, f"[Dry-run] Would set window decoration: {library} (theme: {theme})"
        self.kwin.write_config("kwinrc", "org.kde.kdecoration2", "library", library)
        if theme is not None:
            self.kwin.write_config("kwinrc", "org.kde.kdecoration2", "theme", theme)
        self.kwin.reconfigure_kwin()
        return True, f"Window decoration set to '{library}'."

    # --- Plasma Desktop Style (Panel & Launcher Background) ---

    def list_plasma_styles(self) -> list[str]:
        """Returns all installed Plasma Desktop Styles (controls launcher/panel colors)."""
        style_dirs = [
            Path("/usr/share/plasma/desktoptheme"),
            Path.home() / ".local" / "share" / "plasma" / "desktoptheme",
        ]
        found: set[str] = set()
        for d in style_dirs:
            if d.exists():
                for sub in d.iterdir():
                    if sub.is_dir() and (sub / "metadata.json").exists() or (sub / "metadata.desktop").exists() or (sub / "colors").exists():
                        found.add(sub.name)
        return sorted(list(found))

    def get_current_plasma_style(self) -> str:
        """Returns active Plasma Desktop Style name."""
        return self.kwin.read_config("plasmarc", "Theme", "name", default="default")

    def apply_plasma_style(self, style_name: str) -> tuple[bool, str]:
        """Sets the active Plasma Desktop Style in plasmarc and reloads."""
        if self.dry_run:
            return True, f"[Dry-run] Would set Plasma Desktop Style: {style_name}"
        ok = self.kwin.write_config("plasmarc", "Theme", "name", style_name)
        if ok:
            # Reload KWin & inform Plasma
            self.kwin.reconfigure_kwin()
            return True, f"Plasma Desktop Style set to '{style_name}'."
        return False, f"Failed to set Plasma style '{style_name}'."

    # --- Wallpaper ---

    def apply_wallpaper(self, wallpaper_path: Path) -> tuple[bool, str]:
        """Applies a desktop wallpaper image using plasma-apply-wallpaperimage."""
        if not wallpaper_path.exists():
            return False, f"Wallpaper file not found: {wallpaper_path}"
        if self.dry_run:
            return True, f"[Dry-run] Would set wallpaper: {wallpaper_path}"
        if not self.apply_wallpaper_bin:
            return False, "plasma-apply-wallpaperimage command not found."
        try:
            res = subprocess.run([self.apply_wallpaper_bin, str(wallpaper_path.resolve())], capture_output=True, text=True, check=False)
            if res.returncode == 0:
                return True, f"Wallpaper updated to '{wallpaper_path.name}'."
            return False, res.stderr.strip() or res.stdout.strip()
        except Exception as e:
            return False, f"Failed to set wallpaper: {e}"
