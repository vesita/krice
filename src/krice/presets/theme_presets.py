"""全局桌面美化方案库（融合 KDE 全局主题 + 窗口装饰 + 多终端调色 + 物理动效）。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RicePreset:
    """整合式桌面美化方案数据结构，统筹 KDE 主题、终端配色与 KWin 动效。"""

    name: str
    description: str
    is_dark: bool = True
    global_theme: Optional[str] = None
    color_scheme: Optional[str] = None
    plasma_style: Optional[str] = None
    widget_style: Optional[str] = None
    kvantum_theme: Optional[str] = None
    window_decoration_lib: Optional[str] = None
    window_decoration_theme: Optional[str] = None
    cursor_theme: Optional[str] = None
    cursor_size: int = 24
    icon_theme: Optional[str] = None
    gtk_theme: Optional[str] = None
    terminal_palette: Optional[str] = None
    motion_preset: str = "denial"
    notes: list[str] = field(default_factory=list)


# --- 1. CachyOS Nord 暗色风格 ---
CACHY_NORD_RICE = RicePreset(
    name="CachyOS Arctic Nord",
    description="北欧极光深邃暗色风格，搭配 CachyOS 标志性青色强调与流体缩放",
    is_dark=True,
    global_theme="com.github.vinceliuice.Orchis-dark",
    color_scheme="CachyOSNord",
    plasma_style="Orchis-dark",
    widget_style="Breeze",
    kvantum_theme="Nordic",
    window_decoration_lib="org.kde.breeze",
    cursor_theme="Vimix-cursors",
    cursor_size=24,
    icon_theme="Tela-circle-nord",
    gtk_theme="Orchis-Dark",
    terminal_palette="cachy-nord",
    motion_preset="denial",
    notes=[
        "Breeze 原生 C++ 亚像素窗口装饰，彻底消除 1.7x 分数缩放下的像素错位。",
        "Starship 胶囊提示符，显示当前工作目录、Git 状态与执行耗时。",
        "Kitty 终端圆角药丸 Tab，亚克力毛玻璃模糊透明。",
    ],
)

# --- 2. 冰青极光浅色风格 (Cyan Mint Light) ---
CYAN_MINT_LIGHT_RICE = RicePreset(
    name="Cyan Mint Glacier Light",
    description="清新柔和的冰青极光浅色风格（湖水青主调、半透明磨砂亚克力与圆角药丸胶囊）",
    is_dark=False,
    global_theme="com.github.vinceliuice.Orchis",
    color_scheme="Orchis",
    plasma_style="Orchis",
    widget_style="Breeze",
    kvantum_theme="Default",
    window_decoration_lib="org.kde.breeze",
    cursor_theme="Vimix-cursors",
    cursor_size=24,
    icon_theme="Tela-circle",
    gtk_theme="Orchis-Light",
    terminal_palette="cyan-light",
    motion_preset="denial",
    notes=[
        "冰青极光高对比度调色板，在浅色背景下提供 5.2:1 的优异文字可读性。",
        "Kitty 顶部圆角药丸 Tab 与 0.78 亚克力毛玻璃磨砂玻璃质感。",
        "Starship 全圆角胶囊药丸提示符（包含当前工作目录胶囊、Git 与耗时指示）。",
    ],
)

# --- 3. Catppuccin Mocha 现代柔和暗色 ---
CATPPUCCIN_MOCHA_RICE = RicePreset(
    name="Catppuccin Mocha",
    description="舒缓柔和的摩卡粉彩暗色风格，搭配紫色高亮与 150ms 灵动弹簧动效",
    is_dark=True,
    global_theme="Catppuccin-Mocha-Mauve",
    color_scheme="CatppuccinMochaMauve",
    plasma_style="Catppuccin-Mocha-Mauve",
    widget_style="Breeze",
    kvantum_theme="Catppuccin-Mocha-Mauve",
    window_decoration_lib="org.kde.breeze",
    cursor_theme="Catppuccin-Mocha-Mauve-Cursors",
    cursor_size=24,
    icon_theme="Papirus-Dark",
    gtk_theme="Catppuccin-Mocha-Standard-Mauve-Dark",
    terminal_palette="catppuccin-mocha",
    motion_preset="denial",
    notes=[
        "柔和的摩卡低对比度护眼暗色，全终端调色板与 Starship 深度匹配。",
    ],
)

# --- 4. Catppuccin Latte 浅色奶油 ---
CATPPUCCIN_LATTE_RICE = RicePreset(
    name="Catppuccin Latte",
    description="温馨明亮的奶油拿铁浅色风格",
    is_dark=False,
    global_theme="Catppuccin-Latte-Mauve",
    color_scheme="CatppuccinLatteMauve",
    plasma_style="Catppuccin-Latte-Mauve",
    widget_style="Breeze",
    kvantum_theme="Catppuccin-Latte-Mauve",
    window_decoration_lib="org.kde.breeze",
    cursor_theme="Catppuccin-Latte-Mauve-Cursors",
    cursor_size=24,
    icon_theme="Papirus-Light",
    gtk_theme="Catppuccin-Latte-Standard-Mauve-Light",
    terminal_palette="catppuccin-latte",
    motion_preset="denial",
    notes=[
        "优雅淡雅的暖白浅色风格，搭配精致粉彩 Accent 强调色。",
    ],
)

# --- 5. Tokyo Night 霓虹赛博暗色 ---
TOKYO_NIGHT_RICE = RicePreset(
    name="Tokyo Night",
    description="东京之夜赛博霓虹暗色风格，经典深蓝底色与荧光青强调色",
    is_dark=True,
    global_theme="Tokyo-Night",
    color_scheme="TokyoNight",
    plasma_style="Tokyo-Night",
    widget_style="Breeze",
    kvantum_theme="Tokyo-Night",
    window_decoration_lib="org.kde.breeze",
    cursor_theme="Vimix-cursors",
    cursor_size=24,
    icon_theme="Tela-circle-blue",
    gtk_theme="Tokyo-Night",
    terminal_palette="tokyo-night",
    motion_preset="denial",
    notes=[
        "经典 Tokyo Night 霓虹蓝青调色板，全生态终端无缝热重载。",
    ],
)

# --- 6. Dracula 经典暗紫 ---
DRACULA_RICE = RicePreset(
    name="Dracula",
    description="经典吸血鬼德古拉暗夜紫与粉色高亮风格",
    is_dark=True,
    global_theme="Dracula",
    color_scheme="Dracula",
    plasma_style="Dracula",
    widget_style="Breeze",
    kvantum_theme="Dracula",
    window_decoration_lib="org.kde.breeze",
    cursor_theme="Dracula-cursors",
    cursor_size=24,
    icon_theme="Dracula",
    gtk_theme="Dracula",
    terminal_palette="dracula",
    motion_preset="denial",
    notes=[
        "高对比度冷峻紫色系风格，深受开发者喜爱。",
    ],
)

# --- 7. Gruvbox Dark 复古暖调暗色 ---
GRUVBOX_DARK_RICE = RicePreset(
    name="Gruvbox Dark",
    description="复古极简暖调暗色风格，温暖柔和不刺眼",
    is_dark=True,
    global_theme="Gruvbox-Dark",
    color_scheme="GruvboxDark",
    plasma_style="Gruvbox-Dark",
    widget_style="Breeze",
    kvantum_theme="Gruvbox-Dark",
    window_decoration_lib="org.kde.breeze",
    cursor_theme="Capitaine-cursors",
    cursor_size=24,
    icon_theme="Gruvbox-Plus-Dark",
    gtk_theme="Gruvbox-Dark",
    terminal_palette="gruvbox-dark",
    motion_preset="denial",
    notes=[
        "复古温润的暖调色彩，全链路命令行与终端提示符深度定制。",
    ],
)

# --- 8. Orchis Dark 极简暗色 ---
ORCHIS_DARK_RICE = RicePreset(
    name="Orchis Material Dark",
    description="经典 Orchis Material Design 扁平暗色风格",
    is_dark=True,
    global_theme="com.github.vinceliuice.Orchis-dark",
    color_scheme="OrchisDark",
    plasma_style="Orchis-dark",
    widget_style="Breeze",
    kvantum_theme="Orchis-dark",
    window_decoration_lib="org.kde.breeze",
    cursor_theme="Vimix-cursors",
    cursor_size=24,
    icon_theme="Tela-circle-dark",
    gtk_theme="Orchis-Dark",
    terminal_palette="orchis-dark",
    motion_preset="denial",
    notes=[
        "经典 Orchis 材质美学，轻快灵动。",
    ],
)

# --- 9. Orchis Light 极简浅色 ---
ORCHIS_LIGHT_RICE = RicePreset(
    name="Orchis Material Light",
    description="纯净明亮的 Orchis Material Design 浅白风格",
    is_dark=False,
    global_theme="com.github.vinceliuice.Orchis",
    color_scheme="Orchis",
    plasma_style="Orchis",
    widget_style="Breeze",
    kvantum_theme="Default",
    window_decoration_lib="org.kde.breeze",
    cursor_theme="Vimix-cursors",
    cursor_size=24,
    icon_theme="Tela-circle",
    gtk_theme="Orchis-Light",
    terminal_palette="orchis-light",
    motion_preset="denial",
    notes=[
        "明亮纯净的浅色材质设计风格。",
    ],
)

RICE_PRESETS: dict[str, RicePreset] = {
    "cachy-nord": CACHY_NORD_RICE,
    "cyan-mint-light": CYAN_MINT_LIGHT_RICE,
    "cyan-light": CYAN_MINT_LIGHT_RICE,
    "catppuccin-mocha": CATPPUCCIN_MOCHA_RICE,
    "catppuccin-latte": CATPPUCCIN_LATTE_RICE,
    "tokyo-night": TOKYO_NIGHT_RICE,
    "dracula": DRACULA_RICE,
    "gruvbox-dark": GRUVBOX_DARK_RICE,
    "orchis-dark": ORCHIS_DARK_RICE,
    "orchis-light": ORCHIS_LIGHT_RICE,
}
