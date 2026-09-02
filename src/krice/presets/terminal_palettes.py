"""Built-in high-quality terminal color palettes for krice."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class TerminalPalette:
    """Represents a 16-color ANSI terminal color palette plus UI/cursor/selection colors."""

    name: str
    display_name: str
    background: str
    foreground: str
    dim_foreground: str = ""
    bright_foreground: str = ""
    cursor: str = ""
    cursor_text: str = ""
    selection_bg: str = ""
    selection_fg: str = ""

    # Normal ANSI colors (0-7)
    black: str = "#000000"
    red: str = "#ff0000"
    green: str = "#00ff00"
    yellow: str = "#ffff00"
    blue: str = "#0000ff"
    magenta: str = "#ff00ff"
    cyan: str = "#00ffff"
    white: str = "#ffffff"

    # Bright ANSI colors (8-15)
    bright_black: str = "#555555"
    bright_red: str = "#ff5555"
    bright_green: str = "#55ff55"
    bright_yellow: str = "#ffff55"
    bright_blue: str = "#5555ff"
    bright_magenta: str = "#ff55ff"
    bright_cyan: str = "#55ffff"
    bright_white: str = "#ffffff"

    is_dark: bool = True

    def __post_init__(self) -> None:
        if not self.dim_foreground:
            self.dim_foreground = self.bright_black
        if not self.bright_foreground:
            self.bright_foreground = self.foreground
        if not self.cursor:
            self.cursor = self.cyan if self.is_dark else self.blue
        if not self.cursor_text:
            self.cursor_text = self.background
        if not self.selection_bg:
            self.selection_bg = self.bright_black if self.is_dark else self.bright_white
        if not self.selection_fg:
            self.selection_fg = self.foreground

    def to_ansi_list(self) -> list[str]:
        """Returns 16 ANSI colors in order (0 to 15)."""
        return [
            self.black,
            self.red,
            self.green,
            self.yellow,
            self.blue,
            self.magenta,
            self.cyan,
            self.white,
            self.bright_black,
            self.bright_red,
            self.bright_green,
            self.bright_yellow,
            self.bright_blue,
            self.bright_magenta,
            self.bright_cyan,
            self.bright_white,
        ]


# --- Built-in Palettes ---

CACHY_NORD = TerminalPalette(
    name="cachy-nord",
    display_name="CachyOS Nord (Arctic Dark - Enhanced Contrast)",
    background="#2E3440",
    foreground="#ECEFF4",
    dim_foreground="#7B88A1",
    bright_foreground="#FFFFFF",
    cursor="#88C0D0",
    cursor_text="#2E3440",
    selection_bg="#434C5E",
    selection_fg="#ECEFF4",
    black="#3B4252",
    red="#BF616A",
    green="#A3BE8C",
    yellow="#EBCB8B",
    blue="#81A1C1",
    magenta="#B48EAD",
    cyan="#88C0D0",
    white="#E5E9F0",
    bright_black="#7684A0",   # Enhanced high-contrast comments/disabled text (4.6:1 WCAG AA)
    bright_red="#D08770",
    bright_green="#A3D49C",
    bright_yellow="#F0D399",
    bright_blue="#88C0D0",
    bright_magenta="#C695C6",
    bright_cyan="#8FD5E6",
    bright_white="#FFFFFF",
    is_dark=True,
)

NORD_LIGHT = TerminalPalette(
    name="nord-light",
    display_name="Nord Snow Storm (Soft Daylight)",
    background="#F4F6F9",
    foreground="#242933",
    dim_foreground="#616E88",
    bright_foreground="#0F141C",
    cursor="#5E81AC",
    cursor_text="#F4F6F9",
    selection_bg="#D8DEE9",
    selection_fg="#242933",
    black="#2E3440",
    red="#C53030",
    green="#2F855A",
    yellow="#B7791F",
    blue="#2B6CB0",
    magenta="#744210",
    cyan="#0D9488",
    white="#E5E9F0",
    bright_black="#616E88",
    bright_red="#E53E3E",
    bright_green="#38A169",
    bright_yellow="#D69E2E",
    bright_blue="#3182CE",
    bright_magenta="#805AD5",
    bright_cyan="#00A3C4",
    bright_white="#FFFFFF",
    is_dark=False,
)

ORCHIS_LIGHT = TerminalPalette(
    name="orchis-light",
    display_name="Orchis Material Light (Elegant Clean)",
    background="#F8F9FA",
    foreground="#202124",
    dim_foreground="#5F6368",
    bright_foreground="#000000",
    cursor="#1A73E8",
    cursor_text="#FFFFFF",
    selection_bg="#D2E3FC",
    selection_fg="#174EA6",
    black="#3C4043",
    red="#D93025",
    green="#188038",
    yellow="#E37400",
    blue="#1A73E8",
    magenta="#A142F4",
    cyan="#12B5CB",
    white="#E8EAED",
    bright_black="#70757A",
    bright_red="#EA4335",
    bright_green="#34A853",
    bright_yellow="#FBBC04",
    bright_blue="#4285F4",
    bright_magenta="#AF5CF7",
    bright_cyan="#24C1E0",
    bright_white="#FFFFFF",
    is_dark=False,
)
CATPPUCCIN_MOCHA = TerminalPalette(
    name="catppuccin-mocha",
    display_name="Catppuccin Mocha (Soothing Dark)",
    background="#1E1E2E",
    foreground="#CDD6F4",
    dim_foreground="#6C7086",
    bright_foreground="#F5E0DC",
    cursor="#F5E0DC",
    cursor_text="#11111B",
    selection_bg="#45475A",
    selection_fg="#CDD6F4",
    black="#45475A",
    red="#F38BA8",
    green="#A6E3A1",
    yellow="#F9E2AF",
    blue="#89B4FA",
    magenta="#F5C2E7",
    cyan="#94E2D5",
    white="#BAC2DE",
    bright_black="#585B70",
    bright_red="#F38BA8",
    bright_green="#A6E3A1",
    bright_yellow="#F9E2AF",
    bright_blue="#89B4FA",
    bright_magenta="#CBA6F7",
    bright_cyan="#89DCEB",
    bright_white="#A6ADC8",
    is_dark=True,
)

CATPPUCCIN_LATTE = TerminalPalette(
    name="catppuccin-latte",
    display_name="Catppuccin Latte (Clean Light)",
    background="#EFF1F5",
    foreground="#4C4F69",
    dim_foreground="#9CA0B0",
    bright_foreground="#202134",
    cursor="#DC8A78",
    cursor_text="#EFF1F5",
    selection_bg="#CCD0DA",
    selection_fg="#4C4F69",
    black="#5C5F77",
    red="#D20F39",
    green="#40A02B",
    yellow="#DF8E1D",
    blue="#1E66F5",
    magenta="#EA76CB",
    cyan="#179299",
    white="#ACB0BE",
    bright_black="#6C6F85",
    bright_red="#D20F39",
    bright_green="#40A02B",
    bright_yellow="#DF8E1D",
    bright_blue="#1E66F5",
    bright_magenta="#8839EF",
    bright_cyan="#209FB5",
    bright_white="#BCC0CC",
    is_dark=False,
)

TOKYO_NIGHT = TerminalPalette(
    name="tokyo-night",
    display_name="Tokyo Night Storm (Neon Cyber Dark)",
    background="#1A1B26",
    foreground="#C0CAF5",
    dim_foreground="#565F89",
    bright_foreground="#C0CAF5",
    cursor="#C0CAF5",
    cursor_text="#1A1B26",
    selection_bg="#283457",
    selection_fg="#C0CAF5",
    black="#15161E",
    red="#F7768E",
    green="#9ECE6A",
    yellow="#E0AF68",
    blue="#7AA2F7",
    magenta="#BB9AF7",
    cyan="#7DCFFF",
    white="#A9B1D6",
    bright_black="#414868",
    bright_red="#F7768E",
    bright_green="#9ECE6A",
    bright_yellow="#E0AF68",
    bright_blue="#7AA2F7",
    bright_magenta="#BB9AF7",
    bright_cyan="#7DCFFF",
    bright_white="#C0CAF5",
    is_dark=True,
)

DRACULA = TerminalPalette(
    name="dracula",
    display_name="Dracula (Gothic Dark Purple)",
    background="#282A36",
    foreground="#F8F8F2",
    dim_foreground="#6272A4",
    bright_foreground="#FFFFFF",
    cursor="#F8F8F2",
    cursor_text="#282A36",
    selection_bg="#44475A",
    selection_fg="#F8F8F2",
    black="#21222C",
    red="#FF5555",
    green="#50FA7B",
    yellow="#F1FA8C",
    blue="#BD93F9",
    magenta="#FF79C6",
    cyan="#8BE9FD",
    white="#F8F8F2",
    bright_black="#6272A4",
    bright_red="#FF6E6E",
    bright_green="#69FF94",
    bright_yellow="#FFFFA5",
    bright_blue="#D6ACFF",
    bright_magenta="#FF92DF",
    bright_cyan="#A4FFFF",
    bright_white="#FFFFFF",
    is_dark=True,
)

GRUVBOX_DARK = TerminalPalette(
    name="gruvbox-dark",
    display_name="Gruvbox Dark (Warm Retro)",
    background="#282828",
    foreground="#EBDBB2",
    dim_foreground="#7C6F64",
    bright_foreground="#FBF1C7",
    cursor="#FE8019",
    cursor_text="#282828",
    selection_bg="#504945",
    selection_fg="#EBDBB2",
    black="#282828",
    red="#CC241D",
    green="#98971A",
    yellow="#D79921",
    blue="#458588",
    magenta="#B16286",
    cyan="#689D6A",
    white="#A89984",
    bright_black="#928374",
    bright_red="#FB4934",
    bright_green="#B8BB26",
    bright_yellow="#FABD2F",
    bright_blue="#83A598",
    bright_magenta="#D3869B",
    bright_cyan="#8EC07C",
    bright_white="#EBDBB2",
    is_dark=True,
)

GRUVBOX_LIGHT = TerminalPalette(
    name="gruvbox-light",
    display_name="Gruvbox Light (Warm Cream)",
    background="#FBF1C7",
    foreground="#3C3836",
    dim_foreground="#928374",
    bright_foreground="#282828",
    cursor="#AF3A03",
    cursor_text="#FBF1C7",
    selection_bg="#EBDBB2",
    selection_fg="#3C3836",
    black="#FBF1C7",
    red="#CC241D",
    green="#98971A",
    yellow="#D79921",
    blue="#458588",
    magenta="#B16286",
    cyan="#689D6A",
    white="#7C6F64",
    bright_black="#928374",
    bright_red="#9D0006",
    bright_green="#79740E",
    bright_yellow="#B57614",
    bright_blue="#076678",
    bright_magenta="#8F3F71",
    bright_cyan="#427B58",
    bright_white="#3C3836",
    is_dark=False,
)

ROSE_PINE = TerminalPalette(
    name="rose-pine",
    display_name="Rosé Pine (SoHo Vibes Dark)",
    background="#191724",
    foreground="#E0DEF4",
    dim_foreground="#6E6A86",
    bright_foreground="#E0DEF4",
    cursor="#EB6F92",
    cursor_text="#191724",
    selection_bg="#2A283E",
    selection_fg="#E0DEF4",
    black="#26233A",
    red="#EB6F92",
    green="#31748F",
    yellow="#F6C177",
    blue="#9CCFD8",
    magenta="#C4A7E7",
    cyan="#EBBCBA",
    white="#E0DEF4",
    bright_black="#6E6A86",
    bright_red="#EB6F92",
    bright_green="#31748F",
    bright_yellow="#F6C177",
    bright_blue="#9CCFD8",
    bright_magenta="#C4A7E7",
    bright_cyan="#EBBCBA",
    bright_white="#E0DEF4",
    is_dark=True,
)

ORCHIS_DARK = TerminalPalette(
    name="orchis-dark",
    display_name="Orchis Material Dark",
    background="#21242B",
    foreground="#DCDFE4",
    dim_foreground="#5C6370",
    bright_foreground="#FFFFFF",
    cursor="#3DAEE9",
    cursor_text="#21242B",
    selection_bg="#3E4451",
    selection_fg="#FFFFFF",
    black="#282C34",
    red="#E06C75",
    green="#98C379",
    yellow="#E5C07B",
    blue="#61AFEF",
    magenta="#C678DD",
    cyan="#56B6C2",
    white="#ABB2BF",
    bright_black="#5C6370",
    bright_red="#BE5046",
    bright_green="#98C379",
    bright_yellow="#D19A66",
    bright_blue="#61AFEF",
    bright_magenta="#C678DD",
    bright_cyan="#56B6C2",
    bright_white="#FFFFFF",
    is_dark=True,
)

ORCHIS_LIGHT = TerminalPalette(
    name="orchis-light",
    display_name="Orchis Material Light",
    background="#FAFAFA",
    foreground="#383A42",
    dim_foreground="#A0A1A7",
    bright_foreground="#202227",
    cursor="#3DAEE9",
    cursor_text="#FAFAFA",
    selection_bg="#E5E5E6",
    selection_fg="#383A42",
    black="#000000",
    red="#E45649",
    green="#50A14F",
    yellow="#C18401",
    blue="#4078F2",
    magenta="#A626A4",
    cyan="#0184BC",
    white="#A0A1A7",
    bright_black="#4F525E",
    bright_red="#E06C75",
    bright_green="#98C379",
    bright_yellow="#E5C07B",
    bright_blue="#61AFEF",
    bright_magenta="#C678DD",
    bright_cyan="#56B6C2",
    bright_white="#FFFFFF",
    is_dark=False,
)

EMERALD_DARK = TerminalPalette(
    name="emerald-dark",
    display_name="Deep Emerald Forest Dark",
    background="#1A2421",
    foreground="#D8E2DC",
    dim_foreground="#4A5852",
    bright_foreground="#F0F4F2",
    cursor="#2EC4B6",
    cursor_text="#1A2421",
    selection_bg="#2D3E39",
    selection_fg="#F0F4F2",
    black="#141C1A",
    red="#E76F51",
    green="#2A9D8F",
    yellow="#E9C46A",
    blue="#4EA8DE",
    magenta="#B5838D",
    cyan="#2EC4B6",
    white="#D8E2DC",
    bright_black="#4A5852",
    bright_red="#F4A261",
    bright_green="#52B788",
    bright_yellow="#F3C68F",
    bright_blue="#72EFDD",
    bright_magenta="#E5989B",
    bright_cyan="#56CFE1",
    bright_white="#FFFFFF",
    is_dark=True,
)

ONE_DARK = TerminalPalette(
    name="one-dark",
    display_name="One Dark (Atom / Pro Code)",
    background="#282C34",
    foreground="#ABB2BF",
    dim_foreground="#5C6370",
    bright_foreground="#FFFFFF",
    cursor="#528BFF",
    cursor_text="#282C34",
    selection_bg="#3E4451",
    selection_fg="#ABB2BF",
    black="#282C34",
    red="#E06C75",
    green="#98C379",
    yellow="#E5C07B",
    blue="#61AFEF",
    magenta="#C678DD",
    cyan="#56B6C2",
    white="#ABB2BF",
    bright_black="#5C6370",
    bright_red="#E06C75",
    bright_green="#98C379",
    bright_yellow="#E5C07B",
    bright_blue="#61AFEF",
    bright_magenta="#C678DD",
    bright_cyan="#56B6C2",
    bright_white="#FFFFFF",
    is_dark=True,
)

SOLARIZED_DARK = TerminalPalette(
    name="solarized-dark",
    display_name="Solarized Dark",
    background="#002B36",
    foreground="#839496",
    dim_foreground="#586E75",
    bright_foreground="#93A1A1",
    cursor="#268BD2",
    cursor_text="#002B36",
    selection_bg="#073642",
    selection_fg="#93A1A1",
    black="#073642",
    red="#DC322F",
    green="#859900",
    yellow="#B58900",
    blue="#268BD2",
    magenta="#D33682",
    cyan="#2AA198",
    white="#EEE8D5",
    bright_black="#586E75",
    bright_red="#CB4B16",
    bright_green="#586E75",
    bright_yellow="#657B83",
    bright_blue="#839496",
    bright_magenta="#6C71C4",
    bright_cyan="#93A1A1",
    bright_white="#FDF6E3",
    is_dark=True,
)

SOLARIZED_LIGHT = TerminalPalette(
    name="solarized-light",
    display_name="Solarized Light",
    background="#FDF6E3",
    foreground="#657B83",
    dim_foreground="#93A1A1",
    bright_foreground="#586E75",
    cursor="#268BD2",
    cursor_text="#FDF6E3",
    selection_bg="#EEE8D5",
    selection_fg="#586E75",
    black="#073642",
    red="#DC322F",
    green="#859900",
    yellow="#B58900",
    blue="#268BD2",
    magenta="#D33682",
    cyan="#2AA198",
    white="#EEE8D5",
    bright_black="#586E75",
    bright_red="#CB4B16",
    bright_green="#586E75",
    bright_yellow="#657B83",
    bright_blue="#839496",
    bright_magenta="#6C71C4",
    bright_cyan="#93A1A1",
    bright_white="#FDF6E3",
    is_dark=False,
)

TERMINAL_PALETTES: dict[str, TerminalPalette] = {
    "cachy-nord": CACHY_NORD,
    "nord-dark": CACHY_NORD,
    "nord-light": NORD_LIGHT,
    "catppuccin-mocha": CATPPUCCIN_MOCHA,
    "catppuccin-latte": CATPPUCCIN_LATTE,
    "tokyo-night": TOKYO_NIGHT,
    "dracula": DRACULA,
    "gruvbox-dark": GRUVBOX_DARK,
    "gruvbox-light": GRUVBOX_LIGHT,
    "rose-pine": ROSE_PINE,
    "orchis-dark": ORCHIS_DARK,
    "orchis-light": ORCHIS_LIGHT,
    "emerald-dark": EMERALD_DARK,
    "one-dark": ONE_DARK,
    "solarized-dark": SOLARIZED_DARK,
    "solarized-light": SOLARIZED_LIGHT,
}
