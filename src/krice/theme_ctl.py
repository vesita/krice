"""KDE Plasma 6 全局主题、配色方案、图标、鼠标指针、Qt 控件样式、Kvantum、GTK 与壁纸控制器。"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional

from krice.kwin_ctl import KWinController


class ThemeController:
    """全面管理 KDE 全局外观、配色方案、图标主题、鼠标指针、Qt 控件引擎、Kvantum 与 GTK 统一主题。"""

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

    # ==================== 1. 配色方案 (Color Schemes) ====================

    def list_colorschemes(self) -> list[str]:
        """列出系统中已安装的所有可用配色方案。"""
        if not self.apply_colorscheme_bin:
            # 扫描标准配色目录作为回退
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
        """获取当前正在生效的 KDE 配色方案名称。"""
        return self.kwin.read_config("kdeglobals", "General", "ColorScheme", default="Default")

    def apply_colorscheme(self, scheme_name: str) -> tuple[bool, str]:
        """应用指定的配色方案（调用 plasma-apply-colorscheme 或写入 kdeglobals）。"""
        if self.dry_run:
            return True, f"[演练模拟] 将应用配色方案: {scheme_name}"
        if not self.apply_colorscheme_bin:
            ok = self.kwin.write_config("kdeglobals", "General", "ColorScheme", scheme_name)
            if ok:
                self.kwin.reconfigure_kwin()
                return True, f"配色方案已设置为 '{scheme_name}'。"
            return False, "未找到 plasma-apply-colorscheme 且写入 kdeglobals 失败。"

        try:
            res = subprocess.run(
                [self.apply_colorscheme_bin, "-a", scheme_name],
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0:
                self.kwin.reconfigure_kwin()
                return True, f"配色方案已成功应用为 '{scheme_name}'。"
            return False, f"应用配色方案失败: {res.stderr.strip()}"
        except Exception as e:
            return False, f"应用配色方案异常: {e}"

    # ==================== 2. 全局外观包 (Global Look-and-Feel) ====================

    def list_global_themes(self) -> list[str]:
        """列出已安装的全局外观包 ID。"""
        theme_dirs = [
            Path("/usr/share/plasma/look-and-feel"),
            self.data_dir / "plasma" / "look-and-feel",
        ]
        found: set[str] = set()
        for d in theme_dirs:
            if d.exists():
                for sub in d.iterdir():
                    if sub.is_dir() and ((sub / "metadata.json").exists() or (sub / "metadata.desktop").exists()):
                        found.add(sub.name)
        return sorted(list(found))

    def get_current_global_theme(self) -> str:
        """获取当前生效的全局外观包 ID。"""
        return self.kwin.read_config("kdeglobals", "KDE", "LookAndFeelPackage", default="org.kde.breeze.desktop")

    def apply_global_theme(self, theme_id: str) -> tuple[bool, str]:
        """应用全局外观包（调用 plasma-apply-lookandfeel）。"""
        if self.dry_run:
            return True, f"[演练模拟] 将应用全局外观包: {theme_id}"
        if not self.apply_lookandfeel_bin:
            ok = self.kwin.write_config("kdeglobals", "KDE", "LookAndFeelPackage", theme_id)
            if ok:
                self.kwin.reconfigure_kwin()
                return True, f"全局外观包已写入 kdeglobals: '{theme_id}'。"
            return False, "未找到 plasma-apply-lookandfeel 且写入 kdeglobals 失败。"

        try:
            res = subprocess.run(
                [self.apply_lookandfeel_bin, "-a", theme_id],
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0:
                self.kwin.reconfigure_kwin()
                return True, f"全局外观包已成功应用为 '{theme_id}'。"
            return False, f"应用全局外观包失败: {res.stderr.strip()}"
        except Exception as e:
            return False, f"应用全局外观包异常: {e}"

    # ==================== 3. 鼠标指针 (Cursor Themes) ====================

    def list_cursor_themes(self) -> list[str]:
        """列出已安装的鼠标指针主题。"""
        cursor_dirs = [
            Path("/usr/share/icons"),
            self.data_dir / "icons",
            self.home / ".icons",
        ]
        found: set[str] = set()
        for d in cursor_dirs:
            if d.exists():
                for sub in d.iterdir():
                    if sub.is_dir() and (sub / "cursors").exists():
                        found.add(sub.name)
        return sorted(list(found))

    def get_current_cursor_theme(self) -> str:
        """获取当前生效的鼠标指针主题名称。"""
        return self.kwin.read_config("kcminputrc", "Mouse", "cursorTheme", default="breeze_cursors")

    def get_current_cursor_size(self) -> int:
        """获取当前鼠标指针大小像素值。"""
        raw = self.kwin.read_config("kcminputrc", "Mouse", "cursorSize", default="24")
        try:
            return int(raw)
        except ValueError:
            return 24

    def apply_cursor_theme(self, theme_name: str, size: Optional[int] = None) -> tuple[bool, str]:
        """应用指定的鼠标指针主题与大小。"""
        if self.dry_run:
            return True, f"[演练模拟] 将应用鼠标指针: {theme_name} ({size or '默认'}px)"

        # 写入 kcminputrc
        self.kwin.write_config("kcminputrc", "Mouse", "cursorTheme", theme_name)
        if size:
            self.kwin.write_config("kcminputrc", "Mouse", "cursorSize", str(size))

        if self.apply_cursortheme_bin:
            try:
                cmd = [self.apply_cursortheme_bin, theme_name]
                if size:
                    cmd.extend(["--size", str(size)])
                subprocess.run(cmd, capture_output=True, check=False)
            except Exception:
                pass

        self.kwin.reconfigure_kwin()
        return True, f"鼠标指针已设置为 '{theme_name}'。"

    # ==================== 4. 图标主题 (Icon Themes) ====================

    def list_icon_themes(self) -> list[str]:
        """列出已安装的图标主题。"""
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
        """获取当前生效的图标主题名称。"""
        return self.kwin.read_config("kdeglobals", "Icons", "Theme", default="breeze")

    def apply_icon_theme(self, theme_name: str) -> tuple[bool, str]:
        """设置 kdeglobals 中的图标主题。"""
        if self.dry_run:
            return True, f"[演练模拟] 将应用图标主题: {theme_name}"
        ok = self.kwin.write_config("kdeglobals", "Icons", "Theme", theme_name)
        if ok:
            self.kwin.reconfigure_kwin()
            return True, f"图标主题已成功设置为 '{theme_name}'。"
        return False, f"设置图标主题 '{theme_name}' 失败。"

    # ==================== 5. Plasma 桌面样式 (Panel/Taskbar Style) ====================

    def list_plasma_styles(self) -> list[str]:
        """列出已安装的 Plasma 桌面面板与任务栏样式。"""
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
        """获取当前生效的 Plasma 桌面面板样式。"""
        return self.kwin.read_config("plasmarc", "Theme", "name", default="default")

    def apply_plasma_style(self, style_name: str) -> tuple[bool, str]:
        """设置 plasmarc 中的桌面面板样式。"""
        if self.dry_run:
            return True, f"[演练模拟] 将设置 Plasma 桌面面板样式: {style_name}"
        ok = self.kwin.write_config("plasmarc", "Theme", "name", style_name)
        if ok:
            self.kwin.reconfigure_kwin()
            return True, f"Plasma 桌面面板样式已设置为 '{style_name}'。"
        return False, f"设置 Plasma 样式 '{style_name}' 失败。"

    # ==================== 6. Qt6 控件渲染引擎 (Widget Styles) ====================

    def list_widget_styles(self) -> list[str]:
        """列出系统中可用的 Qt 控件渲染引擎 (Breeze, kvantum, Fusion 等)。"""
        styles = {"Breeze", "Fusion", "Oxygen"}
        if shutil.which("kvantummanager") or (Path("/usr/lib/qt6/plugins/styles/libkvantum.so").exists()):
            styles.add("kvantum")
            styles.add("kvantum-dark")
        return sorted(list(styles))

    def get_current_widget_style(self) -> str:
        """获取当前生效的 Qt 控件渲染引擎。"""
        return self.kwin.read_config("kdeglobals", "KDE", "widgetStyle", default="Breeze")

    def apply_widget_style(self, style_name: str) -> tuple[bool, str]:
        """设置 kdeglobals 中的 Qt 控件样式引擎。"""
        if self.dry_run:
            return True, f"[演练模拟] 将设置 Qt 控件样式引擎: {style_name}"
        ok = self.kwin.write_config("kdeglobals", "KDE", "widgetStyle", style_name)
        if ok:
            self.kwin.reconfigure_kwin()
            return True, f"Qt 控件样式引擎已成功设置为 '{style_name}'。"
        return False, f"设置控件引擎 '{style_name}' 失败。"

    # ==================== 7. Kvantum SVG 主题 ====================

    def list_kvantum_themes(self) -> list[str]:
        """列出已安装的 Kvantum SVG 主题。"""
        kv_dirs = [
            Path("/usr/share/Kvantum"),
            self.config_dir / "Kvantum",
            self.data_dir / "Kvantum",
        ]
        found = set()
        for d in kv_dirs:
            if d.exists():
                for sub in d.iterdir():
                    if sub.is_dir() and ((sub / f"{sub.name}.kvconfig").exists() or (sub / f"{sub.name}.svg").exists()):
                        found.add(sub.name)
        return sorted(list(found))

    def get_current_kvantum_theme(self) -> str:
        """获取当前配置的 Kvantum SVG 主题名称。"""
        kv_config = self.config_dir / "Kvantum" / "kvantum.kvconfig"
        if kv_config.exists():
            for line in kv_config.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line.strip().startswith("theme="):
                    return line.strip().split("=", 1)[1].strip()
        return "Default"

    def apply_kvantum_theme(self, theme_name: str) -> tuple[bool, str]:
        """切换 Kvantum SVG 主题配置。"""
        if self.dry_run:
            return True, f"[演练模拟] 将应用 Kvantum 主题: {theme_name}"
        kv_dir = self.config_dir / "Kvantum"
        kv_dir.mkdir(parents=True, exist_ok=True)
        kv_config = kv_dir / "kvantum.kvconfig"
        content = f"[General]\ntheme={theme_name}\n"
        try:
            kv_config.write_text(content, encoding="utf-8")
            self.kwin.reconfigure_kwin()
            return True, f"Kvantum SVG 主题已设置为 '{theme_name}'。"
        except Exception as e:
            return False, f"写入 Kvantum 配置失败: {e}"

    # ==================== 8. 窗口装饰引擎 (Window Decorations) ====================

    def list_window_decorations(self) -> list[str]:
        """列出可用的窗口装饰引擎（如 Breeze 原生 C++ 亚像素渲染、Klassy 等）。"""
        decos = ["org.kde.breeze"]
        if shutil.which("klassy-settings") or Path("/usr/lib/qt6/plugins/org.kde.kdecoration2/klassy.so").exists():
            decos.append("klassy")
        if Path("/usr/lib/qt6/plugins/org.kde.kdecoration2/org.kde.kwin.aurorae.so").exists():
            decos.append("org.kde.kwin.aurorae.v2")
        return decos

    def get_window_decoration(self) -> tuple[str, str]:
        """获取当前激活的窗口装饰库与主题。"""
        lib = self.kwin.read_config("kwinrc", "org.kde.kdecoration2", "library", default="org.kde.breeze")
        theme = self.kwin.read_config("kwinrc", "org.kde.kdecoration2", "theme", default="")
        return lib, theme

    def set_window_decoration(self, library: str, theme: Optional[str] = None) -> tuple[bool, str]:
        """切换窗口装饰引擎并在需要时配置特定主题。"""
        if self.dry_run:
            return True, f"[演练模拟] 将设置窗口装饰: {library} (主题: {theme or '默认'})"
        ok1 = self.kwin.write_config("kwinrc", "org.kde.kdecoration2", "library", library)
        if theme:
            self.kwin.write_config("kwinrc", "org.kde.kdecoration2", "theme", theme)
        self.kwin.reconfigure_kwin()
        if ok1:
            return True, f"窗口装饰已成功设置为 '{library}'。"
        return False, "设置窗口装饰失败。"

    # ==================== 9. GTK 3/4 样式同步 ====================

    def sync_gtk_theme(self, gtk_theme: Optional[str] = None, dark_mode: bool = True) -> tuple[bool, str]:
        """同步 GTK 3/4 主题、暗色模式偏好与图标指针至 KDE 一致。"""
        if self.dry_run:
            return True, f"[演练模拟] 将同步 GTK 主题为: {gtk_theme or 'Breeze'} (暗色: {dark_mode})"

        cur_icon = self.get_current_icon_theme()
        cur_cursor = self.get_current_cursor_theme()
        chosen_gtk = gtk_theme or ("Breeze-Dark" if dark_mode else "Breeze")

        # 写入 ~/.config/gtk-3.0/settings.ini
        gtk3_dir = self.config_dir / "gtk-3.0"
        gtk3_dir.mkdir(parents=True, exist_ok=True)
        gtk3_file = gtk3_dir / "settings.ini"
        gtk3_content = f"""[Settings]
gtk-theme-name={chosen_gtk}
gtk-icon-theme-name={cur_icon}
gtk-cursor-theme-name={cur_cursor}
gtk-application-prefer-dark-theme={1 if dark_mode else 0}
"""
        # 写入 ~/.config/gtk-4.0/settings.ini
        gtk4_dir = self.config_dir / "gtk-4.0"
        gtk4_dir.mkdir(parents=True, exist_ok=True)
        gtk4_file = gtk4_dir / "settings.ini"

        try:
            gtk3_file.write_text(gtk3_content, encoding="utf-8")
            gtk4_file.write_text(gtk3_content, encoding="utf-8")
            return True, f"GTK 3/4 样式已成功同步至 '{chosen_gtk}'。"
        except Exception as e:
            return False, f"写入 GTK 配置文件失败: {e}"

    # ==================== 10. 系统字体配置 ====================

    def get_fonts(self) -> dict[str, str]:
        """获取当前配置的 KDE 系统字体字典。"""
        return {
            "general": self.kwin.read_config("kdeglobals", "General", "font", default=""),
            "fixed": self.kwin.read_config("kdeglobals", "General", "fixed", default=""),
            "windowtitle": self.kwin.read_config("kdeglobals", "WM", "activeFont", default=""),
            "menu": self.kwin.read_config("kdeglobals", "General", "menuFont", default=""),
            "toolbar": self.kwin.read_config("kdeglobals", "General", "toolBarFont", default=""),
            "small": self.kwin.read_config("kdeglobals", "General", "smallestReadableFont", default=""),
        }

    def set_font(self, category: str, font_spec: str) -> tuple[bool, str]:
        """设置指定分类的系统字体规格。"""
        if self.dry_run:
            return True, f"[演练模拟] 将设置字体 [{category}] 为 '{font_spec}'"
        cat_map = {
            "general": ("General", "font"),
            "fixed": ("General", "fixed"),
            "windowtitle": ("WM", "activeFont"),
            "menu": ("General", "menuFont"),
            "toolbar": ("General", "toolBarFont"),
            "small": ("General", "smallestReadableFont"),
        }
        if category.lower() not in cat_map:
            return False, f"未知的字体分类: {category}"

        grp, key = cat_map[category.lower()]
        ok = self.kwin.write_config("kdeglobals", grp, key, font_spec)
        if ok:
            self.kwin.reconfigure_kwin()
            return True, f"字体分类 [{category}] 已成功更新为 '{font_spec}'。"
        return False, f"更新字体分类 [{category}] 失败。"
