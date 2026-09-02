"""根据调色板动态生成 Shell 提示符 (Starship) 与系统硬件信息看板 (Fastfetch) 配置模板。"""

from __future__ import annotations

import json
from krice.presets.terminal_palettes import TerminalPalette


def generate_starship_config(palette: TerminalPalette) -> str:
    """生成匹配调色板的现代圆角药丸胶囊风格 starship.toml 配置文件。"""
    bg_pill_1 = palette.cyan if palette.is_dark else palette.blue
    fg_pill_1 = palette.background if palette.is_dark else palette.foreground
    bg_pill_2 = palette.selection_bg
    fg_pill_2 = palette.foreground
    accent_blue = palette.blue
    accent_green = palette.green
    accent_yellow = palette.yellow
    accent_magenta = palette.magenta
    accent_red = palette.red

    return f"""# Starship 提示符 - 由 krice 自动生成，匹配调色板: {palette.display_name}

format = \"\"\"
[]({bg_pill_1})\\
[  ](bg:{bg_pill_1} fg:{fg_pill_1})\\
[](bg:{bg_pill_2} fg:{bg_pill_1})\\
$directory\\
[](fg:{bg_pill_2} bg:{palette.selection_bg})\\
$git_branch\\
$git_status\\
[](fg:{palette.selection_bg} bg:{bg_pill_2})\\
$rust\\
$golang\\
$python\\
$nodejs\\
[](fg:{bg_pill_2} bg:{palette.selection_bg})\\
$cmd_duration\\
[ ](fg:{palette.selection_bg})\\
$character
\"\"\"

command_timeout = 800

[directory]
style = "fg:{fg_pill_2} bg:{bg_pill_2} bold"
format = "[ $path ]($style)"
truncation_length = 3
truncation_symbol = "…/"

[git_branch]
symbol = ""
style = "fg:{accent_blue} bg:{palette.selection_bg} bold"
format = "[ $symbol $branch ]($style)"

[git_status]
style = "fg:{accent_yellow} bg:{palette.selection_bg}"
format = "[$all_status$ahead_behind ]($style)"

[rust]
symbol = ""
style = "fg:{accent_red} bg:{bg_pill_2} bold"
format = "[ $symbol ($version) ]($style)"

[golang]
symbol = ""
style = "fg:{accent_blue} bg:{bg_pill_2} bold"
format = "[ $symbol ($version) ]($style)"

[python]
symbol = ""
style = "fg:{accent_green} bg:{bg_pill_2} bold"
format = "[ $symbol ($version) ]($style)"

[nodejs]
symbol = ""
style = "fg:{accent_green} bg:{bg_pill_2} bold"
format = "[ $symbol ($version) ]($style)"

[cmd_duration]
min_time = 500
style = "fg:{accent_blue} bg:{palette.background}"
format = "[ ⏱ $duration ]($style)"

[character]
success_symbol = "[❯](bold {accent_blue})"
error_symbol = "[❯](bold {accent_red})"
"""


def generate_fastfetch_config(palette: TerminalPalette) -> str:
    """生成匹配调色板色彩的极简美观 Fastfetch config.jsonc 配置文件。"""
    key_color = "cyan" if palette.is_dark else "blue"
    title_color = "blue" if palette.is_dark else "cyan"

    config = {
        "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
        "logo": {
            "type": "small",
            "padding": {
                "top": 1,
                "left": 2,
                "right": 3,
            },
        },
        "display": {
            "separator": " 󰄾 ",
            "color": {
                "keys": key_color,
                "title": title_color,
            },
        },
        "modules": [
            "title",
            "separator",
            {
                "type": "os",
                "key": "OS",
                "format": "{3} {12}",
            },
            {
                "type": "host",
                "key": "Host",
            },
            {
                "type": "kernel",
                "key": "Kernel",
            },
            {
                "type": "uptime",
                "key": "Uptime",
            },
            {
                "type": "wm",
                "key": "WM",
                "format": "{2} ({3})",
            },
            {
                "type": "theme",
                "key": "Theme",
            },
            {
                "type": "icons",
                "key": "Icons",
            },
            {
                "type": "terminal",
                "key": "Term",
            },
            {
                "type": "terminalfont",
                "key": "Font",
            },
            {
                "type": "cpu",
                "key": "CPU",
            },
            {
                "type": "gpu",
                "key": "GPU",
            },
            {
                "type": "memory",
                "key": "Memory",
            },
            "break",
            "colors",
        ],
    }
    return json.dumps(config, indent=2) + "\n"
