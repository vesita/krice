"""多终端模拟器与 Shell 提示符调色板控制器（支持 Kitty、Alacritty、Konsole、Ghostty、Foot、WezTerm、Zellij、Starship、Fastfetch）。"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from krice.presets.prompt_presets import generate_fastfetch_config, generate_starship_config
from krice.presets.terminal_palettes import CACHY_NORD, CYAN_LIGHT, NORD_LIGHT, TERMINAL_PALETTES, TerminalPalette


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """将十六进制颜色值 (#RRGGBB 或 #RGB) 转换为 (R, G, B) 整数元组。"""
    hex_clean = hex_color.lstrip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join([c * 2 for c in hex_clean])
    if len(hex_clean) != 6:
        return (0, 0, 0)
    return (int(hex_clean[0:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """将 (R, G, B) 整数转换为标准的 #RRGGBB 十六进制大写字符串。"""
    return f"#{r:02X}{g:02X}{b:02X}"


def parse_kde_rgb(kde_str: str, default_hex: str = "#000000") -> str:
    """解析 KDE 配置文件中的 'R,G,B' 格式颜色字符串为十六进制 #RRGGBB 格式。"""
    parts = kde_str.strip().split(",")
    if len(parts) >= 3:
        try:
            r = max(0, min(255, int(parts[0].strip())))
            g = max(0, min(255, int(parts[1].strip())))
            b = max(0, min(255, int(parts[2].strip())))
            return rgb_to_hex(r, g, b)
        except ValueError:
            pass
    return default_hex


class TerminalController:
    """管理并同步终端模拟器与 Shell 提示符工具的色彩、字体与视觉布局。"""

    def __init__(self, dry_run: bool = False, home_dir: Optional[Path] = None) -> None:
        self.dry_run = dry_run
        self.home = home_dir or Path.home()
        self.config_dir = Path(os.environ.get("XDG_CONFIG_HOME", str(self.home / ".config")))
        self.data_dir = Path(os.environ.get("XDG_DATA_HOME", str(self.home / ".local" / "share")))

    def get_palette(self, name: str) -> Optional[TerminalPalette]:
        """根据名称获取预设的终端调色板。"""
        return TERMINAL_PALETTES.get(name.lower())

    def list_palettes(self) -> dict[str, TerminalPalette]:
        """列出所有已注册的终端调色板。"""
        return TERMINAL_PALETTES

    def detect_installed_terminals(self) -> dict[str, bool]:
        """检测当前系统已安装或已配置的终端模拟器与命令行工具。"""
        return {
            "konsole": shutil.which("konsole") is not None or (self.data_dir / "konsole").exists(),
            "alacritty": shutil.which("alacritty") is not None or (self.config_dir / "alacritty").exists(),
            "kitty": shutil.which("kitty") is not None or (self.config_dir / "kitty").exists(),
            "ghostty": shutil.which("ghostty") is not None or (self.config_dir / "ghostty").exists(),
            "foot": shutil.which("foot") is not None or (self.config_dir / "foot").exists(),
            "wezterm": shutil.which("wezterm") is not None or (self.config_dir / "wezterm").exists(),
            "zellij": shutil.which("zellij") is not None or (self.config_dir / "zellij").exists(),
            "starship": shutil.which("starship") is not None or (self.config_dir / "starship.toml").exists(),
            "fastfetch": shutil.which("fastfetch") is not None or (self.config_dir / "fastfetch").exists(),
        }

    # ==================== 从当前 KDE 配色中智能提取调色板 ====================

    def extract_palette_from_kde(self) -> TerminalPalette:
        """从当前系统的 ~/.config/kdeglobals 中智能提取活动配色方案，生成高对比度 16 色 ANSI 调色板。"""
        kdeglobals = self.config_dir / "kdeglobals"
        bg = "#F0F6F6"
        fg = "#1A282D"
        sel_bg = "#C8E6E6"
        sel_fg = "#0F3D39"
        accent = "#0891B2"

        if kdeglobals.exists():
            content = kdeglobals.read_text(encoding="utf-8", errors="ignore")
            # 提取 [Colors:View] 或 [Colors:Window]
            m_bg = re.search(r"\[Colors:View\][^\[]*?BackgroundNormal=([0-9,]+)", content)
            if not m_bg:
                m_bg = re.search(r"\[Colors:Window\][^\[]*?BackgroundNormal=([0-9,]+)", content)
            if m_bg:
                bg = parse_kde_rgb(m_bg.group(1), bg)

            m_fg = re.search(r"\[Colors:View\][^\[]*?ForegroundNormal=([0-9,]+)", content)
            if not m_fg:
                m_fg = re.search(r"\[Colors:Window\][^\[]*?ForegroundNormal=([0-9,]+)", content)
            if m_fg:
                fg = parse_kde_rgb(m_fg.group(1), fg)

            m_sel_bg = re.search(r"\[Colors:Selection\][^\[]*?BackgroundNormal=([0-9,]+)", content)
            if m_sel_bg:
                sel_bg = parse_kde_rgb(m_sel_bg.group(1), sel_bg)

            m_sel_fg = re.search(r"\[Colors:Selection\][^\[]*?ForegroundNormal=([0-9,]+)", content)
            if m_sel_fg:
                sel_fg = parse_kde_rgb(m_sel_fg.group(1), sel_fg)

            accent = sel_bg if sel_bg else ("#0891B2" if not is_dark else "#88C0D0")
            m_accent = re.search(r"\[General\][^\[]*?AccentColor=([0-9,]+)", content)
            if m_accent:
                accent = parse_kde_rgb(m_accent.group(1), accent)
        # 计算亮度以判断暗色/亮色模式
        r, g, b = hex_to_rgb(bg)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        is_dark = brightness < 128

        if not is_dark:
            # 浅色模式调色板（青翠冰霜）
            return TerminalPalette(
                name="kde-extracted",
                display_name="KDE Extracted (Cyan Ice Daylight / 冰青极光)",
                background=bg,
                foreground=fg,
                dim_foreground="#52707A",
                bright_foreground="#0B171B",
                cursor=accent,
                cursor_text="#FFFFFF",
                selection_bg=sel_bg,
                selection_fg=sel_fg,
                black="#1A282D",
                red="#E11D48",
                green="#059669",
                yellow="#D97706",
                blue=accent,
                magenta="#7C3AED",
                cyan="#0D9488",
                white="#E0EEEE",
                bright_black="#5E7A85",
                bright_red="#F43F5E",
                bright_green="#10B981",
                bright_yellow="#F59E0B",
                bright_blue="#06B6D4",
                bright_magenta="#8B5CF6",
                bright_cyan="#14B8A6",
                bright_white="#FFFFFF",
                is_dark=False,
            )
        else:
            # 暗色模式调色板
            return TerminalPalette(
                name="kde-extracted",
                display_name="KDE Extracted Palette (Live Sync)",
                background=bg,
                foreground=fg,
                dim_foreground="#7684A0",
                bright_foreground="#FFFFFF",
                cursor=accent,
                cursor_text=bg,
                selection_bg=sel_bg,
                selection_fg=sel_fg,
                black="#2E3440",
                red="#BF616A",
                green="#A3BE8C",
                yellow="#EBCB8B",
                blue=accent,
                magenta="#B48EAD",
                cyan="#88C0D0",
                white="#E5E9F0",
                bright_black="#7684A0",
                bright_red="#D08770",
                bright_green="#A3BE8C",
                bright_yellow="#EBCB8B",
                bright_blue="#81A1C1",
                bright_magenta="#B48EAD",
                bright_cyan="#8FD5E6",
                bright_white="#ECEFF4",
                is_dark=True,
            )

    def get_system_monospace_font(self) -> tuple[str, float]:
        """从 kdeglobals 中读取当前 KDE 桌面配置的等宽字体名称与字号。"""
        kdeglobals = self.config_dir / "kdeglobals"
        if kdeglobals.exists():
            content = kdeglobals.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"fixed=([^,\n]+)", content)
            if m:
                font_name = m.group(1).strip()
                line = content[m.start():content.find("\n", m.start())]
                parts = line.split(",")
                size = 11.5
                if len(parts) >= 2:
                    try:
                        s = float(parts[1].strip())
                        if 8.0 <= s <= 24.0:
                            size = s
                    except ValueError:
                        pass
                if font_name:
                    return font_name, size
        return "MesloLGS Nerd Font", 11.5

    def _resolve_palette(self, palette_or_name: Union[str, TerminalPalette]) -> Optional[TerminalPalette]:
        """智能解析调色板：接收名称字符串或 TerminalPalette 实例并返回对应对象。"""
        if isinstance(palette_or_name, str):
            return self.get_palette(palette_or_name)
        return palette_or_name

    # ==================== 各终端独立配置写入逻辑 ====================

    # 1. Konsole (KDE 原生终端)
    def apply_konsole(self, palette: Union[str, TerminalPalette]) -> tuple[bool, str]:
        """应用配色方案至 KDE 原生 Konsole 终端。"""
        pal = self._resolve_palette(palette)
        if not pal:
            return False, f"未知的调色板 '{palette}'"
        palette = pal

        if self.dry_run:
            return True, f"[演练模拟] 将为 Konsole 应用配色方案: krice-{palette.name}"

        scheme_dir = self.data_dir / "konsole"
        scheme_dir.mkdir(parents=True, exist_ok=True)
        scheme_file = scheme_dir / f"krice-{palette.name}.colorscheme"

        def hex_rgb_str(hex_val: str) -> str:
            r, g, b = hex_to_rgb(hex_val)
            return f"{r},{g},{b}"

        lines = [
            "[General]",
            f"Description=krice {palette.display_name}",
            "Blur=true",
            "Opacity=0.94",
            f"[Background]\nColor={hex_rgb_str(palette.background)}",
            f"[BackgroundIntense]\nColor={hex_rgb_str(palette.background)}",
            f"[Foreground]\nColor={hex_rgb_str(palette.foreground)}",
            f"[ForegroundIntense]\nColor={hex_rgb_str(palette.bright_foreground or palette.foreground)}",
            f"[Color0]\nColor={hex_rgb_str(palette.black)}",
            f"[Color0Intense]\nColor={hex_rgb_str(palette.bright_black)}",
            f"[Color1]\nColor={hex_rgb_str(palette.red)}",
            f"[Color1Intense]\nColor={hex_rgb_str(palette.bright_red)}",
            f"[Color2]\nColor={hex_rgb_str(palette.green)}",
            f"[Color2Intense]\nColor={hex_rgb_str(palette.bright_green)}",
            f"[Color3]\nColor={hex_rgb_str(palette.yellow)}",
            f"[Color3Intense]\nColor={hex_rgb_str(palette.bright_yellow)}",
            f"[Color4]\nColor={hex_rgb_str(palette.blue)}",
            f"[Color4Intense]\nColor={hex_rgb_str(palette.bright_blue)}",
            f"[Color5]\nColor={hex_rgb_str(palette.magenta)}",
            f"[Color5Intense]\nColor={hex_rgb_str(palette.bright_magenta)}",
            f"[Color6]\nColor={hex_rgb_str(palette.cyan)}",
            f"[Color6Intense]\nColor={hex_rgb_str(palette.bright_cyan)}",
            f"[Color7]\nColor={hex_rgb_str(palette.white)}",
            f"[Color7Intense]\nColor={hex_rgb_str(palette.bright_white)}",
        ]
        try:
            scheme_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            # 确保 konsolerc 与默认 Profile 存在
            self.config_dir.mkdir(parents=True, exist_ok=True)
            konsolerc = self.config_dir / "konsolerc"
            if not konsolerc.exists():
                konsolerc.write_text("[Desktop Entry]\nDefaultProfile=krice.profile\n", encoding="utf-8")
        except Exception as e:
            return False, f"写入 Konsole 配色方案失败: {e}"

        return True, f"Konsole 主题已成功设置为 'krice-{palette.name}'。"

    # 2. Alacritty
    def apply_alacritty(self, palette: Union[str, TerminalPalette]) -> tuple[bool, str]:
        """应用配色方案至 Alacritty 终端 (alacritty.toml)。"""
        pal = self._resolve_palette(palette)
        if not pal:
            return False, f"未知的调色板 '{palette}'"
        palette = pal

        if self.dry_run:
            return True, f"[演练模拟] 将为 Alacritty 应用调色板: {palette.name}"

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
"""
        try:
            if config_path.exists():
                content = config_path.read_text(encoding="utf-8")
                content = re.sub(r"\[colors.*?(\n\[|\Z)", r"\1", content, flags=re.DOTALL).strip()
                content += "\n\n" + colors_toml
                config_path.write_text(content.strip() + "\n", encoding="utf-8")
            else:
                config_path.write_text(
                    f"""# Alacritty Configuration - Managed by krice
[window]
opacity = 0.88
blur = true
padding = {{ x = 0, y = 0 }}

[font]
size = 11.5
normal = {{ family = "MesloLGS Nerd Font", style = "Regular" }}

{colors_toml}
""",
                    encoding="utf-8",
                )

            return True, f"Alacritty 配色已成功设置为 '{palette.name}'。"
        except Exception as e:
            return False, f"更新 Alacritty 配置失败: {e}"

    # 3. Kitty
    def apply_kitty(self, palette: Union[str, TerminalPalette]) -> tuple[bool, str]:
        """应用配色方案至 Kitty 终端（包含顶部圆角药丸 Tab 与磨砂亚克力玻璃）。"""
        pal = self._resolve_palette(palette)
        if not pal:
            return False, f"未知的调色板 '{palette}'"
        palette = pal

        if self.dry_run:
            return True, f"[演练模拟] 将为 Kitty 应用调色板: {palette.name}"

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

# Tab bar colors (Rounded Pill / Bubble Tabs)
active_tab_background {palette.blue}
active_tab_foreground #FFFFFF
inactive_tab_background {palette.selection_bg}
inactive_tab_foreground {palette.dim_foreground or '#52707A'}
tab_bar_background {palette.background}
tab_bar_margin_color {palette.background}

# Window borders
active_border_color {palette.blue}
inactive_border_color {palette.selection_bg}
"""
        try:
            theme_file.write_text(theme_content, encoding="utf-8")
            if main_config.exists():
                c_txt = main_config.read_text(encoding="utf-8")
                if "include current-theme.conf" not in c_txt:
                    main_config.write_text("include current-theme.conf\n" + c_txt, encoding="utf-8")
            else:
                default_kitty_conf = f"""# Kitty Terminal Configuration - Managed by krice
include current-theme.conf

# 排版字体设置
font_family      MesloLGS Nerd Font
bold_font        auto
italic_font      auto
bold_italic_font auto
font_size        11.5

# 窗口与亚克力磨砂毛玻璃
window_padding_width 0
background_opacity 0.78
background_blur 32
dynamic_background_opacity yes

# 光标样式
cursor_shape beam
cursor_beam_thickness 1.8
cursor_blink_interval 0.5

# 顶部圆角药丸 Tab 栏 (Top Powerline Rounded Bubble Tabs)
tab_bar_edge top
tab_bar_style powerline
tab_powerline_style round
tab_bar_min_tabs 1
tab_bar_margin_width 6.0
tab_bar_margin_height 6.0 0.0
tab_title_template " 󰓩 {{index}}: {{title}} "
active_tab_font_style bold
inactive_tab_font_style normal

# 快捷键配置
map ctrl+shift+t new_tab
map ctrl+shift+w close_tab
map ctrl+shift+right next_tab
map ctrl+shift+left previous_tab
map ctrl+shift+1 goto_tab 1
map ctrl+shift+2 goto_tab 2
map ctrl+shift+3 goto_tab 3
map ctrl+shift+4 goto_tab 4
map ctrl+shift+5 goto_tab 5

# 实时透明度调节快捷键
map ctrl+shift+u set_background_opacity +0.05
map ctrl+shift+o set_background_opacity -0.05
map ctrl+shift+delete set_background_opacity default
"""
                main_config.write_text(default_kitty_conf, encoding="utf-8")

            # 向 Kitty 进程发送热重载信号
            try:
                subprocess.run(["pkill", "-USR1", "kitty"], check=False, capture_output=True)
            except Exception:
                pass

            return True, f"Kitty 主题已成功设置为 '{palette.name}'。"
        except Exception as e:
            return False, f"更新 Kitty 配置失败: {e}"

    # 4. Ghostty
    def apply_ghostty(self, palette: Union[str, TerminalPalette]) -> tuple[bool, str]:
        """应用配色方案至 Ghostty 终端。"""
        pal = self._resolve_palette(palette)
        if not pal:
            return False, f"未知的调色板 '{palette}'"
        palette = pal

        if self.dry_run:
            return True, f"[演练模拟] 将为 Ghostty 应用调色板: {palette.name}"

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
                c_txt = config_path.read_text(encoding="utf-8")
                if "theme = " in c_txt:
                    c_txt = re.sub(r"theme\s*=\s*.*", f"theme = krice-{palette.name}", c_txt)
                else:
                    c_txt = f"theme = krice-{palette.name}\n" + c_txt
                config_path.write_text(c_txt, encoding="utf-8")
            else:
                config_path.write_text(f"theme = krice-{palette.name}\nbackground-opacity = 0.94\n", encoding="utf-8")

            return True, f"Ghostty 主题已设置为 'krice-{palette.name}'。"
        except Exception as e:
            return False, f"更新 Ghostty 配置失败: {e}"

    # 5. Foot
    def apply_foot(self, palette: Union[str, TerminalPalette]) -> tuple[bool, str]:
        """应用配色方案至 Foot Wayland 终端。"""
        pal = self._resolve_palette(palette)
        if not pal:
            return False, f"未知的调色板 '{palette}'"
        palette = pal

        if self.dry_run:
            return True, f"[演练模拟] 将为 Foot 应用调色板: {palette.name}"

        foot_dir = self.config_dir / "foot"
        foot_dir.mkdir(parents=True, exist_ok=True)
        config_path = foot_dir / "foot.ini"

        def hex_no_hash(h: str) -> str:
            return h.lstrip("#")

        colors_ini = f"""[colors]
alpha=0.94
background={hex_no_hash(palette.background)}
foreground={hex_no_hash(palette.foreground)}
regular0={hex_no_hash(palette.black)}
regular1={hex_no_hash(palette.red)}
regular2={hex_no_hash(palette.green)}
regular3={hex_no_hash(palette.yellow)}
regular4={hex_no_hash(palette.blue)}
regular5={hex_no_hash(palette.magenta)}
regular6={hex_no_hash(palette.cyan)}
regular7={hex_no_hash(palette.white)}
bright0={hex_no_hash(palette.bright_black)}
bright1={hex_no_hash(palette.bright_red)}
bright2={hex_no_hash(palette.bright_green)}
bright3={hex_no_hash(palette.bright_yellow)}
bright4={hex_no_hash(palette.bright_blue)}
bright5={hex_no_hash(palette.bright_magenta)}
bright6={hex_no_hash(palette.bright_cyan)}
bright7={hex_no_hash(palette.bright_white)}
"""
        try:
            if config_path.exists():
                c_txt = config_path.read_text(encoding="utf-8")
                c_txt = re.sub(r"\[colors.*?(\n\[|\Z)", r"\1", c_txt, flags=re.DOTALL).strip()
                c_txt += "\n\n" + colors_ini
                config_path.write_text(c_txt.strip() + "\n", encoding="utf-8")
            else:
                config_path.write_text(
                    f"""# Foot Configuration - Managed by krice
[main]
font=MesloLGS Nerd Font:size=11.5
pad=0x0

{colors_ini}
""",
                    encoding="utf-8",
                )
            return True, f"Foot 主题已设置为 '{palette.name}'。"
        except Exception as e:
            return False, f"更新 Foot 配置失败: {e}"

    # 6. WezTerm
    def apply_wezterm(self, palette: Union[str, TerminalPalette]) -> tuple[bool, str]:
        """应用配色方案至 WezTerm 终端。"""
        pal = self._resolve_palette(palette)
        if not pal:
            return False, f"未知的调色板 '{palette}'"
        palette = pal

        if self.dry_run:
            return True, f"[演练模拟] 将为 WezTerm 应用调色板: {palette.name}"

        wezterm_dir = self.config_dir / "wezterm"
        colors_dir = wezterm_dir / "colors"
        colors_dir.mkdir(parents=True, exist_ok=True)
        theme_file = colors_dir / f"krice-{palette.name}.toml"

        theme_toml = f"""[colors]
background = "{palette.background}"
foreground = "{palette.foreground}"
cursor_bg = "{palette.cursor}"
cursor_border = "{palette.cursor}"
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
            config_lua = wezterm_dir / "wezterm.lua"
            if config_lua.exists():
                c_txt = config_lua.read_text(encoding="utf-8")
                if "color_scheme" in c_txt:
                    c_txt = re.sub(r'color_scheme\s*=\s*["\'].*?["\']', f'color_scheme = "krice-{palette.name}"', c_txt)
                else:
                    c_txt = f'config.color_scheme = "krice-{palette.name}"\n' + c_txt
                config_lua.write_text(c_txt, encoding="utf-8")
            return True, f"WezTerm 主题已设置为 'krice-{palette.name}'。"
        except Exception as e:
            return False, f"更新 WezTerm 配置失败: {e}"

    # 6b. Zellij
    def apply_zellij(self, palette: Union[str, TerminalPalette]) -> tuple[bool, str]:
        """应用配色方案至 Zellij 终端多路复用器。"""
        pal = self._resolve_palette(palette)
        if not pal:
            return False, f"未知的调色板 '{palette}'"
        palette = pal

        if self.dry_run:
            return True, f"[演练模拟] 将为 Zellij 应用调色板: {palette.name}"

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
                config_file.write_text(f'theme "krice-{palette.name}"\ndefault_layout "compact"\n', encoding="utf-8")
            return True, f"Zellij 主题已设置为 'krice-{palette.name}'。"
        except Exception as e:
            return False, f"更新 Zellij 配置失败: {e}"

    # 7. Starship Shell 提示符
    def apply_starship(self, palette: Union[str, TerminalPalette]) -> tuple[bool, str]:
        """应用匹配的 Starship 全圆角工作目录胶囊提示符配置。"""
        pal = self._resolve_palette(palette)
        if not pal:
            return False, f"未知的调色板 '{palette}'"
        palette = pal

        if self.dry_run:
            return True, f"[演练模拟] 将为 Starship 应用调色板: {palette.name}"

        starship_file = self.config_dir / "starship.toml"
        starship_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            config_content = generate_starship_config(palette)
            starship_file.write_text(config_content, encoding="utf-8")
            return True, f"Starship 提示符已成功匹配调色板 '{palette.display_name}'。"
        except Exception as e:
            return False, f"更新 starship.toml 失败: {e}"

    # 8. Fastfetch
    def apply_fastfetch(self, palette: Union[str, TerminalPalette]) -> tuple[bool, str]:
        """应用匹配的 Fastfetch 硬件美化展示看板配色。"""
        pal = self._resolve_palette(palette)
        if not pal:
            return False, f"未知的调色板 '{palette}'"
        palette = pal

        if self.dry_run:
            return True, f"[演练模拟] 将为 Fastfetch 应用调色板: {palette.name}"

        fastfetch_dir = self.config_dir / "fastfetch"
        fastfetch_dir.mkdir(parents=True, exist_ok=True)
        config_path = fastfetch_dir / "config.jsonc"
        try:
            content = generate_fastfetch_config(palette)
            config_path.write_text(content, encoding="utf-8")
            return True, f"Fastfetch 硬件看板已成功匹配调色板 '{palette.display_name}'。"
        except Exception as e:
            return False, f"更新 Fastfetch 配置失败: {e}"

    # --- 全终端统一批量应用 ---

    def apply_all(
        self,
        palette_or_name: Union[str, TerminalPalette],
        terminals: Optional[list[str]] = None,
    ) -> dict[str, tuple[bool, str]]:
        """全量同步应用调色板至所有已安装的终端模拟器与 Shell 工具。"""
        if isinstance(palette_or_name, str):
            palette = self.get_palette(palette_or_name)
            if not palette:
                palette = self.extract_palette_from_kde()
        else:
            palette = palette_or_name

        results: dict[str, tuple[bool, str]] = {}
        detected = self.detect_installed_terminals()
        allowed = [t.lower() for t in terminals] if terminals else None

        def should_run(key: str) -> bool:
            if allowed is None:
                return True
            return key.lower() in allowed

        if should_run("konsole") and detected.get("konsole", True):
            results["Konsole"] = self.apply_konsole(palette)

        if should_run("alacritty") and detected.get("alacritty", True):
            results["Alacritty"] = self.apply_alacritty(palette)

        if should_run("kitty") and (detected.get("kitty", False) or (self.config_dir / "kitty").exists()):
            results["Kitty"] = self.apply_kitty(palette)

        if should_run("ghostty") and (detected.get("ghostty", False) or (self.config_dir / "ghostty").exists()):
            results["Ghostty"] = self.apply_ghostty(palette)

        if should_run("foot") and (detected.get("foot", False) or (self.config_dir / "foot").exists()):
            results["Foot"] = self.apply_foot(palette)

        if should_run("wezterm") and (detected.get("wezterm", False) or (self.config_dir / "wezterm").exists()):
            results["WezTerm"] = self.apply_wezterm(palette)

        if should_run("zellij") and (detected.get("zellij", False) or (self.config_dir / "zellij").exists()):
            results["Zellij"] = self.apply_zellij(palette)

        if should_run("starship") and detected.get("starship", True):
            results["Starship"] = self.apply_starship(palette)

        if should_run("fastfetch") and detected.get("fastfetch", True):
            results["Fastfetch"] = self.apply_fastfetch(palette)

        return results
