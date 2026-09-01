"""Unified Desktop Rice (Visual Theme + Terminal + Motion) Presets."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RicePreset:
    """Complete unified desktop aesthetic preset encompassing KDE theme, terminal theme, and motion physics."""

    name: str
    description: str
    global_theme: Optional[str] = None
    color_scheme: Optional[str] = None
    cursor_theme: Optional[str] = None
    cursor_size: Optional[int] = 24
    icon_theme: Optional[str] = None
    plasma_style: Optional[str] = None
    widget_style: Optional[str] = None
    kvantum_theme: Optional[str] = None
    window_decoration_lib: Optional[str] = None
    window_decoration_theme: Optional[str] = None
    terminal_palette: Optional[str] = None
    gtk_theme: Optional[str] = None
    is_dark: bool = True
    motion_preset: str = "denial"
    notes: list[str] = field(default_factory=list)


# --- 1. CachyOS Nord Dark (Arctic Dark Aesthetic) ---
CACHY_NORD_RICE = RicePreset(
    name="cachy-nord",
    description="CachyOS Nordic Arctic Dark (Deep blue-gray palette, Nordic icons, Denial fluid scale & Nord terminal sync)",
    global_theme="Nordic",
    color_scheme="CachyOSNord",
    cursor_theme="Nordzy-cursors",
    cursor_size=24,
    icon_theme="Nordic-Darker",
    plasma_style="Nordic",
    widget_style="kvantum",
    kvantum_theme="Nordic",
    window_decoration_lib="klassy",
    window_decoration_theme="Nordic",
    terminal_palette="cachy-nord",
    gtk_theme="Nordic",
    is_dark=True,
    motion_preset="denial",
    notes=[
        "Matches KDE Arctic Dark palette with synchronized Nord Alacritty/Kitty/Konsole/Ghostty.",
        "Generates custom Starship Nord pill prompt & Fastfetch cyber-cyan logo display.",
        "Fluid DenialWM 65% -> 100% window scale with background blur.",
    ],
)

# --- 2. Nord Lightly / Snow Storm (Semi-Light Arctic Daylight) ---
NORD_LIGHTLY_RICE = RicePreset(
    name="nord-lightly",
    description="Nord Snow Storm Semi-Light (Eye-friendly off-white canvas, crisp frost accents, Glide motion & Light terminal sync)",
    global_theme="Nordic-Polar",
    color_scheme="NordSnowStorm",
    cursor_theme="Nordzy-cursors-white",
    cursor_size=24,
    icon_theme="Nordic-Folders",
    plasma_style="default",
    widget_style="Breeze",
    window_decoration_lib="org.kde.breeze",
    terminal_palette="nord-light",
    gtk_theme="Nordic-Polar",
    is_dark=False,
    motion_preset="glide",
    notes=[
        "Comfortable daylight aesthetic without harsh pure-white glare (#ECEFF4 background).",
        "Glide sheet motion (smooth angle tilt) with matching light terminal palette.",
    ],
)

# --- 3. Catppuccin Mocha (Modern Soothing Dark Pastel) ---
CATPPUCCIN_MOCHA_RICE = RicePreset(
    name="catppuccin-mocha",
    description="Catppuccin Mocha (Soothing dark pastel, Lavender/Mauve accents, Denial fluid motion & Catppuccin terminal)",
    global_theme="Catppuccin-Mocha-Mauve",
    color_scheme="CatppuccinMochaMauve",
    cursor_theme="Catppuccin-Mocha-Mauve-Cursors",
    cursor_size=24,
    icon_theme="Papirus-Dark",
    plasma_style="Catppuccin-Mocha",
    widget_style="kvantum",
    kvantum_theme="Catppuccin-Mocha-Mauve",
    window_decoration_lib="klassy",
    terminal_palette="catppuccin-mocha",
    gtk_theme="Catppuccin-Mocha-Standard-Mauve-Dark",
    is_dark=True,
    motion_preset="denial",
    notes=[
        "Modern developer aesthetic with soft pastel highlights.",
        "Deep contrast with #1E1E2E canvas and vibrant Lavender/Peach accents.",
    ],
)

# --- 4. Catppuccin Latte (Clean Soft Pastel Light) ---
CATPPUCCIN_LATTE_RICE = RicePreset(
    name="catppuccin-latte",
    description="Catppuccin Latte (Soft warm pastel light, Rosewater highlights, Glide motion & Latte terminal)",
    global_theme="Catppuccin-Latte-Rosewater",
    color_scheme="CatppuccinLatteRosewater",
    cursor_theme="Catppuccin-Latte-Rosewater-Cursors",
    cursor_size=24,
    icon_theme="Papirus-Light",
    plasma_style="default",
    widget_style="Breeze",
    window_decoration_lib="org.kde.breeze",
    terminal_palette="catppuccin-latte",
    gtk_theme="Catppuccin-Latte-Standard-Rosewater-Light",
    is_dark=False,
    motion_preset="glide",
    notes=[
        "Clean, gentle light mode with pleasant warmth (#EFF1F5).",
    ],
)

# --- 5. Tokyo Night (Neon Cyber Dark) ---
TOKYO_NIGHT_RICE = RicePreset(
    name="tokyo-night",
    description="Tokyo Night Storm (Neon cyberpunk dark, electric blue/magenta highlights & Denial Vivid deep zoom motion)",
    global_theme="Tokyo-Night",
    color_scheme="TokyoNightStorm",
    cursor_theme="Bibata-Modern-Ice",
    cursor_size=24,
    icon_theme="Tela-circle-dark",
    plasma_style="Tokyo-Night",
    widget_style="kvantum",
    kvantum_theme="Tokyo-Night",
    window_decoration_lib="klassy",
    terminal_palette="tokyo-night",
    gtk_theme="Tokyo-Night",
    is_dark=True,
    motion_preset="denial-vivid",
    notes=[
        "High-contrast neon dark theme with deep 50% -> 100% Denial Vivid zoom.",
    ],
)

# --- 6. Dracula (Classic Vampire Dark Purple) ---
DRACULA_RICE = RicePreset(
    name="dracula",
    description="Dracula (Gothic dark purple canvas, electric pink/cyan accents, Snappy fast response & Dracula terminal)",
    global_theme="Dracula",
    color_scheme="Dracula",
    cursor_theme="Dracula-cursors",
    cursor_size=24,
    icon_theme="Dracula",
    plasma_style="Dracula",
    widget_style="kvantum",
    kvantum_theme="Dracula",
    window_decoration_lib="org.kde.breeze",
    terminal_palette="dracula",
    gtk_theme="Dracula",
    is_dark=True,
    motion_preset="snappy",
    notes=[
        "Iconic dark purple palette with ultra-fast 120Hz/240Hz Snappy window animations.",
    ],
)

# --- 7. Gruvbox Dark (Warm Retro Groove) ---
GRUVBOX_DARK_RICE = RicePreset(
    name="gruvbox-dark",
    description="Gruvbox Dark (Warm retro groove, golden yellow/orange highlights, Spring-Wobbly bouncy physics)",
    global_theme="Gruvbox-Dark",
    color_scheme="GruvboxDark",
    cursor_theme="Capitaine-Cursors-Gruvbox",
    cursor_size=24,
    icon_theme="Gruvbox-Plus-Dark",
    plasma_style="Gruvbox-Dark",
    widget_style="kvantum",
    kvantum_theme="Gruvbox-Dark",
    window_decoration_lib="klassy",
    terminal_palette="gruvbox-dark",
    gtk_theme="Gruvbox-Dark",
    is_dark=True,
    motion_preset="spring-wobbly",
    notes=[
        "Tactile organic bouncy spring window physics with cozy warm retro colors.",
    ],
)

# --- 8. Gruvbox Light (Warm Cream Retro) ---
GRUVBOX_LIGHT_RICE = RicePreset(
    name="gruvbox-light",
    description="Gruvbox Light (Comfortable parchment/cream aesthetic, warm terracotta accents, Glide motion)",
    global_theme="Gruvbox-Light",
    color_scheme="GruvboxLight",
    cursor_theme="Capitaine-Cursors",
    cursor_size=24,
    icon_theme="Gruvbox-Plus-Light",
    plasma_style="default",
    widget_style="Breeze",
    window_decoration_lib="org.kde.breeze",
    terminal_palette="gruvbox-light",
    gtk_theme="Gruvbox-Light",
    is_dark=False,
    motion_preset="glide",
    notes=[
        "Warm paper/parchment background (#FBF1C7) with retro typography and Glide sheet animations.",
    ],
)

# --- 9. Rosé Pine (SoHo Vibes Dark Aesthetic) ---
ROSE_PINE_RICE = RicePreset(
    name="rose-pine",
    description="Rosé Pine (All-natural SoHo vibes, subtle muted dark palette, pine green/rose accents & Denial motion)",
    global_theme="Rose-Pine",
    color_scheme="RosePine",
    cursor_theme="Breeze_Dark",
    cursor_size=24,
    icon_theme="Papirus-Dark",
    plasma_style="default",
    widget_style="Breeze",
    window_decoration_lib="org.kde.breeze",
    terminal_palette="rose-pine",
    gtk_theme="Rose-Pine",
    is_dark=True,
    motion_preset="denial",
    notes=[
        "Elegantly muted, non-fatiguing dark theme with matching prompt & terminal.",
    ],
)

# --- 10. Orchis Dark (Material Design Modern Dark) ---
ORCHIS_DARK_RICE = RicePreset(
    name="orchis-dark",
    description="Orchis Dark (Material Design dark canvas, vibrant blue highlights, Klassy rounded titlebars & Denial motion)",
    global_theme="Orchis-dark",
    color_scheme="OrchisDark",
    cursor_theme="Vimix-cursors",
    cursor_size=24,
    icon_theme="Tela-dark",
    plasma_style="Orchis-dark",
    widget_style="kvantum",
    kvantum_theme="Orchis-dark",
    window_decoration_lib="klassy",
    terminal_palette="orchis-dark",
    gtk_theme="Orchis-Dark",
    is_dark=True,
    motion_preset="denial",
    notes=[
        "Combines smooth Material rounded corners with Denial fluid acceleration.",
    ],
)

# --- 11. Orchis Light (Material Design Clean Light) ---
ORCHIS_LIGHT_RICE = RicePreset(
    name="orchis-light",
    description="Orchis Light (Material Design clean white/gray canvas, subtle shadows & Glide smooth tilt motion)",
    global_theme="Orchis-light",
    color_scheme="OrchisLight",
    cursor_theme="Vimix-white-cursors",
    cursor_size=24,
    icon_theme="Tela-light",
    plasma_style="default",
    widget_style="kvantum",
    kvantum_theme="Orchis-light",
    window_decoration_lib="klassy",
    terminal_palette="orchis-light",
    gtk_theme="Orchis-Light",
    is_dark=False,
    motion_preset="glide",
    notes=[
        "Crisp Material Design aesthetic with modern semi-light terminal sync.",
    ],
)

# --- 12. Breeze Twilight Clean Hybrid ---
BREEZE_TWILIGHT_RICE = RicePreset(
    name="breeze-twilight",
    description="Breeze Twilight Hybrid (Dark panel/dock + Light window canvas, native KDE Plasma 6 look & Glide motion)",
    global_theme="org.kde.breezetwilight.desktop",
    color_scheme="BreezeLight",
    cursor_theme="breeze_cursors",
    cursor_size=24,
    icon_theme="breeze",
    plasma_style="default",
    widget_style="Breeze",
    window_decoration_lib="org.kde.breeze",
    terminal_palette="nord-light",
    gtk_theme="Breeze",
    is_dark=False,
    motion_preset="glide",
    notes=[
        "Official KDE 6 hybrid aesthetic: dark launcher & system tray with light document area.",
    ],
)

# --- 13. Deep Emerald Dark ---
EMERALD_DARK_RICE = RicePreset(
    name="emerald-dark",
    description="Emerald Dark (Deep forest dark green, mint highlights, fluid Denial scaling & Emerald terminal sync)",
    global_theme="Emerald-Dark",
    color_scheme="EmeraldDark",
    cursor_theme="Breeze_Dark",
    cursor_size=24,
    icon_theme="Papirus-Dark",
    plasma_style="default",
    widget_style="Breeze",
    window_decoration_lib="org.kde.breeze",
    terminal_palette="emerald-dark",
    gtk_theme="Breeze-Dark",
    is_dark=True,
    motion_preset="denial",
    notes=[
        "Deep calming green atmosphere with matching terminal & Starship prompt.",
    ],
)

# --- 14. One Dark (Developer Pro Dark) ---
ONE_DARK_RICE = RicePreset(
    name="one-dark",
    description="One Dark (Atom / Pro Developer dark palette, Snappy ultra-responsive animations & One-Dark terminal)",
    global_theme="One-Dark",
    color_scheme="OneDark",
    cursor_theme="Breeze_Dark",
    cursor_size=24,
    icon_theme="Papirus-Dark",
    plasma_style="default",
    widget_style="Breeze",
    window_decoration_lib="org.kde.breeze",
    terminal_palette="one-dark",
    gtk_theme="Breeze-Dark",
    is_dark=True,
    motion_preset="snappy",
    notes=[
        "Balanced coding dark theme with instant responsive Snappy motion.",
    ],
)

RICE_PRESETS: dict[str, RicePreset] = {
    "cachy-nord": CACHY_NORD_RICE,
    "nord-lightly": NORD_LIGHTLY_RICE,
    "catppuccin-mocha": CATPPUCCIN_MOCHA_RICE,
    "catppuccin-latte": CATPPUCCIN_LATTE_RICE,
    "tokyo-night": TOKYO_NIGHT_RICE,
    "dracula": DRACULA_RICE,
    "gruvbox-dark": GRUVBOX_DARK_RICE,
    "gruvbox-light": GRUVBOX_LIGHT_RICE,
    "rose-pine": ROSE_PINE_RICE,
    "orchis-dark": ORCHIS_DARK_RICE,
    "orchis-light": ORCHIS_LIGHT_RICE,
    "breeze-twilight": BREEZE_TWILIGHT_RICE,
    "emerald-dark": EMERALD_DARK_RICE,
    "one-dark": ONE_DARK_RICE,
}
