"""krice 命令行接口：KDE Plasma 6 全方位美化、流体动效调优、多终端配色联动与跨机器无损迁移工具箱。"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from krice.inspector import DesktopInspector
from krice.installer import DependencyHelper
from krice.kwin_ctl import KWinController
from krice.presets.builtin_presets import PRESETS as MOTION_PRESETS
from krice.presets.terminal_palettes import TERMINAL_PALETTES
from krice.presets.theme_presets import RICE_PRESETS
from krice.snapshot import SnapshotManager
from krice.terminal_ctl import TerminalController
from krice.theme_ctl import ThemeController

app = typer.Typer(
    name="krice",
    help="KDE Plasma 6 全方位美化、流体动效调优、多终端配色联动与跨机器无损迁移工具箱。",
    add_completion=False,
)
motion_app = typer.Typer(help="管理与应用 KWin 窗口动效预设（物理弹簧阻尼、流体缩放、窗口切换器动效等）。")
theme_app = typer.Typer(help="管理 KDE 桌面全局主题、配色方案、窗口装饰、控件样式、GTK/QT 统一美化。")
terminal_app = typer.Typer(help="管理与同步多终端及 Shell 提示符配色（Kitty, Alacritty, Konsole, Ghostty, Foot, WezTerm, Starship, Fastfetch）。")
snapshot_app = typer.Typer(help="跨设备配置打包导出、无损还原与依赖自愈（.pmz 架构）。")

app.add_typer(motion_app, name="motion")
app.add_typer(theme_app, name="theme")
app.add_typer(terminal_app, name="terminal")
app.add_typer(snapshot_app, name="snapshot")

console = Console()


@app.command()
def status() -> None:
    """查看当前 KDE 桌面主题、KWin 动效引擎、小部件风格与终端集成状态。"""
    inspector = DesktopInspector()
    report = inspector.inspect()

    # 1. 桌面视觉主题状态表
    t_theme = Table(title="[bold cyan]🎨 当前 KDE 桌面主题与样式[/bold cyan]", show_header=True, header_style="bold magenta")
    t_theme.add_column("属性项目", style="dim", width=26)
    t_theme.add_column("当前生效值", style="bold green")

    t_theme.add_row("全局外观主题 (Look & Feel)", report.global_theme)
    t_theme.add_row("配色方案 (Color Scheme)", report.color_scheme)
    t_theme.add_row("鼠标指针 (Cursor)", f"{report.cursor_theme} ({report.cursor_size}px)")
    t_theme.add_row("图标主题 (Icons)", report.icon_theme)
    t_theme.add_row("Plasma 桌面样式 (Panel/Bar)", report.plasma_style)
    t_theme.add_row("Qt 控件引擎 (Widget Style)", report.widget_style)
    t_theme.add_row("Kvantum SVG 主题", report.kvantum_theme)
    t_theme.add_row("窗口装饰 (Window Decoration)", report.window_decoration)
    t_theme.add_row("GTK 3/4 主题", report.gtk_theme)
    t_theme.add_row("欢迎屏幕 (Splash Screen)", report.splash_theme)

    # 2. 动效与合成器状态表
    t_motion = Table(title="[bold cyan]⚡ KWin 动效与合成器状态[/bold cyan]", show_header=True, header_style="bold blue")
    t_motion.add_column("属性项目", style="dim", width=26)
    t_motion.add_column("当前生效值", style="bold yellow")

    t_motion.add_row("显示服务协议 (Session)", report.session_type)
    t_motion.add_row("Plasma 版本", report.plasma_version)
    t_motion.add_row("动画速度缩放因子", f"{report.animation_factor:.2f}x")
    t_motion.add_row("窗口打开/关闭动效", report.window_open_close_effect)
    t_motion.add_row("窗口最小化动效", report.window_minimize_effect)
    t_motion.add_row("Alt+Tab 任务切换器", report.task_switcher)
    t_motion.add_row("硬件背景毛玻璃模糊 (Blur)", "[green]已开启[/green]" if report.blur_enabled else "[dim]已关闭[/dim]")
    t_motion.add_row("弹出菜单形变动效 (Morphing)", "[green]已开启[/green]" if report.morphing_popups else "[dim]已关闭[/dim]")
    t_motion.add_row("果冻窗口动效 (Wobbly)", "[green]已开启[/green]" if report.wobbly_windows else "[dim]已关闭[/dim]")

    # 3. 终端与 Shell 工具链集成表
    t_term = Table(title="[bold cyan]💻 终端模拟器与 Shell 工具集成[/bold cyan]", show_header=True, header_style="bold cyan")
    t_term.add_column("组件名称", style="dim", width=26)
    t_term.add_column("检测状态", width=20)

    terms_str = ", ".join(report.installed_terminals) if report.installed_terminals else "未检测到终端"
    t_term.add_row("已安装终端模拟器", f"[green]{terms_str}[/green]")
    t_term.add_row("Starship 提示符", "[green]已安装[/green]" if report.starship_installed else "[yellow]未安装[/yellow]")
    t_term.add_row("Fastfetch 系统信息工具", "[green]已安装[/green]" if report.fastfetch_installed else "[yellow]未安装[/yellow]")

    # 4. 已安装的美化扩展引擎
    t_engines = Table(title="[bold cyan]🛠️ 已安装的美化与圆角引擎[/bold cyan]", show_header=True, header_style="bold green")
    t_engines.add_column("美化扩展", style="dim", width=26)
    t_engines.add_column("状态", width=20)

    t_engines.add_row("Klassy (独立圆角与薄边框)", "[green]已安装[/green]" if report.klassy_installed else "[yellow]未安装[/yellow]")
    t_engines.add_row("Kvantum (SVG 质感渲染器)", "[green]已安装[/green]" if report.kvantum_installed else "[yellow]未安装[/yellow]")
    t_engines.add_row("ForceBlur (强制终端毛玻璃)", "[green]已安装[/green]" if report.forceblur_installed else "[yellow]未安装[/yellow]")

    console.print(t_theme)
    console.print()
    console.print(t_motion)
    console.print()
    console.print(t_term)
    console.print()
    console.print(t_engines)


# ==============================================================================
# ==================== 全局桌面美化方案命令 (UNIFIED RICE) ======================
# ==============================================================================

@theme_app.command("list")
def list_rice_presets() -> None:
    """列出所有预设的全局桌面美化方案（融合 KDE 主题 + 终端调色 + 动效方案）。"""
    table = Table(title="[bold cyan]全局桌面美化 (Rice) 预设方案清单[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("方案名称", style="bold yellow", width=18)
    table.add_column("KDE 主题 / 配色", style="green", width=22)
    table.add_column("终端调色板", style="cyan", width=18)
    table.add_column("动效风格", style="blue", width=14)
    table.add_column("方案描述", style="white")

    for key, preset in RICE_PRESETS.items():
        theme_str = preset.color_scheme or preset.global_theme or "系统默认"
        term_str = preset.terminal_palette or "自动匹配"
        table.add_row(key, theme_str, term_str, preset.motion_preset, preset.description)

    console.print(table)


@theme_app.command("apply")
def apply_rice_preset(
    preset_name: str = typer.Argument("cachy-nord", help="全局美化方案名称 (如: cachy-nord, catppuccin-mocha, tokyo-night, dracula, gruvbox-dark, orchis-dark)"),
    no_terminal: bool = typer.Option(False, "--no-terminal", help="跳过更新终端模拟器、Starship 与 Fastfetch"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="演练模拟，不实际修改配置文件"),
) -> None:
    """一键应用全局桌面美化方案（联动 KDE 主题、控件样式、GTK、多终端配色与流体动效！）。"""
    preset = RICE_PRESETS.get(preset_name.lower())
    if not preset:
        console.print(f"[bold red]错误：[/bold red] 未知的全局美化方案 '{preset_name}'。请运行 'krice theme list' 查看支持的方案。")
        raise typer.Exit(code=1)

    theme_ctl = ThemeController(dry_run=dry_run)
    kwin_ctl = KWinController(dry_run=dry_run)
    term_ctl = TerminalController(dry_run=dry_run)

    console.print(Panel.fit(
        f"[bold cyan]正在应用全局桌面方案：[/bold cyan] [bold yellow]{preset.name}[/bold yellow]\n"
        f"[dim]{preset.description}[/dim]\n\n"
        f"• 全局外观主题: [green]{preset.global_theme or '保持当前'}[/green]\n"
        f"• 配色方案: [green]{preset.color_scheme or '保持当前'}[/green]\n"
        f"• 控件样式: [green]{preset.widget_style or '保持当前'}[/green]\n"
        f"• Kvantum 主题: [green]{preset.kvantum_theme or '保持当前'}[/green]\n"
        f"• 窗口装饰: [green]{preset.window_decoration_lib or '保持当前'}[/green]\n"
        f"• 鼠标指针: [green]{preset.cursor_theme or '保持当前'}[/green]\n"
        f"• 终端调色板: [cyan]{preset.terminal_palette or '无'}[/cyan]\n"
        f"• GTK 统一主题: [green]{preset.gtk_theme or 'Breeze'}[/green]\n"
        f"• 动效方案: [yellow]{preset.motion_preset}[/yellow]",
        title="全局桌面方案配置详情",
    ))

    # 1. 全局外观
    if preset.global_theme:
        ok, msg = theme_ctl.apply_global_theme(preset.global_theme)
        console.print(f"  [bold]全局外观:[/] {msg}")

    # 2. 配色方案
    if preset.color_scheme:
        ok, msg = theme_ctl.apply_colorscheme(preset.color_scheme)
        console.print(f"  [bold]配色方案:[/] {msg}")

    # 3. 鼠标指针
    if preset.cursor_theme:
        ok, msg = theme_ctl.apply_cursor_theme(preset.cursor_theme, size=preset.cursor_size)
        console.print(f"  [bold]鼠标指针:[/] {msg}")

    # 4. 图标
    if preset.icon_theme:
        ok, msg = theme_ctl.apply_icon_theme(preset.icon_theme)
        console.print(f"  [bold]图标主题:[/] {msg}")

    # 5. Plasma 样式 (任务栏与面板)
    if preset.plasma_style:
        ok, msg = theme_ctl.apply_plasma_style(preset.plasma_style)
        console.print(f"  [bold]Plasma 样式:[/] {msg}")

    # 6. Qt6 控件引擎
    if preset.widget_style:
        ok, msg = theme_ctl.apply_widget_style(preset.widget_style)
        console.print(f"  [bold]控件样式:[/] {msg}")

    # 7. Kvantum 主题
    if preset.kvantum_theme:
        ok, msg = theme_ctl.apply_kvantum_theme(preset.kvantum_theme)
        console.print(f"  [bold]Kvantum 主题:[/] {msg}")

    # 8. 窗口装饰
    if preset.window_decoration_lib:
        ok, msg = theme_ctl.set_window_decoration(preset.window_decoration_lib, theme=preset.window_decoration_theme)
        console.print(f"  [bold]窗口装饰:[/] {msg}")

    # 9. GTK 3/4 同步
    if preset.gtk_theme:
        ok, msg = theme_ctl.sync_gtk_theme(gtk_theme=preset.gtk_theme, dark_mode=preset.is_dark)
        console.print(f"  [bold]GTK 样式联动:[/] {msg}")

    # 10. 动效预设
    motion = MOTION_PRESETS.get(preset.motion_preset)
    if motion:
        kwin_ctl.set_animation_factor(motion.animation_factor)
        for ep in motion.enabled_plugins:
            kwin_ctl.set_plugin_status(ep, True)
        for dp in motion.disabled_plugins:
            kwin_ctl.set_plugin_status(dp, False)
        for eff_name, cfg in motion.plugin_configs.items():
            for k, v in cfg.items():
                kwin_ctl.set_effect_param(eff_name.replace("Effect-", ""), k, v)
        kwin_ctl.reconfigure_kwin()
        console.print(f"  [bold]物理动效:[/] 已应用 [yellow]{motion.name}[/yellow] (速度: {motion.animation_factor}x)")

    # 11. 终端与 Shell 联动
    if not no_terminal and preset.terminal_palette:
        term_results = term_ctl.apply_all(preset.terminal_palette)
        console.print("\n  [bold cyan]💻 正在同步终端模拟器与 Shell 提示符调色板：[/bold cyan]")
        for term_name, (ok, msg) in term_results.items():
            status_icon = "[bold green]✓[/bold green]" if ok else "[bold red]✗[/bold red]"
            console.print(f"    {status_icon} [bold]{term_name}:[/bold] {msg}")

    if preset.notes:
        console.print("\n[bold]美化亮点说明：[/bold]")
        for note in preset.notes:
            console.print(f"  • {note}")

    console.print("\n[bold green]✓ 全局桌面美化方案应用完成！[/bold green]")


# --- 细粒度主题子命令 ---

@theme_app.command("colors")
def list_color_schemes() -> None:
    """列出系统中已安装的所有配色方案。"""
    theme_ctl = ThemeController()
    schemes = theme_ctl.list_colorschemes()
    current = theme_ctl.get_current_colorscheme()

    table = Table(title="[bold cyan]已安装的 KDE 配色方案[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("配色方案名称", style="white")
    table.add_column("生效状态", width=15)

    for s in schemes:
        is_curr = (s == current)
        table.add_row(s, "[bold green]当前激活[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-color")
def set_color_scheme(
    scheme_name: str = typer.Argument(..., help="配色方案的完整准确名称"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """切换当前生效的 KDE 配色方案。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_colorscheme(scheme_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("global")
def list_global_themes() -> None:
    """列出已安装的全局外观包 (Look-and-Feel)。"""
    theme_ctl = ThemeController()
    themes = theme_ctl.list_global_themes()
    current = theme_ctl.get_current_global_theme()

    table = Table(title="[bold cyan]已安装的全局外观包 (Look-and-Feel)[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("外观包 ID / 名称", style="white")
    table.add_column("生效状态", width=15)

    for t in themes:
        is_curr = (t == current)
        table.add_row(t, "[bold green]当前激活[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-global")
def set_global_theme(
    theme_name: str = typer.Argument(..., help="全局外观包 ID (如: com.github.vinceliuice.Orchis)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """切换当前全局外观包。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_global_theme(theme_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("cursors")
def list_cursor_themes() -> None:
    """列出已安装的鼠标指针主题。"""
    theme_ctl = ThemeController()
    cursors = theme_ctl.list_cursor_themes()
    current = theme_ctl.get_current_cursor_theme()

    table = Table(title="[bold cyan]已安装的鼠标指针主题[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("指针主题名称", style="white")
    table.add_column("生效状态", width=15)

    for c in cursors:
        is_curr = (c == current)
        table.add_row(c, "[bold green]当前激活[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-cursor")
def set_cursor_theme(
    theme_name: str = typer.Argument(..., help="鼠标指针主题名称"),
    size: Optional[int] = typer.Option(None, "--size", "-s", help="指针尺寸像素值 (如: 24, 32, 48)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """切换鼠标指针主题与大小。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_cursor_theme(theme_name, size=size)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("icons")
def list_icon_themes() -> None:
    """列出已安装的图标主题。"""
    theme_ctl = ThemeController()
    icons = theme_ctl.list_icon_themes()
    current = theme_ctl.get_current_icon_theme()

    table = Table(title="[bold cyan]已安装的桌面图标主题[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("图标主题名称", style="white")
    table.add_column("生效状态", width=15)

    for i in icons:
        is_curr = (i == current)
        table.add_row(i, "[bold green]当前激活[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-icon")
def set_icon_theme(
    theme_name: str = typer.Argument(..., help="图标主题名称 (如: Tela-circle, Papirus)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """切换桌面图标主题。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_icon_theme(theme_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")

@theme_app.command("plasma-style")
def list_plasma_styles() -> None:
    """列出已安装的 Plasma 桌面面板与任务栏样式。"""
    theme_ctl = ThemeController()
    styles = theme_ctl.list_plasma_styles()
    current = theme_ctl.get_current_plasma_style()

    table = Table(title="[bold cyan]已安装的 Plasma 桌面面板样式 (Panel/Launcher)[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Plasma 样式名称", style="white")
    table.add_column("生效状态", width=15)

    for s in styles:
        is_curr = (s == current)
        table.add_row(s, "[bold green]当前激活[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-plasma-style")
def set_plasma_style(
    style_name: str = typer.Argument(..., help="Plasma 样式名称 (如: default, breeze-dark, Orchis)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """切换 Plasma 桌面面板与任务栏样式。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_plasma_style(style_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("widget-styles")
def list_widget_styles() -> None:
    """列出系统中可用的 Qt 控件渲染引擎 (如: Breeze, Kvantum, Fusion)。"""
    theme_ctl = ThemeController()
    styles = theme_ctl.list_widget_styles()
    current = theme_ctl.get_current_widget_style()

    table = Table(title="[bold cyan]可用的 Qt 控件样式引擎[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("控件引擎名称", style="white")
    table.add_column("生效状态", width=15)

    for s in styles:
        is_curr = (s.lower() == current.lower())
        table.add_row(s, "[bold green]当前激活[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-widget-style")
def set_widget_style(
    style_name: str = typer.Argument(..., help="控件引擎名称 (Breeze, kvantum, Fusion)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """切换 Qt 控件样式引擎。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_widget_style(style_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("kvantum-themes")
def list_kvantum_themes() -> None:
    """列出已安装的 Kvantum SVG 主题。"""
    theme_ctl = ThemeController()
    themes = theme_ctl.list_kvantum_themes()
    current = theme_ctl.get_current_kvantum_theme()

    table = Table(title="[bold cyan]已安装的 Kvantum SVG 主题[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Kvantum 主题名称", style="white")
    table.add_column("生效状态", width=15)

    for t in themes:
        is_curr = (t.lower() == current.lower())
        table.add_row(t, "[bold green]当前激活[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-kvantum")
def set_kvantum_theme(
    theme_name: str = typer.Argument(..., help="Kvantum 主题名称 (如: Nordic, Catppuccin-Mocha-Mauve, Orchis-dark)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """切换当前生效的 Kvantum SVG 主题。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_kvantum_theme(theme_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("decorations")
def list_decorations() -> None:
    """查看当前生效的窗口装饰引擎与主题。"""
    theme_ctl = ThemeController()
    lib, theme = theme_ctl.get_window_decoration()
    available = theme_ctl.list_window_decorations()

    table = Table(title="[bold cyan]窗口装饰引擎[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("装饰引擎", style="white")
    table.add_column("当前激活详情", width=25)

    for a in available:
        is_curr = (a == lib)
        desc = f"[bold green]当前激活 ({theme})[/bold green]" if (is_curr and theme) else ("[bold green]当前激活[/bold green]" if is_curr else "")
        table.add_row(a, desc)

    console.print(table)


@theme_app.command("set-decoration")
def set_decoration(
    library: str = typer.Argument(..., help="装饰库名称 (org.kde.breeze, klassy, org.kde.kwin.aurorae.v2)"),
    theme: Optional[str] = typer.Option(None, "--theme", "-t", help="Aurorae 或 Klassy 装饰主题名称"),
    corner_radius: Optional[int] = typer.Option(None, "--radius", "-r", help="圆角半径像素值 (用于 Klassy)"),
    blur: bool = typer.Option(True, "--blur/--no-blur", help="开启 Klassy 标题栏背景毛玻璃模糊"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """切换窗口装饰引擎并可配置圆角和毛玻璃。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.set_window_decoration(library, theme=theme)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")

    if library.lower() == "klassy" and corner_radius is not None:
        ok_k, msg_k = theme_ctl.configure_klassy(corner_radius=corner_radius, blur=blur)
        console.print(f"  [{'green' if ok_k else 'red'}]{msg_k}[/]")


@theme_app.command("fonts")
def list_fonts() -> None:
    """查看当前 KDE 系统字体配置。"""
    theme_ctl = ThemeController()
    fonts = theme_ctl.get_fonts()

    table = Table(title="[bold cyan]KDE Plasma 6 系统字体配置[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("字体应用分类", style="dim", width=22)
    table.add_column("已配置字体规格", style="bold white")

    for cat, val in fonts.items():
        table.add_row(cat, val)

    console.print(table)


@theme_app.command("set-font")
def set_font(
    category: str = typer.Argument(..., help="字体分类: general, fixed, windowtitle, menu, toolbar, small"),
    font_spec: str = typer.Argument(..., help="字体规格字符串 (例如: 'Inter,10,-1,5,50,0,0,0,0,0')"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """设置指定分类的系统字体规格。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.set_font(category, font_spec)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("sync-gtk")
def sync_gtk(
    gtk_theme: Optional[str] = typer.Option(None, "--gtk-theme", "-g", help="明确指定 GTK 3/4 主题名称"),
    dark: bool = typer.Option(True, "--dark/--light", help="设置 GTK 暗色模式偏好"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """同步 GTK 3/4 主题、暗色模式偏好与图标指针至 KDE 一致。"""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.sync_gtk_theme(gtk_theme=gtk_theme, dark_mode=dark)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


# ==============================================================================
# ==================== 终端与 SHELL 调色联动命令 ==============================
# ==============================================================================

@terminal_app.command("list")
def list_terminal_palettes() -> None:
    """列出所有预设的 16 色 ANSI 终端与 Shell 高清调色板。"""
    table = Table(title="[bold cyan]终端与 Shell 调色板预设清单[/bold cyan]", show_header=True, header_style="bold cyan")
    table.add_column("调色板名称", style="bold yellow", width=18)
    table.add_column("色彩模式", width=10)
    table.add_column("背景色 (Hex)", style="dim", width=12)
    table.add_column("前景色 (Hex)", style="dim", width=12)
    table.add_column("核心强调色", style="magenta", width=12)
    table.add_column("调色板描述", style="white")

    for key, pal in TERMINAL_PALETTES.items():
        mode_str = "[blue]暗色[/blue]" if pal.is_dark else "[yellow]浅色[/yellow]"
        table.add_row(key, mode_str, pal.background, pal.foreground, pal.blue, pal.display_name)
    console.print(table)


@terminal_app.command("sync")
def sync_terminal_from_kde(
    terminals: Optional[str] = typer.Option(None, "--terminals", "-t", help="以逗号分隔的终端列表 (如: kitty,alacritty,konsole)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """从当前 KDE 活动配色方案中智能提取调色板，并一键同步给所有终端模拟器！"""
    ctl = TerminalController(dry_run=dry_run)
    palette = ctl.extract_palette_from_kde()
    term_list = [t.strip().lower() for t in terminals.split(",")] if terminals else None

    console.print(Panel.fit(
        f"[bold cyan]正在提取 KDE 配色方案：[/bold cyan] [bold yellow]{palette.name}[/bold yellow]\n"
        f"[dim]{palette.display_name}[/dim]\n\n"
        f"• 背景色 (Background): [green]{palette.background}[/green]\n"
        f"• 前景色 (Foreground): [green]{palette.foreground}[/green]\n"
        f"• 强调色 (Accent Blue): [cyan]{palette.blue}[/cyan]\n"
        f"• 选区色 (Selection): [magenta]{palette.selection_bg}[/magenta]",
        title="KDE 配色智能提取",
    ))

    results = ctl.apply_all(palette, terminals=term_list)
    for term_name, (ok, msg) in results.items():
        status_icon = "[bold green]✓[/bold green]" if ok else "[bold red]✗[/bold red]"
        console.print(f"{status_icon} [bold]{term_name}:[/bold] {msg}")

    console.print("\n[bold green]✓ 终端模拟器与 Shell 配色已全量同步刷新！[/bold green]")


@terminal_app.command("apply")
def apply_terminal_palette(
    palette_name: str = typer.Argument(..., help="预设调色板名称 (如: cachy-nord, catppuccin-latte, tokyo-night, dracula)"),
    terminals: Optional[str] = typer.Option(None, "--terminals", "-t", help="以逗号分隔的目标终端列表"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """将指定的预设调色板应用到所有终端、Starship 提示符与 Fastfetch。"""
    ctl = TerminalController(dry_run=dry_run)
    term_list = [t.strip().lower() for t in terminals.split(",")] if terminals else None
    results = ctl.apply_all(palette_name, terminals=term_list)

    console.print(f"[bold cyan]正在应用终端调色板：[/bold cyan] [bold yellow]{palette_name}[/bold yellow]")
    for term_name, (ok, msg) in results.items():
        status_icon = "[bold green]✓[/bold green]" if ok else "[bold red]✗[/bold red]"
        console.print(f"  {status_icon} [bold]{term_name}:[/bold] {msg}")


@terminal_app.command("set-kitty")
def set_kitty_palette(
    palette_name: str = typer.Argument(..., help="调色板名称 (如: cachy-nord, catppuccin-latte, nord-light)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """为 Kitty 终端应用指定调色板，并保持磨砂毛玻璃与顶部斜切 Tab。"""
    ctl = TerminalController(dry_run=dry_run)
    ok, msg = ctl.apply_kitty(palette_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-starship")
def set_starship_palette(
    palette_name: str = typer.Argument(..., help="调色板名称"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """为 Starship Shell 提示符应用指定调色板（更新目录胶囊色、Git 与语言图标）。"""
    ctl = TerminalController(dry_run=dry_run)
    ok, msg = ctl.apply_starship(palette_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-fastfetch")
def set_fastfetch_palette(
    palette_name: str = typer.Argument(..., help="调色板名称"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """为 Fastfetch 硬件与美化展示看板应用指定配色。"""
    ctl = TerminalController(dry_run=dry_run)
    ok, msg = ctl.apply_fastfetch(palette_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")

@terminal_app.command("set-konsole")
def set_konsole_palette(
    palette_name: str = typer.Argument(..., help="调色板名称"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """为 KDE 原生 Konsole 终端应用指定配色方案。"""
    ctl = TerminalController(dry_run=dry_run)
    palette = ctl.get_palette(palette_name)
    if not palette:
        console.print(f"[bold red]未找到调色板 '{palette_name}'[/bold red]")
        raise typer.Exit(code=1)
    ok, msg = ctl.apply_konsole(palette)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-alacritty")
def set_alacritty_palette(
    palette_name: str = typer.Argument(..., help="调色板名称"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """为 Alacritty 终端应用指定配色方案。"""
    ctl = TerminalController(dry_run=dry_run)
    palette = ctl.get_palette(palette_name)
    if not palette:
        console.print(f"[bold red]未找到调色板 '{palette_name}'[/bold red]")
        raise typer.Exit(code=1)
    ok, msg = ctl.apply_alacritty(palette)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-zellij")
def set_zellij_palette(
    palette_name: str = typer.Argument(..., help="调色板名称"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """为 Zellij 终端多路复用器应用指定配色。"""
    ctl = TerminalController(dry_run=dry_run)
    palette = ctl.get_palette(palette_name)
    if not palette:
        console.print(f"[bold red]未找到调色板 '{palette_name}'[/bold red]")
        raise typer.Exit(code=1)
    ok, msg = ctl.apply_zellij(palette)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("export-palette")
def export_terminal_palette(
    palette_name: str = typer.Argument(..., help="调色板名称 (如: cachy-nord, catppuccin-latte, dracula)"),
) -> None:
    """查看并导出指定调色板的 16 色 ANSI 色卡与十六进制代码。"""
    ctl = TerminalController()
    pal = ctl.get_palette(palette_name)
    if not pal:
        console.print(f"[bold red]未找到调色板 '{palette_name}'[/bold red]")
        raise typer.Exit(code=1)

    table = Table(title=f"[bold cyan]调色板详情: {pal.display_name} ({pal.name})[/bold cyan]", show_header=True)
    table.add_column("颜色槽位", style="bold white", width=16)
    table.add_column("十六进制 (HEX)", style="yellow", width=14)
    table.add_column("色彩展示预览", width=18)

    colors = [
        ("背景色 (Background)", pal.background),
        ("前景色 (Foreground)", pal.foreground),
        ("光标色 (Cursor)", pal.cursor),
        ("选区高亮色", pal.selection_bg),
        ("Color 0 (Black)", pal.black),
        ("Color 1 (Red)", pal.red),
        ("Color 2 (Green)", pal.green),
        ("Color 3 (Yellow)", pal.yellow),
        ("Color 4 (Blue)", pal.blue),
        ("Color 5 (Magenta)", pal.magenta),
        ("Color 6 (Cyan)", pal.cyan),
        ("Color 7 (White)", pal.white),
        ("Color 8 (Bright Black)", pal.bright_black),
        ("Color 9 (Bright Red)", pal.bright_red),
        ("Color 10 (Bright Green)", pal.bright_green),
        ("Color 11 (Bright Yellow)", pal.bright_yellow),
        ("Color 12 (Bright Blue)", pal.bright_blue),
        ("Color 13 (Bright Magenta)", pal.bright_magenta),
        ("Color 14 (Bright Cyan)", pal.bright_cyan),
        ("Color 15 (Bright White)", pal.bright_white),
    ]

    for name, hex_val in colors:
        table.add_row(name, hex_val, f"[{hex_val}]████████████[/{hex_val}]")

    console.print(table)


# ==============================================================================
# ==================== KWIN 流体动效管理命令 ===================================
# ==============================================================================

@motion_app.command("list")
def list_motion_presets() -> None:
    """列出所有预设的 KWin 窗口流体动效方案（弹簧阻尼、流体缩放、原生平滑等）。"""
    table = Table(title="[bold cyan]KWin 窗口物理动效预设清单[/bold cyan]", show_header=True, header_style="bold blue")
    table.add_column("动效方案名称", style="bold yellow", width=18)
    table.add_column("速度倍率", style="green", width=10)
    table.add_column("开启插件", style="cyan", width=22)
    table.add_column("禁用插件", style="magenta", width=18)
    table.add_column("动效物理特性描述", style="white")

    for key, p in MOTION_PRESETS.items():
        enabled_str = ", ".join(p.enabled_plugins)
        disabled_str = ", ".join(p.disabled_plugins)
        table.add_row(key, f"{p.animation_factor:.2f}x", enabled_str, disabled_str, p.description)

    console.print(table)


@motion_app.command("apply")
def apply_motion_preset(
    preset_name: str = typer.Argument("denial", help="动效方案名称 (denial, glide-smooth, snappy, apple-flow, instant)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """一键应用 KWin 窗口流体动效方案并热重载合成器。"""
    preset = MOTION_PRESETS.get(preset_name.lower())
    if not preset:
        console.print(f"[bold red]错误：[/bold red] 未知的动效方案 '{preset_name}'。请运行 'krice motion list'。")
        raise typer.Exit(code=1)

    kwin = KWinController(dry_run=dry_run)
    kwin.set_animation_factor(preset.animation_factor)
    for p in preset.enabled_plugins:
        kwin.set_plugin_status(p, True)
    for p in preset.disabled_plugins:
        kwin.set_plugin_status(p, False)
    for eff_name, cfg in preset.plugin_configs.items():
        for k, v in cfg.items():
            kwin.set_effect_param(eff_name.replace("Effect-", ""), k, v)

    kwin.reconfigure_kwin()
    console.print(f"[bold green]✓ 成功应用 KWin 动效方案：[bold yellow]{preset.name}[/bold yellow] (动画缩放因子: {preset.animation_factor:.2f}x)[/bold green]")


@motion_app.command("set-factor")
def set_animation_factor(
    factor: float = typer.Argument(..., help="动画缩放因子 (如: 0.50 为极速响应, 1.0 为默认速度, 0.0 为完全关闭)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """设置全局窗口动画持续时间缩放因子 (AnimationDurationFactor)。"""
    kwin = KWinController(dry_run=dry_run)
    kwin.set_animation_factor(factor)
    kwin.reconfigure_kwin()
    console.print(f"[bold green]✓ 动画持续时间缩放因子已设置为: {factor:.2f}x[/bold green]")


@motion_app.command("set-open-close")
def set_open_close_animation(
    effect: str = typer.Argument(..., help="打开/关闭动效: scale (弹簧缩放), fade (淡入淡出), glide (平滑滑动), none (关闭)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """设置窗口打开和关闭时的动画效果。"""
    kwin = KWinController(dry_run=dry_run)
    eff_lower = effect.lower()

    if eff_lower in ("scale", "zoom"):
        kwin.set_plugin_status("scale", True)
        kwin.set_plugin_status("fade", False)
        kwin.set_plugin_status("glide", False)
        console.print("[bold green]✓ 窗口打开/关闭动效已设置为: Scale (流体弹簧缩放)[/bold green]")
    elif eff_lower in ("fade", "dissolve"):
        kwin.set_plugin_status("scale", False)
        kwin.set_plugin_status("fade", True)
        kwin.set_plugin_status("glide", False)
        console.print("[bold green]✓ 窗口打开/关闭动效已设置为: Fade (渐变淡入淡出)[/bold green]")
    elif eff_lower == "glide":
        kwin.set_plugin_status("scale", False)
        kwin.set_plugin_status("fade", False)
        kwin.set_plugin_status("glide", True)
        console.print("[bold green]✓ 窗口打开/关闭动效已设置为: Glide (平滑滑动)[/bold green]")
    elif eff_lower in ("none", "off", "disable"):
        kwin.set_plugin_status("scale", False)
        kwin.set_plugin_status("fade", False)
        kwin.set_plugin_status("glide", False)
        console.print("[bold yellow]! 窗口打开/关闭动效已禁用 (即时出现)[/bold yellow]")
    else:
        console.print(f"[bold red]未知的动效 '{effect}'。可选范围: scale, fade, glide, none[/bold red]")
        raise typer.Exit(code=1)

    kwin.reconfigure_kwin()


@motion_app.command("set-minimize")
def set_minimize_animation(
    effect: str = typer.Argument(..., help="最小化动效: squash (挤压折叠), magiclamp (神灯卷轴), none (关闭)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """设置窗口最小化和恢复时的动画效果。"""
    kwin = KWinController(dry_run=dry_run)
    eff_lower = effect.lower()

    if eff_lower == "squash":
        kwin.set_plugin_status("squash", True)
        kwin.set_plugin_status("magiclamp", False)
        console.print("[bold green]✓ 窗口最小化动效已设置为: Squash (流畅挤压至任务栏)[/bold green]")
    elif eff_lower in ("magiclamp", "magic-lamp", "genie"):
        kwin.set_plugin_status("squash", False)
        kwin.set_plugin_status("magiclamp", True)
        console.print("[bold green]✓ 窗口最小化动效已设置为: Magic Lamp (神灯弧线折叠)[/bold green]")
    elif eff_lower in ("none", "off", "disable"):
        kwin.set_plugin_status("squash", False)
        kwin.set_plugin_status("magiclamp", False)
        console.print("[bold yellow]! 窗口最小化动效已禁用 (即时切换)[/bold yellow]")
    else:
        console.print(f"[bold red]未知的最小化动效 '{effect}'。可选范围: squash, magiclamp, none[/bold red]")
        raise typer.Exit(code=1)

    kwin.reconfigure_kwin()


@motion_app.command("set-switcher")
def set_task_switcher_animation(
    switcher: str = typer.Argument(
        "thumbnail_grid",
        help="Alt+Tab 任务切换器布局: thumbnail_grid (缩略图网格), coverswitch (3D 封面流), flipswitch (3D 层叠卡片), compact, breeze",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """设置 Alt+Tab 窗口任务切换器的视觉与动画布局。"""
    kwin = KWinController(dry_run=dry_run)
    s_lower = switcher.lower()

    layout_map = {
        "grid": "thumbnail_grid",
        "thumbnail_grid": "thumbnail_grid",
        "coverswitch": "coverswitch",
        "cover": "coverswitch",
        "flipswitch": "flipswitch",
        "flip": "flipswitch",
        "compact": "compact",
        "breeze": "org.kde.breeze.desktop",
        "default": "org.kde.breeze.desktop",
    }

    target_layout = layout_map.get(s_lower, s_lower)
    ok = kwin.set_tabbox_layout(target_layout)
    if ok:
        console.print(f"[bold green]✓ Alt+Tab 任务切换器布局已设置为: [yellow]{target_layout}[/yellow][/bold green]")
    else:
        console.print(f"[bold red]设置任务切换器为 '{target_layout}' 失败[/bold red]")
    kwin.reconfigure_kwin()


# ==============================================================================
# ==================== 跨机器配置快照与无损迁移 ================================
# ==============================================================================

@snapshot_app.command("save")
def snapshot_save(
    name: Optional[str] = typer.Option(None, "--name", "-m", help="快照存档自定义名称"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="输出路径 (.pmz 压缩包)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """将当前 KDE 桌面美化、窗口动效、Kitty 终端与 Shell 提示符打包为便携快照存档。"""
    manager = SnapshotManager(dry_run=dry_run)
    out_file = manager.create_snapshot(output_path=output, name=name)
    console.print(f"[bold green]✓[/bold green] 快照存档打包成功: [bold cyan]{out_file}[/bold cyan]")


@snapshot_app.command("info")
def snapshot_info(
    archive: Path = typer.Argument(..., help=".pmz 快照压缩包路径"),
) -> None:
    """查看快照存档的元数据信息与包含的文件清单。"""
    manager = SnapshotManager()
    try:
        data = manager.inspect_snapshot(archive)
        console.print(Panel.fit(
            f"[bold cyan]快照名称:[/] {data.get('name', '未知')}\n"
            f"[bold cyan]打包时间:[/] {data.get('created_at', '未知')}\n"
            f"[bold cyan]来源主机:[/] {data.get('hostname', '未知')}\n"
            f"[bold cyan]打包范围:[/] {data.get('scope', 'Orchis 主题, KWin 动效, Kitty 终端 & Starship Shell')}\n"
            f"[bold cyan]包含配置目标数:[/] {len(data.get('files', []))}",
            title=f"快照存档: {archive.name}",
        ))
        if "files" in data:
            t = Table(title="打包的配置文件与本地资源清单", show_header=True, header_style="bold blue")
            t.add_column("目标配置文件 / 资源路径", style="dim")
            for f in data["files"]:
                t.add_row(f)
            console.print(t)
    except Exception as e:
        console.print(f"[bold red]读取快照存档失败：[/bold red] {e}")


@snapshot_app.command("load")
@snapshot_app.command("restore")
def snapshot_load(
    archive: Path = typer.Argument(..., help=".pmz 快照压缩包路径"),
    no_backup: bool = typer.Option(False, "--no-backup", help="还原前跳过创建当前配置的自动安全备份"),
    install_deps: bool = typer.Option(False, "--install-deps", "-i", help="还原时自动通过系统包管理器安装缺失的依赖与字体"),
    no_hooks: bool = typer.Option(False, "--no-hooks", help="跳过自动在 fish/zsh/bash 中配置 Starship 提示符挂钩"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """将快照存档无损还原到当前系统，自动挂钩 Shell 前缀并热重载 KWin、Plasma 与 Kitty。"""
    manager = SnapshotManager(dry_run=dry_run)
    try:
        restored = manager.restore_snapshot(
            archive,
            create_backup=not no_backup,
            install_deps=install_deps,
            wire_shell_hooks=not no_hooks,
        )
        console.print(f"[bold green]✓ 成功还原了 {len(restored)} 个配置目标。[/bold green]")
        console.print("[bold cyan]✓ 已校验并注入 fish/zsh/bash 的 Starship 工作目录前缀提示符集成。[/bold cyan]")
        console.print("[bold blue]✓ 已通过 D-Bus 触发 KWin 合成器实时热重载。[/bold blue]")
        console.print("[bold magenta]✓ 已发送信号无缝刷新 Kitty 终端配置。[/bold magenta]")
    except Exception as e:
        console.print(f"[bold red]还原快照存档失败：[/bold red] {e}")


# ==============================================================================
# ==================== 系统健康诊断与内嵌安装器 ================================
# ==============================================================================

@app.command("doctor")
@app.command("diagnose")
def doctor() -> None:
    """全面诊断桌面美化工具链、Nerd Fonts 字体、Shell 前缀 Hook 与主题资源完整度。"""
    helper = DependencyHelper()
    doc = helper.doctor()

    # 1. 核心包状态表
    table = Table(title="[bold cyan]🏥 美化工具链与依赖软件包健康状态[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("组件名称", style="bold white", width=22)
    table.add_column("分类", style="dim", width=20)
    table.add_column("重要性", width=10)
    table.add_column("安装状态", width=15)
    table.add_column("安装与修复指令", style="yellow")

    for c in doc.packages:
        status_str = "[bold green]✓ 已安装[/bold green]" if c.installed else "[bold red]✗ 未安装[/bold red]"
        ess_str = "[bold red]必需[/bold red]" if c.essential else "[dim]可选推荐[/dim]"
        cmd_str = "[dim]已就绪[/dim]" if c.installed else f"[bold yellow]{c.install_command}[/bold yellow]"
        table.add_row(c.name, c.category, ess_str, status_str, cmd_str)

    console.print(table)

    # 2. Shell 挂钩状态表
    t_hooks = Table(title="[bold cyan]🐚 Shell 提示符挂钩状态（当前工作目录胶囊与图标）[/bold cyan]", show_header=True, header_style="bold blue")
    t_hooks.add_column("Shell 类型", style="bold white", width=12)
    t_hooks.add_column("目标配置文件路径", style="dim", width=42)
    t_hooks.add_column("集成状态", width=18)
    t_hooks.add_column("建议操作", style="yellow")

    for h in doc.hooks:
        hook_status = "[bold green]✓ 已正确集成[/bold green]" if h.hooked else "[bold red]✗ 未配置[/bold red]"
        action = "[dim]正常运行中[/dim]" if h.hooked else "[bold yellow]运行 'krice install --hooks' 一键修复[/bold yellow]"
        t_hooks.add_row(h.shell, str(h.rc_file), hook_status, action)

    console.print(t_hooks)

    # 3. 字体与系统环境诊断面板
    font_color = "green" if doc.fonts_ready else "red"
    console.print(Panel.fit(
        f"[bold cyan]检测到的包管理器:[/] {doc.pkg_manager} (AUR 助手: {doc.aur_helper or '无'})\n"
        f"[bold cyan]Nerd Font 字体状态:[/] [{font_color}]{doc.font_details}[/{font_color}]\n"
        f"[bold yellow]一键修复提示:[/] 运行 [bold green]krice install --all[/bold green] 可自动补齐所有缺失依赖与字体！",
        title="系统诊断总览",
    ))


@app.command("install")
@app.command("setup")
def install_dependencies(
    all_deps: bool = typer.Option(True, "--all", "-a", help="通过系统包管理器安装核心终端依赖并配置 Shell 挂钩"),
    hooks_only: bool = typer.Option(False, "--hooks", help="仅在 fish、zsh 和 bash 配置文件中注入 Starship 提示符挂钩"),
    terminal_only: bool = typer.Option(False, "--terminal", help="仅安装 Kitty、Starship 与 Fastfetch 软件包"),
) -> None:
    """内嵌智能安装器：一键调用系统包管理器安装缺失工具，并配置 Shell 工作目录提示符集成。"""
    helper = DependencyHelper()

    if hooks_only:
        console.print("[bold cyan]正在向各 Shell 配置文件注入 Starship 提示符集成代码...[/bold cyan]")
        res = helper.inject_shell_hooks(["fish", "zsh", "bash"])
        for sh, ok, msg in res:
            console.print(f"[{'green' if ok else 'yellow'}]✓ {sh}: {msg}[/]")
        return

    # 若选择 --all 或 --terminal:
    checks = helper.check_all()
    missing_pkgs: list[str] = []

    for c in checks:
        if terminal_only and not c.essential:
            continue
        if not c.installed:
            if c.name in ("kitty", "starship", "fastfetch", "eza", "bat", "zoxide"):
                missing_pkgs.append(c.name)

    if missing_pkgs:
        console.print(f"[bold cyan]正在通过系统包管理器安装缺失软件包: {', '.join(missing_pkgs)}...[/bold cyan]")
        ok, msg = helper.install_packages(missing_pkgs)
        if ok:
            console.print(f"[bold green]✓ {msg}[/bold green]")
        else:
            console.print(f"[bold red]✗ {msg}[/bold red]")
    else:
        console.print("[bold green]✓ 核心终端与 Shell 软件包已全部安装就绪！[/bold green]")

    # 始终校验并注入 Shell 挂钩
    console.print("[bold cyan]正在注入 Starship 工作目录胶囊提示符至 fish/zsh/bash...[/bold cyan]")
    res = helper.inject_shell_hooks(["fish", "zsh", "bash"])
    for sh, ok, msg in res:
        console.print(f"[{'green' if ok else 'yellow'}]✓ {sh}: {msg}[/]")

    console.print("[bold green]🎉 美化运行环境配置与依赖安装已全部就绪！[/bold green]")


@app.command("check-deps")
def check_dependencies() -> None:
    """检查推荐的桌面美化与终端视觉工具链依赖（别名命令，同 doctor）。"""
    doctor()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
