"""krice CLI: Unified KDE Plasma 6 animation tuning, theme orchestration & terminal rice toolkit."""

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
    help="KDE Plasma 6 comprehensive theme customization, animation tuning, terminal ricing & multi-machine sync toolkit.",
    add_completion=False,
)
motion_app = typer.Typer(help="Manage and apply KWin window animation presets (e.g. Denial Flutter style, Glide, Snappy).")
theme_app = typer.Typer(help="Manage KDE themes, color schemes, widget styles, Kvantum, GTK, icons, cursors, and unified desktop styles.")
terminal_app = typer.Typer(help="Manage and synchronize terminal color palettes (Konsole, Kitty, Alacritty, Ghostty, Foot, WezTerm, Starship, Fastfetch).")
snapshot_app = typer.Typer(help="Export and restore KDE and terminal configuration bundles across machines.")

app.add_typer(motion_app, name="motion")
app.add_typer(theme_app, name="theme")
app.add_typer(terminal_app, name="terminal")
app.add_typer(snapshot_app, name="snapshot")

console = Console()


@app.command()
def status() -> None:
    """Inspect current KDE Plasma session, active theme, motion effects, widget style, and terminal integration."""
    inspector = DesktopInspector()
    report = inspector.inspect()

    # Visual Theme Table
    t_theme = Table(title="[bold cyan]🎨 Active KDE Theme & Style[/bold cyan]", show_header=True, header_style="bold magenta")
    t_theme.add_column("Property", style="dim", width=26)
    t_theme.add_column("Current Value", style="bold green")

    t_theme.add_row("Global Look & Feel", report.global_theme)
    t_theme.add_row("Color Scheme", report.color_scheme)
    t_theme.add_row("Cursor Theme", f"{report.cursor_theme} ({report.cursor_size}px)")
    t_theme.add_row("Icon Theme", report.icon_theme)
    t_theme.add_row("Plasma Desktop Style", report.plasma_style)
    t_theme.add_row("Widget Style Engine", report.widget_style)
    t_theme.add_row("Kvantum Theme", report.kvantum_theme)
    t_theme.add_row("Window Decoration", report.window_decoration)
    t_theme.add_row("GTK 3/4 Theme", report.gtk_theme)
    t_theme.add_row("Splash Screen", report.splash_theme)

    # Motion & Compositor Table
    t_motion = Table(title="[bold cyan]⚡ KWin Motion & Compositor[/bold cyan]", show_header=True, header_style="bold blue")
    t_motion.add_column("Property", style="dim", width=26)
    t_motion.add_column("Current Value", style="bold yellow")

    t_motion.add_row("Session Type", report.session_type)
    t_motion.add_row("Plasma Shell Version", report.plasma_version)
    t_motion.add_row("Animation Duration Factor", f"{report.animation_factor:.2f}x")
    t_motion.add_row("Window Open/Close Effect", report.window_open_close_effect)
    t_motion.add_row("Background Blur", "[green]Enabled[/green]" if report.blur_enabled else "[dim]Disabled[/dim]")
    t_motion.add_row("Morphing Popups", "[green]Enabled[/green]" if report.morphing_popups else "[dim]Disabled[/dim]")
    t_motion.add_row("Wobbly Windows", "[green]Enabled[/green]" if report.wobbly_windows else "[dim]Disabled[/dim]")

    # Terminal Integration Table
    t_term = Table(title="[bold cyan]💻 Terminal & Shell Tooling[/bold cyan]", show_header=True, header_style="bold cyan")
    t_term.add_column("Component", style="dim", width=26)
    t_term.add_column("Status", width=20)

    terms_str = ", ".join(report.installed_terminals) if report.installed_terminals else "None detected"
    t_term.add_row("Detected Terminals", f"[green]{terms_str}[/green]")
    t_term.add_row("Starship Shell Prompt", "[green]Installed[/green]" if report.starship_installed else "[yellow]Not Installed[/yellow]")
    t_term.add_row("Fastfetch Fetch Tool", "[green]Installed[/green]" if report.fastfetch_installed else "[yellow]Not Installed[/yellow]")

    # Installed Engines Table
    t_engines = Table(title="[bold cyan]🛠️ Installed Theming Engines[/bold cyan]", show_header=True, header_style="bold green")
    t_engines.add_column("Engine / Tool", style="dim", width=26)
    t_engines.add_column("Status", width=20)

    t_engines.add_row("Klassy (Corner & Deco)", "[green]Installed[/green]" if report.klassy_installed else "[yellow]Not Installed[/yellow]")
    t_engines.add_row("Kvantum (SVG Qt Style)", "[green]Installed[/green]" if report.kvantum_installed else "[yellow]Not Installed[/yellow]")
    t_engines.add_row("ForceBlur (Terminal Blur)", "[green]Installed[/green]" if report.forceblur_installed else "[yellow]Not Installed[/yellow]")

    console.print(t_theme)
    console.print()
    console.print(t_motion)
    console.print()
    console.print(t_term)
    console.print()
    console.print(t_engines)


# ==============================================================================
# ==================== UNIFIED RICE & KDE THEME COMMANDS =======================
# ==============================================================================

@theme_app.command("list")
def list_rice_presets() -> None:
    """List unified desktop aesthetic presets (combines KDE themes + terminal palettes + motion)."""
    table = Table(title="[bold cyan]Unified Desktop Aesthetic (Rice) Presets[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("Preset Name", style="bold yellow", width=18)
    table.add_column("KDE Theme / Color", style="green", width=22)
    table.add_column("Terminal Palette", style="cyan", width=18)
    table.add_column("Motion Style", style="blue", width=14)
    table.add_column("Description", style="white")

    for key, preset in RICE_PRESETS.items():
        theme_str = preset.color_scheme or preset.global_theme or "System"
        term_str = preset.terminal_palette or "Auto"
        table.add_row(key, theme_str, term_str, preset.motion_preset, preset.description)

    console.print(table)


@theme_app.command("apply")
def apply_rice_preset(
    preset_name: str = typer.Argument("cachy-nord", help="Rice preset name (e.g. cachy-nord, catppuccin-mocha, tokyo-night, dracula, gruvbox-dark, orchis-dark)"),
    no_terminal: bool = typer.Option(False, "--no-terminal", help="Skip updating terminal emulators, Starship and Fastfetch"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate theme and terminal changes"),
) -> None:
    """Apply a unified desktop preset (orchestrates KDE theme, widget style, Kvantum, GTK, terminal palette & motion!)."""
    preset = RICE_PRESETS.get(preset_name.lower())
    if not preset:
        console.print(f"[bold red]Error:[/bold red] Unknown rice preset '{preset_name}'. Run 'krice theme list'.")
        raise typer.Exit(code=1)

    theme_ctl = ThemeController(dry_run=dry_run)
    kwin_ctl = KWinController(dry_run=dry_run)
    term_ctl = TerminalController(dry_run=dry_run)

    console.print(Panel.fit(
        f"[bold cyan]Applying Unified Style:[/bold cyan] [bold yellow]{preset.name}[/bold yellow]\n"
        f"[dim]{preset.description}[/dim]\n\n"
        f"• Global Theme: [green]{preset.global_theme or 'Unchanged'}[/green]\n"
        f"• Color Scheme: [green]{preset.color_scheme or 'Unchanged'}[/green]\n"
        f"• Widget Style: [green]{preset.widget_style or 'Unchanged'}[/green]\n"
        f"• Kvantum Theme: [green]{preset.kvantum_theme or 'Unchanged'}[/green]\n"
        f"• Window Deco: [green]{preset.window_decoration_lib or 'Unchanged'}[/green]\n"
        f"• Cursor Theme: [green]{preset.cursor_theme or 'Unchanged'}[/green]\n"
        f"• Terminal Palette: [cyan]{preset.terminal_palette or 'None'}[/cyan]\n"
        f"• GTK Theme: [green]{preset.gtk_theme or 'Breeze'}[/green]\n"
        f"• Motion Style: [yellow]{preset.motion_preset}[/yellow]",
        title="Unified Desktop Application",
    ))

    # 1. Global Theme
    if preset.global_theme:
        ok, msg = theme_ctl.apply_global_theme(preset.global_theme)
        console.print(f"  [bold]Global Theme:[/] {msg}")

    # 2. Color Scheme
    if preset.color_scheme:
        ok, msg = theme_ctl.apply_colorscheme(preset.color_scheme)
        console.print(f"  [bold]Color Scheme:[/] {msg}")

    # 3. Cursor
    if preset.cursor_theme:
        ok, msg = theme_ctl.apply_cursor_theme(preset.cursor_theme, size=preset.cursor_size)
        console.print(f"  [bold]Cursor Theme:[/] {msg}")

    # 4. Icons
    if preset.icon_theme:
        ok, msg = theme_ctl.apply_icon_theme(preset.icon_theme)
        console.print(f"  [bold]Icon Theme:[/] {msg}")

    # 5. Plasma Style (Panel/Taskbar)
    if preset.plasma_style:
        ok, msg = theme_ctl.apply_plasma_style(preset.plasma_style)
        console.print(f"  [bold]Plasma Style:[/] {msg}")

    # 6. Widget Style (Qt6 Engine)
    if preset.widget_style:
        ok, msg = theme_ctl.apply_widget_style(preset.widget_style)
        console.print(f"  [bold]Widget Style:[/] {msg}")

    # 7. Kvantum Theme
    if preset.kvantum_theme:
        ok, msg = theme_ctl.apply_kvantum_theme(preset.kvantum_theme)
        console.print(f"  [bold]Kvantum Theme:[/] {msg}")

    # 8. Window Decoration
    if preset.window_decoration_lib:
        ok, msg = theme_ctl.set_window_decoration(preset.window_decoration_lib, theme=preset.window_decoration_theme)
        console.print(f"  [bold]Window Decoration:[/] {msg}")

    # 9. GTK 3/4 Sync
    if preset.gtk_theme:
        ok, msg = theme_ctl.sync_gtk_theme(gtk_theme=preset.gtk_theme, dark_mode=preset.is_dark)
        console.print(f"  [bold]GTK Theme Sync:[/] {msg}")

    # 10. Motion Preset
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
        console.print(f"  [bold]Motion Physics:[/] Applied [yellow]{motion.name}[/yellow] ({motion.animation_factor}x)")

    # 11. Terminal & Shell Sync
    if not no_terminal and preset.terminal_palette:
        term_results = term_ctl.apply_all(preset.terminal_palette)
        console.print("\n  [bold cyan]💻 Synchronizing Terminal Themes & Prompts:[/bold cyan]")
        for term_name, (ok, msg) in term_results.items():
            status_icon = "[bold green]✓[/bold green]" if ok else "[bold red]✗[/bold red]"
            console.print(f"    {status_icon} [bold]{term_name}:[/bold] {msg}")

    if preset.notes:
        console.print("\n[bold]Rice Highlights:[/bold]")
        for note in preset.notes:
            console.print(f"  • {note}")

    console.print("\n[bold green]✓ Unified desktop style applied successfully![/bold green]")


# --- Sub-Element Granular Theme Commands ---

@theme_app.command("colors")
def list_color_schemes() -> None:
    """List all installed color schemes."""
    theme_ctl = ThemeController()
    schemes = theme_ctl.list_colorschemes()
    current = theme_ctl.get_current_colorscheme()

    table = Table(title="[bold cyan]Installed KDE Color Schemes[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Color Scheme Name", style="white")
    table.add_column("Status", width=15)

    for s in schemes:
        is_curr = (s == current)
        table.add_row(s, "[bold green]Active[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-color")
def set_color_scheme(
    scheme_name: str = typer.Argument(..., help="Exact name of installed color scheme"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Switch active KDE color scheme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_colorscheme(scheme_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("global")
def list_global_themes() -> None:
    """List installed Global Look-and-Feel packages."""
    theme_ctl = ThemeController()
    themes = theme_ctl.list_global_themes()
    current = theme_ctl.get_current_global_theme()

    table = Table(title="[bold cyan]Installed Global Look-and-Feel Packages[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Package ID / Name", style="white")
    table.add_column("Status", width=15)

    for t in themes:
        is_curr = (t == current)
        table.add_row(t, "[bold green]Active[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-global")
def set_global_theme(
    theme_name: str = typer.Argument(..., help="Package ID of global look-and-feel theme"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Switch active Global Look-and-Feel theme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_global_theme(theme_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("cursors")
def list_cursor_themes() -> None:
    """List installed mouse cursor themes."""
    theme_ctl = ThemeController()
    cursors = theme_ctl.list_cursor_themes()
    current = theme_ctl.get_current_cursor_theme()

    table = Table(title="[bold cyan]Installed Mouse Cursor Themes[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Cursor Theme Name", style="white")
    table.add_column("Status", width=15)

    for c in cursors:
        is_curr = (c == current)
        table.add_row(c, "[bold green]Active[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-cursor")
def set_cursor_theme(
    theme_name: str = typer.Argument(..., help="Cursor theme name"),
    size: Optional[int] = typer.Option(None, "--size", "-s", help="Cursor size (e.g. 24, 32, 48)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Switch active mouse cursor theme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_cursor_theme(theme_name, size=size)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("icons")
def list_icon_themes() -> None:
    """List installed icon themes."""
    theme_ctl = ThemeController()
    icons = theme_ctl.list_icon_themes()
    current = theme_ctl.get_current_icon_theme()

    table = Table(title="[bold cyan]Installed Icon Themes[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Icon Theme Name", style="white")
    table.add_column("Status", width=15)

    for i in icons:
        is_curr = (i == current)
        table.add_row(i, "[bold green]Active[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-icon")
def set_icon_theme(
    theme_name: str = typer.Argument(..., help="Icon theme name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Switch active icon theme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_icon_theme(theme_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("plasma-style")
def list_plasma_styles() -> None:
    """List installed Plasma Desktop Styles (Panel & Taskbar style)."""
    theme_ctl = ThemeController()
    styles = theme_ctl.list_plasma_styles()
    current = theme_ctl.get_current_plasma_style()

    table = Table(title="[bold cyan]Installed Plasma Desktop Styles (Panel/Launcher)[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Plasma Style Name", style="white")
    table.add_column("Status", width=15)

    for s in styles:
        is_curr = (s == current)
        table.add_row(s, "[bold green]Active[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-plasma-style")
def set_plasma_style(
    style_name: str = typer.Argument(..., help="Plasma Desktop style name (e.g. default, breeze-dark, Nordic)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Switch active Plasma Desktop Style."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_plasma_style(style_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("widget-styles")
def list_widget_styles() -> None:
    """List available Qt widget style engines (e.g. Breeze, Kvantum, Fusion)."""
    theme_ctl = ThemeController()
    styles = theme_ctl.list_widget_styles()
    current = theme_ctl.get_current_widget_style()

    table = Table(title="[bold cyan]Available Qt Widget Style Engines[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Widget Style Engine", style="white")
    table.add_column("Status", width=15)

    for s in styles:
        is_curr = (s.lower() == current.lower())
        table.add_row(s, "[bold green]Active[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-widget-style")
def set_widget_style(
    style_name: str = typer.Argument(..., help="Widget style engine (Breeze, kvantum, Fusion)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Switch active Qt widget style engine."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_widget_style(style_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("kvantum-themes")
def list_kvantum_themes() -> None:
    """List installed Kvantum SVG themes."""
    theme_ctl = ThemeController()
    themes = theme_ctl.list_kvantum_themes()
    current = theme_ctl.get_current_kvantum_theme()

    table = Table(title="[bold cyan]Installed Kvantum SVG Themes[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Kvantum Theme Name", style="white")
    table.add_column("Status", width=15)

    for t in themes:
        is_curr = (t.lower() == current.lower())
        table.add_row(t, "[bold green]Active[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-kvantum")
def set_kvantum_theme(
    theme_name: str = typer.Argument(..., help="Kvantum theme name (e.g. Nordic, Catppuccin-Mocha-Mauve, Orchis-dark)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Switch active Kvantum SVG theme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_kvantum_theme(theme_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("decorations")
def list_decorations() -> None:
    """Show active window decoration library and theme."""
    theme_ctl = ThemeController()
    lib, theme = theme_ctl.get_window_decoration()
    available = theme_ctl.list_window_decorations()

    table = Table(title="[bold cyan]Window Decoration Engines[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Decoration Engine", style="white")
    table.add_column("Current Active", width=25)

    for a in available:
        is_curr = (a == lib)
        desc = f"[bold green]Active ({theme})[/bold green]" if (is_curr and theme) else ("[bold green]Active[/bold green]" if is_curr else "")
        table.add_row(a, desc)

    console.print(table)


@theme_app.command("set-decoration")
def set_decoration(
    library: str = typer.Argument(..., help="Decoration library (org.kde.breeze, klassy, org.kde.kwin.aurorae.v2)"),
    theme: Optional[str] = typer.Option(None, "--theme", "-t", help="Decoration theme name if using Aurorae or Klassy"),
    corner_radius: Optional[int] = typer.Option(None, "--radius", "-r", help="Corner radius in px (for Klassy)"),
    blur: bool = typer.Option(True, "--blur/--no-blur", help="Enable titlebar blur in Klassy"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Switch window decoration and configure Klassy parameters."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.set_window_decoration(library, theme=theme)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")

    if library.lower() == "klassy" and corner_radius is not None:
        ok_k, msg_k = theme_ctl.configure_klassy(corner_radius=corner_radius, blur=blur)
        console.print(f"  [{'green' if ok_k else 'red'}]{msg_k}[/]")


@theme_app.command("fonts")
def list_fonts() -> None:
    """Display current KDE system fonts."""
    theme_ctl = ThemeController()
    fonts = theme_ctl.get_fonts()

    table = Table(title="[bold cyan]KDE Plasma 6 System Fonts[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Category", style="dim", width=22)
    table.add_column("Configured Font", style="bold white")

    for cat, val in fonts.items():
        table.add_row(cat, val)

    console.print(table)


@theme_app.command("set-font")
def set_font(
    category: str = typer.Argument(..., help="Category: general, fixed, windowtitle, menu, toolbar, small"),
    font_spec: str = typer.Argument(..., help="Font specification (e.g. 'Inter,10,-1,5,50,0,0,0,0,0')"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Set system font specification for a category."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.set_font(category, font_spec)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("splash")
def list_splash_themes() -> None:
    """List installed splash screen themes."""
    theme_ctl = ThemeController()
    splashes = theme_ctl.list_splash_themes()
    curr_theme, curr_eng = theme_ctl.get_current_splash()

    table = Table(title="[bold cyan]Installed KDE Splash Screen Themes[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Splash Theme Name", style="white")
    table.add_column("Status", width=15)

    for s in splashes:
        is_curr = (s == curr_theme)
        table.add_row(s, "[bold green]Active[/bold green]" if is_curr else "")

    console.print(table)


@theme_app.command("set-splash")
def set_splash_theme(
    theme_name: str = typer.Argument(..., help="Splash screen theme name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Set active splash screen theme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_splash_theme(theme_name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("gtk")
def show_gtk_status() -> None:
    """Display active GTK 3/4 theme settings."""
    theme_ctl = ThemeController()
    gtk_theme = theme_ctl.get_gtk_theme()
    console.print(f"[bold cyan]Current GTK Theme:[/] [bold green]{gtk_theme}[/bold green]")


@theme_app.command("sync-gtk")
def sync_gtk(
    theme_name: Optional[str] = typer.Option(None, "--theme", "-t", help="GTK theme name (default auto-matched)"),
    dark: bool = typer.Option(True, "--dark/--light", help="Set GTK dark/light application preference"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Synchronize GTK 3/4 settings and GNOME preferences with KDE."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.sync_gtk_theme(gtk_theme=theme_name, dark_mode=dark)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("palette")
def show_palette_summary() -> None:
    """Inspect colors extracted from the active KDE color scheme."""
    theme_ctl = ThemeController()
    pal = theme_ctl.get_active_palette_summary()

    table = Table(title="[bold cyan]Active KDE Color Palette Summary[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Role", style="dim", width=22)
    table.add_column("Hex Color", style="bold white", width=14)
    table.add_column("Visual Color Sample", width=20)

    for role, hex_val in pal.items():
        if role == "ColorScheme":
            table.add_row("ColorScheme Name", hex_val, "")
        else:
            sample = f"[{hex_val}]██████████[/{hex_val}]"
            table.add_row(role, hex_val, sample)

    console.print(table)


@theme_app.command("set-wallpaper")
def set_wallpaper(
    image_path: Path = typer.Argument(..., help="Path to wallpaper image file"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Set desktop wallpaper image."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_wallpaper(image_path)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


# ==============================================================================
# ==================== TERMINAL & PROMPT THEME COMMANDS ========================
# ==============================================================================

@terminal_app.command("list")
def list_terminal_palettes() -> None:
    """List all available terminal color palettes and detected terminals."""
    term_ctl = TerminalController()
    detected = term_ctl.detect_installed_terminals()

    # Palette Table
    table = Table(title="[bold cyan]Available Terminal Color Palettes[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("Palette Name", style="bold yellow", width=18)
    table.add_column("Mode", width=8)
    table.add_column("Background", width=12)
    table.add_column("Foreground", width=12)
    table.add_column("Display Name", style="white")

    for key, pal in TERMINAL_PALETTES.items():
        mode_str = "[dim]Dark[/dim]" if pal.is_dark else "[bold white]Light[/bold white]"
        bg_sample = f"[{pal.background}]██[/] {pal.background}"
        fg_sample = f"[{pal.foreground}]██[/] {pal.foreground}"
        table.add_row(key, mode_str, bg_sample, fg_sample, pal.display_name)

    # Detected Table
    t_det = Table(title="[bold cyan]Detected Terminal & Shell Tooling[/bold cyan]", show_header=True, header_style="bold green")
    t_det.add_column("Terminal / Tool", style="white", width=22)
    t_det.add_column("Status", width=18)

    for tool, ok in detected.items():
        t_det.add_row(tool.capitalize(), "[bold green]Detected[/bold green]" if ok else "[dim]Not Found[/dim]")

    console.print(table)
    console.print()
    console.print(t_det)


@terminal_app.command("apply")
def apply_terminal_palette(
    palette_name: str = typer.Argument("cachy-nord", help="Palette name (e.g. cachy-nord, catppuccin-mocha, tokyo-night, dracula, gruvbox-dark)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate terminal changes"),
) -> None:
    """Apply a color palette across ALL installed terminals, Starship prompt & Fastfetch."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.get_palette(palette_name.lower())
    if not pal:
        console.print(f"[bold red]Error:[/bold red] Unknown terminal palette '{palette_name}'. Run 'krice terminal list'.")
        raise typer.Exit(code=1)

    console.print(Panel.fit(
        f"[bold cyan]Applying Terminal Palette:[/bold cyan] [bold yellow]{pal.display_name}[/bold yellow]\n"
        f"• Background: [{pal.background}]██[/] {pal.background} | Foreground: [{pal.foreground}]██[/] {pal.foreground}\n"
        f"• Mode: {'Dark' if pal.is_dark else 'Light'}",
        title="Terminal Theming",
    ))

    results = term_ctl.apply_all(pal)
    for term_name, (ok, msg) in results.items():
        status_icon = "[bold green]✓[/bold green]" if ok else "[bold red]✗[/bold red]"
        console.print(f"  {status_icon} [bold]{term_name}:[/bold] {msg}")

    console.print("\n[bold green]✓ Terminal palettes updated successfully![/bold green]")


@terminal_app.command("sync")
def sync_terminal_from_kde(
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate terminal changes"),
) -> None:
    """Extract colors from the active KDE color scheme and synchronize all terminals."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.extract_palette_from_kde()

    console.print(Panel.fit(
        f"[bold cyan]Dynamically Synthesizing Palette from Active KDE Theme[/bold cyan]\n"
        f"• Background: [{pal.background}]██[/] {pal.background} | Foreground: [{pal.foreground}]██[/] {pal.foreground}\n"
        f"• Accent / Cursor: [{pal.cursor}]██[/] {pal.cursor}",
        title="KDE -> Terminal Sync",
    ))

    results = term_ctl.apply_all(pal)
    for term_name, (ok, msg) in results.items():
        status_icon = "[bold green]✓[/bold green]" if ok else "[bold red]✗[/bold red]"
        console.print(f"  {status_icon} [bold]{term_name}:[/bold] {msg}")

    console.print("\n[bold green]✓ Terminals synchronized with KDE color scheme![/bold green]")


@terminal_app.command("set-konsole")
def set_konsole_theme(
    palette_name: str = typer.Argument(..., help="Palette name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Apply palette specifically to KDE Konsole."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.get_palette(palette_name.lower()) or term_ctl.extract_palette_from_kde()
    ok, msg = term_ctl.apply_konsole(pal)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-alacritty")
def set_alacritty_theme(
    palette_name: str = typer.Argument(..., help="Palette name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Apply palette specifically to Alacritty."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.get_palette(palette_name.lower()) or term_ctl.extract_palette_from_kde()
    ok, msg = term_ctl.apply_alacritty(pal)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-kitty")
def set_kitty_theme(
    palette_name: str = typer.Argument(..., help="Palette name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Apply palette specifically to Kitty."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.get_palette(palette_name.lower()) or term_ctl.extract_palette_from_kde()
    ok, msg = term_ctl.apply_kitty(pal)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-ghostty")
def set_ghostty_theme(
    palette_name: str = typer.Argument(..., help="Palette name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Apply palette specifically to Ghostty."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.get_palette(palette_name.lower()) or term_ctl.extract_palette_from_kde()
    ok, msg = term_ctl.apply_ghostty(pal)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-foot")
def set_foot_theme(
    palette_name: str = typer.Argument(..., help="Palette name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Apply palette specifically to Foot."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.get_palette(palette_name.lower()) or term_ctl.extract_palette_from_kde()
    ok, msg = term_ctl.apply_foot(pal)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-wezterm")
def set_wezterm_theme(
    palette_name: str = typer.Argument(..., help="Palette name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Apply palette specifically to WezTerm."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.get_palette(palette_name.lower()) or term_ctl.extract_palette_from_kde()
    ok, msg = term_ctl.apply_wezterm(pal)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-starship")
def set_starship_theme(
    palette_name: str = typer.Argument(..., help="Palette name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Apply palette specifically to Starship prompt."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.get_palette(palette_name.lower()) or term_ctl.extract_palette_from_kde()
    ok, msg = term_ctl.apply_starship(pal)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("set-fastfetch")
def set_fastfetch_theme(
    palette_name: str = typer.Argument(..., help="Palette name"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Apply palette specifically to Fastfetch."""
    term_ctl = TerminalController(dry_run=dry_run)
    pal = term_ctl.get_palette(palette_name.lower()) or term_ctl.extract_palette_from_kde()
    ok, msg = term_ctl.apply_fastfetch(pal)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@terminal_app.command("export-palette")
def export_palette(
    palette_name: str = typer.Argument("cachy-nord", help="Palette name to display"),
) -> None:
    """Display detailed ANSI 16 colors and hex codes for a palette."""
    term_ctl = TerminalController()
    pal = term_ctl.get_palette(palette_name.lower()) or term_ctl.extract_palette_from_kde()

    table = Table(title=f"[bold cyan]Color Palette: {pal.display_name}[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Slot", style="dim", width=14)
    table.add_column("Normal Hex", width=14)
    table.add_column("Normal Sample", width=14)
    table.add_column("Bright Hex", width=14)
    table.add_column("Bright Sample", width=14)

    slots = [
        ("Black", pal.black, pal.bright_black),
        ("Red", pal.red, pal.bright_red),
        ("Green", pal.green, pal.bright_green),
        ("Yellow", pal.yellow, pal.bright_yellow),
        ("Blue", pal.blue, pal.bright_blue),
        ("Magenta", pal.magenta, pal.bright_magenta),
        ("Cyan", pal.cyan, pal.bright_cyan),
        ("White", pal.white, pal.bright_white),
    ]

    for name, normal_hex, bright_hex in slots:
        norm_sample = f"[{normal_hex}]██████[/{normal_hex}]"
        bright_sample = f"[{bright_hex}]██████[/{bright_hex}]"
        table.add_row(name, normal_hex, norm_sample, bright_hex, bright_sample)

    console.print(table)


# ==============================================================================
# ==================== MOTION & KWIN ANIMATION COMMANDS ========================
# ==============================================================================

@motion_app.command("list")
def list_presets() -> None:
    """List all available window animation presets."""
    table = Table(title="[bold cyan]KWin Window Motion Physics Presets[/bold cyan]", show_header=True, header_style="bold yellow")
    table.add_column("Preset Name", style="bold green", width=18)
    table.add_column("Speed Factor", width=14)
    table.add_column("Enabled Effects", width=34)
    table.add_column("Description", style="white")

    for key, preset in MOTION_PRESETS.items():
        effects = ", ".join(preset.enabled_plugins)
        table.add_row(key, f"{preset.animation_factor:.2f}x", effects, preset.description)

    console.print(table)


@motion_app.command("apply")
def apply_preset(
    preset_name: str = typer.Argument("denial", help="Motion preset name (denial, denial-vivid, glide, snappy, spring-wobbly)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate without applying to kwinrc"),
) -> None:
    """Apply a motion preset to KWin (including Denial Flutter-style fluid scale)."""
    preset = MOTION_PRESETS.get(preset_name.lower())
    if not preset:
        console.print(f"[bold red]Error:[/bold red] Unknown preset '{preset_name}'. Run 'krice motion list'.")
        raise typer.Exit(code=1)

    kwin = KWinController(dry_run=dry_run)

    console.print(Panel.fit(
        f"[bold cyan]Applying Window Motion Preset:[/bold cyan] [bold green]{preset.name}[/bold green]\n"
        f"[dim]{preset.description}[/dim]\n\n"
        f"• Duration Factor: [yellow]{preset.animation_factor:.2f}x[/yellow]\n"
        f"• Active Plugins: [green]{', '.join(preset.enabled_plugins)}[/green]\n"
        f"• Suppressed Plugins: [red]{', '.join(preset.disabled_plugins)}[/red]",
        title="KWin Motion Tuning",
    ))

    kwin.set_animation_factor(preset.animation_factor)
    for ep in preset.enabled_plugins:
        kwin.set_plugin_status(ep, True)
    for dp in preset.disabled_plugins:
        kwin.set_plugin_status(dp, False)
    for eff_name, cfg in preset.plugin_configs.items():
        for k, v in cfg.items():
            kwin.set_effect_param(eff_name.replace("Effect-", ""), k, v)

    ok, msg = kwin.reconfigure_kwin()
    if ok:
        console.print(f"[bold green]✓[/bold green] {msg}")
    else:
        console.print(f"[bold yellow]![/bold yellow] {msg}")

    if preset.notes:
        console.print("\n[bold]Motion Notes:[/bold]")
        for note in preset.notes:
            console.print(f"  • {note}")


@motion_app.command("tune")
def tune_motion(
    factor: float = typer.Option(1.0, "--factor", "-f", help="Animation speed factor (e.g. 0.85 = fluid, 0.35 = snappy)"),
    effect: str = typer.Option("scale", "--effect", "-e", help="Window open/close effect: scale, glide, fade, squash"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Manually fine-tune animation duration factor and active window effect."""
    kwin = KWinController(dry_run=dry_run)
    kwin.set_animation_factor(factor)
    all_effects = ["scale", "glide", "fade", "squash"]
    for eff in all_effects:
        kwin.set_plugin_status(eff, eff == effect.lower())

    console.print(f"[bold green]✓[/bold green] Animation factor set to [yellow]{factor:.2f}x[/yellow]")
    console.print(f"[bold green]✓[/bold green] Window effect set to [yellow]{effect}[/yellow]")
    kwin.reconfigure_kwin()


# ==============================================================================
# ==================== SNAPSHOT & SYNC COMMANDS ================================
# ==============================================================================

@snapshot_app.command("save")
def snapshot_save(
    name: Optional[str] = typer.Option(None, "--name", "-m", help="Custom name for the snapshot"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Custom output path (.pmz)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Export current KDE configurations, themes, and terminal setups into a portable snapshot."""
    manager = SnapshotManager(dry_run=dry_run)
    out_file = manager.create_snapshot(output_path=output, name=name)
    console.print(f"[bold green]✓[/bold green] Snapshot successfully created: [bold cyan]{out_file}[/bold cyan]")


@snapshot_app.command("info")
def snapshot_info(
    archive: Path = typer.Argument(..., help="Path to .pmz snapshot archive"),
) -> None:
    """Inspect the metadata and file contents of a snapshot archive."""
    manager = SnapshotManager()
    try:
        data = manager.inspect_snapshot(archive)
        console.print(Panel.fit(
            f"[bold cyan]Snapshot Name:[/] {data.get('name', 'Unknown')}\n"
            f"[bold cyan]Created At:[/] {data.get('created_at', 'Unknown')}\n"
            f"[bold cyan]Source Host:[/] {data.get('hostname', 'Unknown')}\n"
            f"[bold cyan]Total Bundled Targets:[/] {len(data.get('files', []))}",
            title=f"Archive: {archive.name}",
        ))
        if "files" in data:
            t = Table(title="Contained Configuration Files & Assets", show_header=True, header_style="bold blue")
            t.add_column("Tracked Target", style="dim")
            for f in data["files"]:
                t.add_row(f)
            console.print(t)
    except Exception as e:
        console.print(f"[bold red]Error reading snapshot:[/bold red] {e}")


@snapshot_app.command("load")
def snapshot_load(
    archive: Path = typer.Argument(..., help="Path to .pmz snapshot archive"),
    no_backup: bool = typer.Option(False, "--no-backup", help="Skip creating safety backup before restoring"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
) -> None:
    """Restore a snapshot archive to current machine and reload KWin and themes."""
    manager = SnapshotManager(dry_run=dry_run)
    try:
        restored = manager.restore_snapshot(archive, create_backup=not no_backup)
        console.print(f"[bold green]✓ Restored {len(restored)} configuration targets successfully.[/bold green]")
        console.print("[bold blue]✓ Triggered KWin compositor live reconfigure via D-Bus.[/bold blue]")
    except Exception as e:
        console.print(f"[bold red]Error restoring snapshot:[/bold red] {e}")


# ==============================================================================
# ==================== GENERAL / DEPS COMMANDS =================================
# ==============================================================================

@app.command("check-deps")
def check_dependencies() -> None:
    """Check status of recommended KDE & Terminal visual packages on CachyOS / Arch."""
    helper = DependencyHelper()
    checks = helper.check_all()

    table = Table(title="[bold cyan]CachyOS / Arch Linux Ricing Toolchain Dependencies[/bold cyan]", show_header=True, header_style="bold green")
    table.add_column("Package", style="bold white", width=22)
    table.add_column("Category", style="dim", width=22)
    table.add_column("Status", width=15)
    table.add_column("One-Click Install Command", style="yellow")

    for c in checks:
        status_str = "[bold green]Installed[/bold green]" if c.installed else "[bold red]Missing[/bold red]"
        cmd_str = f"[dim]{c.install_command}[/dim]" if c.installed else f"[bold yellow]{c.install_command}[/bold yellow]"
        table.add_row(c.name, c.category, status_str, cmd_str)

    console.print(table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
