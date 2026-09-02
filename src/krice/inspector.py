"""KDE Plasma 6 桌面环境、主题视觉、流体动效与终端生态诊断器。"""

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
    """桌面全要素诊断数据结构。"""

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
    task_switcher: str
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
    """全面诊断当前系统的 KDE 视觉属性、动效物理参数与终端工具集成状态。"""

    def __init__(self) -> None:
        self.kwin = KWinController()
        self.theme = ThemeController()
        self.term = TerminalController()

    def inspect(self) -> DesktopReport:
        """执行全方位诊断并返回结构化报告对象。"""
        session_type = os.environ.get("XDG_SESSION_TYPE", "未知").upper()

        # 1. 查询 Plasma 版本
        plasmashell_bin = shutil.which("plasmashell")
        plasma_ver = "未知"
        if plasmashell_bin:
            try:
                out = subprocess.check_output([plasmashell_bin, "--version"], text=True, stderr=subprocess.DEVNULL)
                plasma_ver = out.strip().replace("plasmashell ", "")
            except Exception:
                pass

        # 2. 视觉主题配置
        global_theme = self.theme.get_current_global_theme()
        color_scheme = self.theme.get_current_colorscheme()
        cursor_theme = self.theme.get_current_cursor_theme()
        cursor_size = self.theme.get_current_cursor_size()
        icon_theme = self.theme.get_current_icon_theme()
        plasma_style = self.theme.get_current_plasma_style()
        widget_style = self.theme.get_current_widget_style()
        kvantum_theme = self.theme.get_current_kvantum_theme()
        deco_lib, deco_theme = self.theme.get_window_decoration()
        window_deco = f"{deco_lib} ({deco_theme})" if deco_theme else deco_lib

        # GTK 主题读取
        gtk3_file = Path.home() / ".config" / "gtk-3.0" / "settings.ini"
        gtk_theme = "Breeze"
        if gtk3_file.exists():
            for line in gtk3_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line.strip().startswith("gtk-theme-name="):
                    gtk_theme = line.strip().split("=", 1)[1].strip()

        # 欢迎屏幕
        ksplashrc = Path.home() / ".config" / "ksplashrc"
        splash_theme = "org.kde.breeze.desktop"
        if ksplashrc.exists():
            for line in ksplashrc.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line.strip().startswith("Theme="):
                    splash_theme = line.strip().split("=", 1)[1].strip()

        # 3. KWin 动效参数
        anim_factor = self.kwin.get_animation_factor()
        scale_on = self.kwin.get_plugin_status("scale")
        fade_on = self.kwin.get_plugin_status("fade")
        glide_on = self.kwin.get_plugin_status("glide")

        if scale_on:
            open_close_effect = "Scale (流体缩放)"
        elif fade_on:
            open_close_effect = "Fade (淡入淡出)"
        elif glide_on:
            open_close_effect = "Glide (平滑滑动)"
        else:
            open_close_effect = "无动效 (即时)"

        squash_on = self.kwin.get_plugin_status("squash")
        magic_on = self.kwin.get_plugin_status("magiclamp")
        if squash_on:
            minimize_effect = "Squash (挤压)"
        elif magic_on:
            minimize_effect = "Magic Lamp (神灯卷轴)"
        else:
            minimize_effect = "默认"

        task_switcher = self.kwin.get_tabbox_layout()
        blur_on = self.kwin.get_plugin_status("blur")
        morphing_on = self.kwin.get_plugin_status("kwin4_effect_morphingpopups")
        wobbly_on = self.kwin.get_plugin_status("wobblywindows")

        # 4. 已安装的第三方增强引擎
        klassy_installed = (
            shutil.which("klassy-settings") is not None
            or Path("/usr/lib/qt6/plugins/org.kde.kdecoration2/klassy.so").exists()
        )
        kvantum_installed = (
            shutil.which("kvantummanager") is not None
            or Path("/usr/lib/qt6/plugins/styles/libkvantum.so").exists()
        )
        forceblur_installed = (
            shutil.which("kwin_forceblur_config") is not None
            or (Path.home() / ".local/share/kwin/effects/forceblur").exists()
        )

        # 5. 终端生态检测
        detected_terms = self.term.detect_installed_terminals()
        installed_terminals = [
            k.capitalize()
            for k, v in detected_terms.items()
            if v and k not in ("starship", "fastfetch")
        ]
        starship_installed = detected_terms.get("starship", False)
        fastfetch_installed = detected_terms.get("fastfetch", False)

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
            window_decoration=window_deco,
            gtk_theme=gtk_theme,
            splash_theme=splash_theme,
            animation_factor=anim_factor,
            window_open_close_effect=open_close_effect,
            window_minimize_effect=minimize_effect,
            task_switcher=task_switcher,
            blur_enabled=blur_on,
            morphing_popups=morphing_on,
            wobbly_windows=wobbly_on,
            klassy_installed=klassy_installed,
            kvantum_installed=kvantum_installed,
            forceblur_installed=forceblur_installed,
            installed_terminals=installed_terminals,
            starship_installed=starship_installed,
            fastfetch_installed=fastfetch_installed,
        )
