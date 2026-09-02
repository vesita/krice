"""KDE Plasma 6 Theming, Color Schemes, Icons, Cursors, Widget Styles, Kvantum, GTK & Wallpaper Controller."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional

from krice.kwin_ctl import KWinController


class ThemeController:
    """Manages global themes, color schemes, icon themes, cursor themes, widget styles, Kvantum, GTK, and wallpapers."""

    def __init__(self, dry_run: bool = False, home_dir: Optional[Path] = None) -> None:
        self.dry_run = dry_run
        self.home = home_dir or Path.home()
        self.config_dir = Path(os.environ.get("XDG_CONFIG_HOME", str(self.home / ".config")))
        self.data_dir = Path(os.environ.get("XDG_DATA_HOME", str(self.home / ".local" / "share")))
        self.kdeglobals = self.config_dir / "kdeglobals"
        self.kwinrc = self.config_dir / "kwinrc"
        self.kwin = KWinController(dry_run=dry_run, home_dir=self.home)
        self.apply_colorscheme_bin = shutil.which("plasma-apply-colorscheme")
        self.apply_lookandfeel_bin = shutil.which("plasma-apply-lookandfeel")
        self.apply_cursortheme_bin = shutil.which("plasma-apply-cursortheme")
        self.apply_wallpaper_bin = shutil.which("plasma-apply-wallpaperimage")
    # ==================== 1. Color Schemes ====================

    def list_colorschemes(self) -> list[str]:
        """Returns all available color schemes installed on the system."""
        if not self.apply_colorscheme_bin:
            # Fallback scan directories
            scheme_dirs = [
                Path("/usr/share/color-schemes"),
                self.data_dir / "color-schemes",
            ]
            found = set()
            for d in scheme_dirs:
                if d.exists():
                    for f in d.glob("*.colors"):
                        found.add(f.stem)
            return sorted(list(found))

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
        """Applies a color scheme via plasma-apply-colorscheme or directly in kdeglobals."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply color scheme: {scheme_name}"
        if not self.apply_colorscheme_bin:
            ok = self.kwin.write_config("kdeglobals", "General", "ColorScheme", scheme_name)
            if ok:
                self.kwin.reconfigure_kwin()
                return True, f"Color scheme set to '{scheme_name}' in kdeglobals."
            return False, "plasma-apply-colorscheme not found and failed writing kdeglobals."

        try:
            res = subprocess.run([self.apply_colorscheme_bin, scheme_name], capture_output=True, text=True, check=False)
            if res.returncode == 0:
                return True, f"Color scheme '{scheme_name}' applied successfully."
            return False, res.stderr.strip() or res.stdout.strip()
        except Exception as e:
            return False, f"Failed to apply color scheme: {e}"

    # ==================== 2. Global Look & Feel Themes ====================

    def list_global_themes(self) -> list[str]:
        """Returns all available global Look-and-Feel themes."""
        if not self.apply_lookandfeel_bin:
            dirs = [
                Path("/usr/share/plasma/look-and-feel"),
                self.data_dir / "plasma" / "look-and-feel",
            ]
            found = set()
            for d in dirs:
                if d.exists():
                    for sub in d.iterdir():
                        if sub.is_dir():
                            found.add(sub.name)
            return sorted(list(found))

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

    # ==================== 3. Cursor Themes ====================

    def list_cursor_themes(self) -> list[str]:
        """Returns all available cursor themes."""
        if not self.apply_cursortheme_bin:
            dirs = [
                Path("/usr/share/icons"),
                self.data_dir / "icons",
            ]
            found = set()
            for d in dirs:
                if d.exists():
                    for sub in d.iterdir():
                        if sub.is_dir() and (sub / "cursors").exists():
                            found.add(sub.name)
            return sorted(list(found))

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

    def get_current_cursor_size(self) -> int:
        """Returns the current cursor size."""
        raw = self.kwin.read_config("kcminputrc", "Mouse", "cursorSize", default="24")
        try:
            return int(raw)
        except ValueError:
            return 24

    def apply_cursor_theme(self, theme_name: str, size: Optional[int] = None) -> tuple[bool, str]:
        """Applies a cursor theme and optional size."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply cursor theme: {theme_name} (size: {size})"
        if not self.apply_cursortheme_bin:
            self.kwin.write_config("kcminputrc", "Mouse", "cursorTheme", theme_name)
            if size:
                self.kwin.write_config("kcminputrc", "Mouse", "cursorSize", str(size))
            return True, f"Cursor theme set to '{theme_name}' in kcminputrc."

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

    # ==================== 4. Icon Themes ====================

    def list_icon_themes(self) -> list[str]:
        """Scans standard icon search paths for installed icon themes."""
        icon_dirs = [
            Path("/usr/share/icons"),
            self.data_dir / "icons",
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
            self.kwin.reconfigure_kwin()
            return True, f"Icon theme set to '{theme_name}'."
        return False, f"Failed to write icon theme '{theme_name}' to kdeglobals."

    # ==================== 5. Plasma Desktop Style (Panel/Taskbar) ====================

    def list_plasma_styles(self) -> list[str]:
        """Returns all installed Plasma Desktop Styles (controls launcher/panel colors)."""
        style_dirs = [
            Path("/usr/share/plasma/desktoptheme"),
            self.data_dir / "plasma" / "desktoptheme",
        ]
        found: set[str] = set()
        for d in style_dirs:
            if d.exists():
                for sub in d.iterdir():
                    if sub.is_dir() and ((sub / "metadata.json").exists() or (sub / "metadata.desktop").exists() or (sub / "colors").exists()):
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
            self.kwin.reconfigure_kwin()
            return True, f"Plasma Desktop Style set to '{style_name}'."
        return False, f"Failed to set Plasma style '{style_name}'."

    # ==================== 6. Application Widget Styles (Qt6) ====================

    def list_widget_styles(self) -> list[str]:
        """Returns all available Qt widget style engines (e.g. Breeze, kvantum, kvantum-dark, Fusion, Oxygen)."""
        styles = {"Breeze", "Fusion", "Oxygen"}
        # Check Kvantum
        if shutil.which("kvantummanager") is not None or Path("/usr/lib/qt6/plugins/styles/libkvantum.so").exists() or Path("/usr/lib/qt/plugins/styles/libkvantum.so").exists():
            styles.add("kvantum")
            styles.add("kvantum-dark")
        # Check Lightly
        if Path("/usr/lib/qt6/plugins/styles/liblightly.so").exists():
            styles.add("Lightly")
        # Check Qt6 plugin dir
        qt6_plugin_dir = Path("/usr/lib/qt6/plugins/styles")
        if qt6_plugin_dir.exists():
            for p in qt6_plugin_dir.glob("lib*.so"):
                stem = p.stem.removeprefix("lib")
                styles.add(stem.capitalize())
        return sorted(list(styles))

    def get_current_widget_style(self) -> str:
        """Returns active Qt widget style."""
        return self.kwin.read_config("kdeglobals", "KDE", "widgetStyle", default="Breeze")

    def apply_widget_style(self, style_name: str) -> tuple[bool, str]:
        """Sets the active Qt widget style in kdeglobals."""
        if self.dry_run:
            return True, f"[Dry-run] Would set Qt widget style: {style_name}"
        ok = self.kwin.write_config("kdeglobals", "KDE", "widgetStyle", style_name)
        if ok:
            self.kwin.reconfigure_kwin()
            return True, f"Application widget style set to '{style_name}'."
        return False, f"Failed to set widget style '{style_name}'."

    # ==================== 7. Kvantum SVG Theme Manager ====================

    def list_kvantum_themes(self) -> list[str]:
        """Returns all installed Kvantum themes."""
        kv_dirs = [
            Path("/usr/share/Kvantum"),
            self.config_dir / "Kvantum",
            self.data_dir / "Kvantum",
        ]
        found = set()
        for d in kv_dirs:
            if d.exists():
                for sub in d.iterdir():
                    if sub.is_dir() and (sub / f"{sub.name}.kvconfig").exists():
                        found.add(sub.name)
        return sorted(list(found))

    def get_current_kvantum_theme(self) -> str:
        """Returns currently active Kvantum theme."""
        kv_config = self.config_dir / "Kvantum" / "kvantum.kvconfig"
        if kv_config.exists():
            content = kv_config.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"theme\s*=\s*(.+)", content)
            if m:
                return m.group(1).strip()
        return "Default"

    def apply_kvantum_theme(self, theme_name: str) -> tuple[bool, str]:
        """Applies a Kvantum theme via kvantummanager or writing kvantum.kvconfig."""
        if self.dry_run:
            return True, f"[Dry-run] Would apply Kvantum theme: {theme_name}"

        kv_manager = shutil.which("kvantummanager")
        if kv_manager:
            try:
                res = subprocess.run([kv_manager, "--set", theme_name], capture_output=True, text=True, check=False)
                if res.returncode == 0:
                    return True, f"Kvantum theme set to '{theme_name}'."
            except Exception:
                pass

        # Direct file fallback
        kv_dir = self.config_dir / "Kvantum"
        kv_dir.mkdir(parents=True, exist_ok=True)
        kv_config = kv_dir / "kvantum.kvconfig"
        try:
            if kv_config.exists():
                content = kv_config.read_text(encoding="utf-8")
                if re.search(r"theme\s*=", content):
                    content = re.sub(r"theme\s*=.*", f"theme={theme_name}", content)
                else:
                    content += f"\n[General]\ntheme={theme_name}\n"
                kv_config.write_text(content, encoding="utf-8")
            else:
                kv_config.write_text(f"[General]\ntheme={theme_name}\n", encoding="utf-8")
            return True, f"Kvantum theme set to '{theme_name}'."
        except Exception as e:
            return False, f"Failed to set Kvantum theme: {e}"

    # ==================== 8. Window Decorations & Klassy ====================

    def list_window_decorations(self) -> list[str]:
        """Returns available window decoration libraries."""
        libs = ["org.kde.breeze"]
        if shutil.which("klassy-settings") is not None or Path("/usr/lib/qt6/plugins/org.kde.kdecoration2/klassy.so").exists():
            libs.append("klassy")
        if Path("/usr/lib/qt6/plugins/org.kde.kdecoration2/kwin-sierrabreezeenhanced.so").exists():
            libs.append("sierrabreezeenhanced")
        if (Path("/usr/share/aurorae/themes").exists() or (self.data_dir / "aurorae" / "themes").exists()):
            libs.append("org.kde.kwin.aurorae.v2")
        return libs

    def get_window_decoration(self) -> tuple[str, str]:
        """Returns (library, theme) for window decoration."""
        lib = self.kwin.read_config("kwinrc", "org.kde.kdecoration2", "library", default="org.kde.breeze")
        theme = self.kwin.read_config("kwinrc", "org.kde.kdecoration2", "theme", default="")
        return lib, theme

    def set_window_decoration(
        self,
        library: str,
        theme: Optional[str] = None,
        buttons_left: Optional[str] = None,
        buttons_right: Optional[str] = None,
        border_size: Optional[str] = None,
    ) -> tuple[bool, str]:
        """Sets window decoration library, theme, and optional button layout / border size."""
        if self.dry_run:
            return True, f"[Dry-run] Would set window decoration: {library} (theme: {theme})"

        self.kwin.write_config("kwinrc", "org.kde.kdecoration2", "library", library)
        if theme is not None:
            self.kwin.write_config("kwinrc", "org.kde.kdecoration2", "theme", theme)
        if buttons_left is not None:
            self.kwin.write_config("kwinrc", "org.kde.kdecoration2", "ButtonsOnLeft", buttons_left)
        if buttons_right is not None:
            self.kwin.write_config("kwinrc", "org.kde.kdecoration2", "ButtonsOnRight", buttons_right)
        if border_size is not None:
            self.kwin.write_config("kwinrc", "org.kde.kdecoration2", "BorderSize", border_size)

        self.kwin.reconfigure_kwin()
        return True, f"Window decoration set to '{library}'."

    def configure_klassy(
        self,
        corner_radius: int = 10,
        blur: bool = True,
        opacity: int = 100,
    ) -> tuple[bool, str]:
        """Configures Klassy window decoration settings if Klassy is used."""
        if self.dry_run:
            return True, f"[Dry-run] Would configure Klassy (radius: {corner_radius}, blur: {blur})"

        klassy_dir = self.config_dir / "klassy"
        klassy_dir.mkdir(parents=True, exist_ok=True)
        klassyrc = klassy_dir / "klassyrc"

        try:
            # Write or update klassy settings
            self.kwin.write_config("klassyrc", "WindowDeco", "CornerRadius", str(corner_radius))
            self.kwin.write_config("klassyrc", "WindowDeco", "BackgroundBlur", "true" if blur else "false")
            self.kwin.write_config("klassyrc", "WindowDeco", "Opacity", str(opacity))
            self.kwin.reconfigure_kwin()
            return True, f"Klassy configured (CornerRadius: {corner_radius}px, Blur: {blur})."
        except Exception as e:
            return False, f"Failed to configure Klassy: {e}"

    # ==================== 9. Font Settings ====================

    def get_fonts(self) -> dict[str, str]:
        """Returns KDE system font configuration from kdeglobals."""
        fonts = {
            "General": self.kwin.read_config("kdeglobals", "General", "font", default="Noto Sans,10,-1,5,50,0,0,0,0,0"),
            "Fixed": self.kwin.read_config("kdeglobals", "General", "fixed", default="Hack,10,-1,5,50,0,0,0,0,0"),
            "SmallestReadable": self.kwin.read_config("kdeglobals", "General", "smallestReadableFont", default="Noto Sans,8,-1,5,50,0,0,0,0,0"),
            "ToolBar": self.kwin.read_config("kdeglobals", "General", "toolBarFont", default="Noto Sans,10,-1,5,50,0,0,0,0,0"),
            "Menu": self.kwin.read_config("kdeglobals", "General", "menuFont", default="Noto Sans,10,-1,5,50,0,0,0,0,0"),
            "WindowTitle": self.kwin.read_config("kdeglobals", "WM", "activeFont", default="Noto Sans,10,-1,5,50,0,0,0,0,0"),
        }
        return fonts

    def set_font(self, category: str, font_spec: str) -> tuple[bool, str]:
        """Sets a font specification for a given category (General, Fixed, Menu, ToolBar, WindowTitle)."""
        if self.dry_run:
            return True, f"[Dry-run] Would set font for '{category}': {font_spec}"

        cat_map = {
            "general": ("General", "font"),
            "fixed": ("General", "fixed"),
            "small": ("General", "smallestReadableFont"),
            "toolbar": ("General", "toolBarFont"),
            "menu": ("General", "menuFont"),
            "windowtitle": ("WM", "activeFont"),
        }
        target = cat_map.get(category.lower())
        if not target:
            return False, f"Unknown font category '{category}'. Choose from: {list(cat_map.keys())}"

        group, key = target
        ok = self.kwin.write_config("kdeglobals", group, key, font_spec)
        if ok:
            self.kwin.reconfigure_kwin()
            return True, f"Font for '{category}' updated."
        return False, f"Failed to set font for '{category}'."

    # ==================== 10. Splash Screen ====================

    def list_splash_themes(self) -> list[str]:
        """Returns installed KDE splash screen themes."""
        dirs = [
            Path("/usr/share/plasma/look-and-feel"),
            self.data_dir / "plasma" / "look-and-feel",
        ]
        found = set()
        for d in dirs:
            if d.exists():
                for sub in d.iterdir():
                    if sub.is_dir() and (sub / "contents" / "splash").exists():
                        found.add(sub.name)
        return sorted(list(found))

    def get_current_splash(self) -> tuple[str, str]:
        """Returns (theme, engine) for splash screen."""
        theme = self.kwin.read_config("ksplashrc", "KSplash", "Theme", default="org.kde.breeze.desktop")
        engine = self.kwin.read_config("ksplashrc", "KSplash", "Engine", default="KSplashQML")
        return theme, engine

    def apply_splash_theme(self, theme_name: str, engine: str = "KSplashQML") -> tuple[bool, str]:
        """Sets active splash screen in ksplashrc."""
        if self.dry_run:
            return True, f"[Dry-run] Would set Splash Screen: {theme_name} (Engine: {engine})"
        self.kwin.write_config("ksplashrc", "KSplash", "Theme", theme_name)
        self.kwin.write_config("ksplashrc", "KSplash", "Engine", engine)
        return True, f"Splash screen set to '{theme_name}'."

    # ==================== 11. GTK Theme & Dark Preference Sync ====================

    def get_gtk_theme(self) -> str:
        """Returns active GTK 3/4 theme name."""
        gtk3_ini = self.config_dir / "gtk-3.0" / "settings.ini"
        if gtk3_ini.exists():
            content = gtk3_ini.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"gtk-theme-name\s*=\s*(.+)", content)
            if m:
                return m.group(1).strip()
        return "Breeze"

    def sync_gtk_theme(
        self,
        gtk_theme: Optional[str] = None,
        dark_mode: Optional[bool] = None,
        icon_theme: Optional[str] = None,
        cursor_theme: Optional[str] = None,
    ) -> tuple[bool, str]:
        """Synchronizes GTK 3.0 / 4.0 settings and GNOME interface preferences with KDE."""
        if self.dry_run:
            return True, f"[Dry-run] Would sync GTK theme: {gtk_theme} (Dark: {dark_mode})"

        theme_to_set = gtk_theme or ("Breeze-Dark" if dark_mode else "Breeze")
        icons_to_set = icon_theme or self.get_current_icon_theme()
        cursors_to_set = cursor_theme or self.get_current_cursor_theme()

        # Update GTK 3.0
        for ver in ["gtk-3.0", "gtk-4.0"]:
            d = self.config_dir / ver
            d.mkdir(parents=True, exist_ok=True)
            ini_file = d / "settings.ini"
            content = f"""[Settings]
gtk-theme-name={theme_to_set}
gtk-icon-theme-name={icons_to_set}
gtk-cursor-theme-name={cursors_to_set}
gtk-application-prefer-dark-theme={'1' if dark_mode else '0'}
"""
            try:
                ini_file.write_text(content, encoding="utf-8")
            except Exception as e:
                return False, f"Failed writing {ver} settings: {e}"

        # Update GSettings via gsettings if present
        gsettings_bin = shutil.which("gsettings")
        if gsettings_bin:
            try:
                subprocess.run([gsettings_bin, "set", "org.gnome.desktop.interface", "gtk-theme", theme_to_set], check=False, capture_output=True)
                color_scheme = "prefer-dark" if dark_mode else "prefer-light"
                subprocess.run([gsettings_bin, "set", "org.gnome.desktop.interface", "color-scheme", color_scheme], check=False, capture_output=True)
            except Exception:
                pass

        return True, f"GTK 3/4 theme synchronized to '{theme_to_set}'."

    # ==================== 12. Active Palette Extractor ====================

    def get_active_palette_summary(self) -> dict[str, str]:
        """Returns summary of current active color values from kdeglobals."""
        kdeglobals = self.config_dir / "kdeglobals"
        summary = {
            "ColorScheme": self.get_current_colorscheme(),
            "WindowBackground": "#2E3440",
            "WindowForeground": "#ECEFF4",
            "SelectionBackground": "#5E81AC",
            "SelectionForeground": "#ECEFF4",
            "ButtonBackground": "#3B4252",
        }
        if kdeglobals.exists():
            content = kdeglobals.read_text(encoding="utf-8", errors="ignore")
            from krice.terminal_ctl import parse_kde_rgb
            m = re.search(r"\[Colors:Window\][^\[]*?BackgroundNormal=([0-9, ]+)", content)
            if m:
                summary["WindowBackground"] = parse_kde_rgb(m.group(1), summary["WindowBackground"])
            m = re.search(r"\[Colors:Window\][^\[]*?ForegroundNormal=([0-9, ]+)", content)
            if m:
                summary["WindowForeground"] = parse_kde_rgb(m.group(1), summary["WindowForeground"])
            m = re.search(r"\[Colors:Selection\][^\[]*?BackgroundNormal=([0-9, ]+)", content)
            if m:
                summary["SelectionBackground"] = parse_kde_rgb(m.group(1), summary["SelectionBackground"])
            m = re.search(r"\[Colors:Selection\][^\[]*?ForegroundNormal=([0-9, ]+)", content)
            if m:
                summary["SelectionForeground"] = parse_kde_rgb(m.group(1), summary["SelectionForeground"])
            m = re.search(r"\[Colors:Button\][^\[]*?BackgroundNormal=([0-9, ]+)", content)
            if m:
                summary["ButtonBackground"] = parse_kde_rgb(m.group(1), summary["ButtonBackground"])
        return summary

    # ==================== 13. Wallpaper ====================

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
