"""根据调色板动态生成 Shell 提示符 (Starship) 与系统硬件信息看板 (Fastfetch) 配置模板。"""

from __future__ import annotations

import json
from krice.presets.terminal_palettes import TerminalPalette


def generate_starship_config(palette: TerminalPalette) -> str:
    """生成匹配调色板的现代圆角药丸胶囊风格 starship.toml 配置文件。"""
    bg_pill_1 = palette.cyan if palette.is_dark else palette.blue
    fg_pill_1 = palette.background if palette.is_dark else "#FFFFFF"
    bg_pill_2 = palette.selection_bg if palette.is_dark else "#FFFFFF"
    fg_pill_2 = palette.foreground
    accent_blue = palette.blue
    accent_green = palette.green
    accent_yellow = palette.yellow
    accent_magenta = palette.magenta
    accent_red = palette.red
    return f"""# Starship 提示符 - 多阶色彩层次独立自闭合胶囊群，由 krice 自动生成: {palette.display_name}

format = \"\"\"
$directory\\
$git_branch\\
$git_status\\
$rust\\
$golang\\
$python\\
$nodejs\\
$cmd_duration\\
$character
\"\"\"

command_timeout = 800

[directory]
style = "fg:{fg_pill_2} bg:{bg_pill_2} bold"
format = "[]({bg_pill_1})[  ](bg:{bg_pill_1} fg:{fg_pill_1})[](bg:{bg_pill_2} fg:{bg_pill_1})[ $path ]($style)[ ](fg:{bg_pill_2})"
truncation_length = 3
truncation_symbol = "…/"

[git_branch]
symbol = ""
style = "fg:{accent_blue} bg:{palette.selection_bg} bold"
format = "[]({accent_blue})[ $symbol ](bg:{accent_blue} fg:{fg_pill_1})[](bg:{palette.selection_bg} fg:{accent_blue})[ $branch ]($style)"

[git_status]
style = "fg:{accent_yellow} bg:{palette.selection_bg}"
format = "[$all_status$ahead_behind ]($style)[ ](fg:{palette.selection_bg})"

[rust]
symbol = ""
style = "fg:{accent_red} bg:#FFE4E6 bold"
format = "[]({accent_red})[ $symbol ](bg:{accent_red} fg:{fg_pill_1})[](bg:#FFE4E6 fg:{accent_red})[ $version ]($style)[ ](fg:#FFE4E6)"

[golang]
symbol = ""
style = "fg:#0369A1 bg:#E0F2FE bold"
format = "[](#0369A1)[ $symbol ](bg:#0369A1 fg:{fg_pill_1})[](bg:#E0F2FE fg:#0369A1)[ $version ]($style)[ ](fg:#E0F2FE)"

[python]
symbol = ""
style = "fg:{accent_green} bg:#D1FAE5 bold"
format = "[]({accent_green})[ $symbol ](bg:{accent_green} fg:{fg_pill_1})[](bg:#D1FAE5 fg:{accent_green})[ $version ]($style)[ ](fg:#D1FAE5)"

[nodejs]
symbol = ""
style = "fg:#3F6212 bg:#ECFCCB bold"
format = "[](#4D7C0F)[ $symbol ](bg:#4D7C0F fg:{fg_pill_1})[](bg:#ECFCCB fg:#4D7C0F)[ $version ]($style)[ ](fg:#ECFCCB)"

[cmd_duration]
min_time = 500
style = "fg:#334155 bg:#E2E8F0 bold"
format = "[](#64748B)[ ⏱ ](bg:#64748B fg:{fg_pill_1})[](bg:#E2E8F0 fg:#64748B)[ $duration ]($style)[ ](fg:#E2E8F0)"

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
