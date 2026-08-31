"""Unified Desktop Rice (Visual Theme + Motion) Presets."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RicePreset:
    name: str
    description: str
    global_theme: Optional[str] = None
    color_scheme: Optional[str] = None
    cursor_theme: Optional[str] = None
    icon_theme: Optional[str] = None
    window_decoration_lib: Optional[str] = None
    window_decoration_theme: Optional[str] = None
    motion_preset: str = "denial"
    notes: list[str] = None

    def __post_init__(self):
        if self.notes is None:
            self.notes = []


# Orchis Light (Material Design Semi-Light Aesthetic + Rounded Window Deco)
ORCHIS_LIGHT_RICE = RicePreset(
    name="orchis-light",
    description="Vinceliuice's Orchis Material Design semi-light theme (soft rounded tabs, teal accents & Denial motion)",
    global_theme="com.github.vinceliuice.Orchis",
    color_scheme="Orchis",
    cursor_theme="WhiteSur-cursors",
    icon_theme="Fluent",
    window_decoration_lib="org.kde.kwin.aurorae.v2",
    window_decoration_theme="__aurorae__svg__Orchis",
    motion_preset="denial",
    notes=[
        "Material Design 3 aesthetic with pill-shaped rounded window controls.",
        "Soft off-white canvas with elegant teal/cyan accent hues.",
        "Denial fluid scale animation on window open/close.",
    ],
)

# Orchis Dark (Material Design Dark Aesthetic)
ORCHIS_DARK_RICE = RicePreset(
    name="orchis-dark",
    description="Vinceliuice's Orchis Material Design dark theme (deep slate, rounded controls & Denial motion)",
    global_theme="com.github.vinceliuice.Orchis-dark",
    color_scheme="OrchisDark",
    cursor_theme="WhiteSur-cursors",
    icon_theme="Fluent",
    window_decoration_lib="org.kde.kwin.aurorae.v2",
    window_decoration_theme="__aurorae__svg__Orchis-dark",
    motion_preset="denial",
    notes=[
        "Deep slate material dark palette with rounded aurorae titlebars.",
    ],
)

# CachyOS Nord Lightly (Semi-Light Arctic Daylight, Eye-friendly off-white)
NORD_LIGHTLY_RICE = RicePreset(
    name="nord-lightly",
    description="Soft semi-light arctic palette (Snow-Storm off-white with frost cyan accents & Denial motion)",
    global_theme="CachyOS-Nord",
    color_scheme="CachyOSNordLightly",
    cursor_theme="WhiteSur-cursors",
    icon_theme="Fluent",
    window_decoration_lib="org.kde.breeze",
    motion_preset="denial",
    notes=[
        "Soft off-white/slate window canvas (#ECEFF4) avoiding stark blinding white.",
        "Deep charcoal text (#2E3440) for high legibility with zero eye strain.",
    ],
)

# Edna Clean Light
EDNA_LIGHT_RICE = RicePreset(
    name="edna-light",
    description="Clean, high-legibility minimalist soft daylight aesthetic with Denial fluid scale",
    global_theme="Edna-Light",
    color_scheme="EdnaLight",
    cursor_theme="WhiteSur-cursors",
    icon_theme="Fluent",
    window_decoration_lib="org.kde.kwin.aurorae.v2",
    window_decoration_theme="__aurorae__svg__Edna-Light",
    motion_preset="denial",
    notes=[
        "Bright modern daylight workspace style with fluid spring momentum.",
    ],
)

# Breeze Twilight Clean Hybrid (Dark dock + Light window canvas)
BREEZE_TWILIGHT_RICE = RicePreset(
    name="breeze-twilight",
    description="Hybrid twilight style: dark panel & launcher with eye-friendly light window canvas",
    global_theme="org.kde.breezetwilight.desktop",
    color_scheme="CachyOSNordLightly",
    cursor_theme="WhiteSur-cursors",
    icon_theme="Fluent",
    window_decoration_lib="org.kde.breeze",
    motion_preset="denial",
    notes=[
        "Balanced dual-tone layout with dark taskbar and soft light content windows.",
    ],
)

# CachyOS Nord Dark (Original Dark)
CACHY_NORD_RICE = RicePreset(
    name="cachy-nord",
    description="CachyOS signature Nord dark palette paired with Denial fluid scale animations",
    global_theme="CachyOS-Nord",
    color_scheme="CachyOSNord",
    cursor_theme="breeze_cursors",
    icon_theme="char-white",
    window_decoration_lib="org.kde.breeze",
    motion_preset="denial",
    notes=[
        "Nordic arctic blue hues with deep dark slate background.",
    ],
)

RICE_PRESETS: dict[str, RicePreset] = {
    "orchis-light": ORCHIS_LIGHT_RICE,
    "orchis-dark": ORCHIS_DARK_RICE,
    "nord-lightly": NORD_LIGHTLY_RICE,
    "edna-light": EDNA_LIGHT_RICE,
    "breeze-twilight": BREEZE_TWILIGHT_RICE,
    "cachy-nord": CACHY_NORD_RICE,
}
