"""根据调色板动态生成 Shell 提示符 (Starship) 与系统硬件信息看板 (Fastfetch) 配置模板。"""

from __future__ import annotations

import json
from krice.presets.terminal_palettes import TerminalPalette


from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LanguageCapsuleSpec:
    """软件 / 编程语言胶囊配置元数据。"""
    module: str
    symbol: str
    brand_color: str
    icon_fg: str = "#FFFFFF"
    light_bg: Optional[str] = None
    light_fg: Optional[str] = None
    var_template: str = "$version"


# 官方品牌原生配色注册表 (Brand-Authentic Capsule Registry)
SOFTWARE_CAPSULES: list[LanguageCapsuleSpec] = [
    LanguageCapsuleSpec("c", "", "#00599C", light_bg="#E6F0FA", light_fg="#004B87", var_template="$name($version)"),
    LanguageCapsuleSpec("rust", "", "#F74C00", light_bg="#FFECE6", light_fg="#C43A00"),
    LanguageCapsuleSpec("golang", "", "#00ADD8", light_bg="#E0F7FA", light_fg="#007D9C"),
    LanguageCapsuleSpec("python", "", "#3776AB", icon_fg="#FFD43B", light_bg="#E8F2FA", light_fg="#205C90"),
    LanguageCapsuleSpec("nodejs", "", "#5FA04E", light_bg="#F0FDF4", light_fg="#2E6E1F"),
    LanguageCapsuleSpec("bun", "", "#FBF0DF", icon_fg="#333333", light_bg="#FDF6EC", light_fg="#D97706"),
    LanguageCapsuleSpec("deno", "🦕", "#000000", light_bg="#F3F4F6", light_fg="#111827"),
    LanguageCapsuleSpec("java", "", "#ED8B00", light_bg="#FFF3E0", light_fg="#C44800"),
    LanguageCapsuleSpec("kotlin", "", "#7F52FF", light_bg="#F3E8FF", light_fg="#6B21A8"),
    LanguageCapsuleSpec("zig", "", "#F7A41D", light_bg="#FFF8E8", light_fg="#B86F00"),
    LanguageCapsuleSpec("lua", "", "#000080", light_bg="#E8EAF6", light_fg="#000080"),
    LanguageCapsuleSpec("php", "", "#777BB4", light_bg="#F0F1F9", light_fg="#5A5E96"),
    LanguageCapsuleSpec("ruby", "", "#CC342D", light_bg="#FDE8E8", light_fg="#A61C16"),
    LanguageCapsuleSpec("dart", "", "#0175C2", light_bg="#E1F5FE", light_fg="#0277BD"),
    LanguageCapsuleSpec("elixir", "", "#4B275F", light_bg="#F3E5F5", light_fg="#4A148C"),
    LanguageCapsuleSpec("docker_context", "", "#2496ED", light_bg="#E8F4FD", light_fg="#0D6EFD", var_template="$context"),
]


def generate_starship_config(palette: TerminalPalette) -> str:
    """生成匹配调色板的模块化对称独立胶囊 (Modular Floating Pills) starship.toml 配置文件。"""
    bg_dir = "#FFFFFF" if not palette.is_dark else palette.selection_bg
    fg_dir = palette.foreground
    accent_blue = palette.blue
    accent_cyan = palette.cyan
    accent_yellow = palette.yellow
    accent_red = palette.red
    bg_git = palette.selection_bg

    # 自动生成所有注册语言/软件的 format 变量流
    module_formats = "\n".join(f"${spec.module}\\" for spec in SOFTWARE_CAPSULES)

    # 自动渲染各个软件专属的自适应独立胶囊模块
    module_sections: list[str] = []
    for spec in SOFTWARE_CAPSULES:
        ver_bg = palette.selection_bg if palette.is_dark else (spec.light_bg or "#F1F5F9")
        ver_fg = (spec.icon_fg if spec.icon_fg != "#FFFFFF" else spec.brand_color) if palette.is_dark else (spec.light_fg or spec.brand_color)
        icon_fg = spec.brand_color

        section = f"""[{spec.module}]
symbol = "{spec.symbol}"
style = "fg:{ver_fg} bg:{ver_bg} bold"
format = "[]({ver_bg})[ {spec.symbol} ](fg:{icon_fg} bg:{ver_bg})[{spec.var_template} ]($style)[ ](fg:{ver_bg})"
"""
        module_sections.append(section)

    rendered_modules = "\n".join(module_sections)

    return f"""# Starship 提示符 - 模块化对称独立胶囊群，由 krice 自动生成: {palette.display_name}

format = \"\"\"
$directory\\
$git_branch\\
$git_status\\
{module_formats}
$cmd_duration\\
$character
\"\"\"

command_timeout = 800

[directory]
style = "fg:{fg_dir} bg:{bg_dir} bold"
format = "[]({bg_dir})[  ](fg:{accent_cyan if palette.is_dark else accent_blue} bg:{bg_dir})[$path ]($style)[ ](fg:{bg_dir})"
truncation_length = 3
truncation_symbol = "…/"

[git_branch]
symbol = ""
style = "fg:{accent_blue} bg:{bg_git} bold"
format = "[]({bg_git})[ $symbol ](fg:{accent_blue} bg:{bg_git})[$branch]($style)"

[git_status]
style = "fg:{accent_yellow} bg:{bg_git}"
format = "[ $all_status$ahead_behind ]($style)[ ](fg:{bg_git})"

{rendered_modules}
[cmd_duration]
min_time = 500
style = "fg:#334155 bg:#E2E8F0 bold"
format = "[](#E2E8F0)[ ⏱ ](fg:#64748B bg:#E2E8F0)[$duration ]($style)[ ](fg:#E2E8F0)"

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
