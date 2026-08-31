"""krice CLI: Unified KDE Plasma 6 animation tuning & desktop sync toolkit."""

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
from krice.presets.theme_presets import RICE_PRESETS
from krice.snapshot import SnapshotManager
from krice.theme_ctl import ThemeController

app = typer.Typer(
    name="krice",
    help="KDE Plasma 6 comprehensive theme customization, animation tuning & multi-machine sync toolkit.",
    add_completion=False,
)
motion_app = typer.Typer(help="Manage and apply KWin window animation presets (e.g. Denial Flutter style).")
theme_app = typer.Typer(help="Manage global themes, color schemes, icons, cursors, and unified desktop styles.")
snapshot_app = typer.Typer(help="Export and restore KDE configuration bundles across machines.")

app.add_typer(motion_app, name="motion")
app.add_typer(theme_app, name="theme")
app.add_typer(snapshot_app, name="snapshot")

console = Console()


@app.command()
def status() -> None:
    """Inspect current KDE Plasma session, active theme, motion effects, and engines."""
    inspector = DesktopInspector()
    report = inspector.inspect()

    # Visual Theme Table
    t_theme = Table(title="[bold cyan]🎨 Active Theme & Visual Style[/bold cyan]", show_header=True, header_style="bold magenta")
    t_theme.add_column("Property", style="dim", width=26)
    t_theme.add_column("Current Value", style="bold green")

    t_theme.add_row("Global Look & Feel", report.global_theme)
    t_theme.add_row("Color Scheme", report.color_scheme)
    t_theme.add_row("Cursor Theme", report.cursor_theme)
    t_theme.add_row("Icon Theme", report.icon_theme)
    t_theme.add_row("Window Decoration", report.window_decoration)

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
    console.print(t_engines)


# ==================== THEME COMMANDS ====================

@theme_app.command("list")
def list_rice_presets() -> None:
    """List unified desktop aesthetic presets (combines themes + colors + motion)."""
    table = Table(title="[bold cyan]Unified Desktop Aesthetic (Rice) Presets[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("Preset Name", style="bold yellow", width=18)
    table.add_column("Color / Global Theme", style="green", width=24)
    table.add_column("Motion Style", style="blue", width=16)
    table.add_column("Description", style="white")

    for key, preset in RICE_PRESETS.items():
        theme_str = preset.color_scheme or preset.global_theme or "System"
        table.add_row(key, theme_str, preset.motion_preset, preset.description)

    console.print(table)


@theme_app.command("apply")
def apply_rice_preset(
    preset_name: str = typer.Argument("cachy-nord", help="Rice preset name (cachy-nord, edna-light, emerald-dark, breeze-twilight)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate theme changes"),
) -> None:
    """Apply a unified desktop preset (changes global theme, colors, cursors, AND motion!)."""
    preset = RICE_PRESETS.get(preset_name.lower())
    if not preset:
        console.print(f"[bold red]Error:[/bold red] Unknown rice preset '{preset_name}'. Run 'krice theme list'.")
        raise typer.Exit(code=1)

    theme_ctl = ThemeController(dry_run=dry_run)
    kwin_ctl = KWinController(dry_run=dry_run)

    console.print(Panel.fit(
        f"[bold cyan]Applying Unified Style:[/bold cyan] [bold yellow]{preset.name}[/bold yellow]\n"
        f"[dim]{preset.description}[/dim]\n\n"
        f"• Global Theme: [green]{preset.global_theme or 'Unchanged'}[/green]\n"
        f"• Color Scheme: [green]{preset.color_scheme or 'Unchanged'}[/green]\n"
        f"• Cursor Theme: [green]{preset.cursor_theme or 'Unchanged'}[/green]\n"
        f"• Motion Style: [yellow]{preset.motion_preset}[/yellow]",
        title="Desktop Style Application",
    ))

    # 1. Apply Global Theme
    if preset.global_theme:
        ok, msg = theme_ctl.apply_global_theme(preset.global_theme)
        console.print(f"[{'green' if ok else 'yellow'}]•[/] Global Theme: {msg}")

    # 2. Apply Color Scheme
    if preset.color_scheme:
        ok, msg = theme_ctl.apply_colorscheme(preset.color_scheme)
        console.print(f"[{'green' if ok else 'yellow'}]•[/] Color Scheme: {msg}")

    # 3. Apply Cursor Theme
    if preset.cursor_theme:
        ok, msg = theme_ctl.apply_cursor_theme(preset.cursor_theme)
        console.print(f"[{'green' if ok else 'yellow'}]•[/] Cursor Theme: {msg}")

    # 4. Apply Window Decoration
    if preset.window_decoration_lib:
        ok, msg = theme_ctl.set_window_decoration(preset.window_decoration_lib, preset.window_decoration_theme)
        console.print(f"[{'green' if ok else 'yellow'}]•[/] Window Decoration: {msg}")

    # 5. Apply Paired Motion
    if preset.motion_preset and preset.motion_preset in MOTION_PRESETS:
        m_preset = MOTION_PRESETS[preset.motion_preset]
        kwin_ctl.set_animation_factor(m_preset.animation_factor)
        for p in m_preset.enabled_plugins:
            kwin_ctl.set_plugin_status(p, True)
        for p in m_preset.disabled_plugins:
            kwin_ctl.set_plugin_status(p, False)
        for group, params in m_preset.plugin_configs.items():
            for k, v in params.items():
                kwin_ctl.set_effect_param(group.replace("Effect-", ""), k, v)
        kwin_ctl.reconfigure_kwin()
        console.print(f"[green]•[/] Paired Motion Applied: [bold]{m_preset.name}[/bold] ({m_preset.animation_factor}x)")

    console.print("\n[bold green]✓ Unified desktop style applied successfully![/bold green]")


@theme_app.command("colors")
def list_color_schemes() -> None:
    """List all installed color schemes."""
    theme_ctl = ThemeController()
    schemes = theme_ctl.list_colorschemes()
    current = theme_ctl.get_current_colorscheme()

    table = Table(title="[bold cyan]Installed Color Schemes[/bold cyan]", show_header=True, header_style="bold blue")
    table.add_column("Scheme Name", style="bold white")
    table.add_column("Status", width=12)

    for s in schemes:
        is_cur = (s.lower() == current.lower())
        table.add_row(s, "[bold green]Active[/bold green]" if is_cur else "")

    console.print(table)


@theme_app.command("set-color")
def set_color_scheme(
    name: str = typer.Argument(..., help="Color scheme name (e.g. CachyOSNord, EdnaLight, BreezeDark)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate changes"),
) -> None:
    """Switch active KDE color scheme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_colorscheme(name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("global")
def list_global_themes() -> None:
    """List installed Global Look-and-Feel packages."""
    theme_ctl = ThemeController()
    themes = theme_ctl.list_global_themes()
    current = theme_ctl.get_current_global_theme()

    table = Table(title="[bold cyan]Installed Global Look & Feel Packages[/bold cyan]", show_header=True, header_style="bold blue")
    table.add_column("Package ID", style="bold white")
    table.add_column("Status", width=12)

    for t in themes:
        is_cur = (t.lower() == current.lower())
        table.add_row(t, "[bold green]Active[/bold green]" if is_cur else "")

    console.print(table)


@theme_app.command("set-global")
def set_global_theme(
    name: str = typer.Argument(..., help="Global theme ID (e.g. CachyOS-Nord, Edna-Light, org.kde.breezedark.desktop)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate changes"),
) -> None:
    """Switch active Global Look-and-Feel theme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_global_theme(name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("cursors")
def list_cursor_themes() -> None:
    """List installed mouse cursor themes."""
    theme_ctl = ThemeController()
    cursors = theme_ctl.list_cursor_themes()
    current = theme_ctl.get_current_cursor_theme()

    table = Table(title="[bold cyan]Installed Cursor Themes[/bold cyan]", show_header=True, header_style="bold blue")
    table.add_column("Cursor Theme", style="bold white")
    table.add_column("Status", width=12)

    for c in cursors:
        is_cur = (c.lower() == current.lower())
        table.add_row(c, "[bold green]Active[/bold green]" if is_cur else "")

    console.print(table)


@theme_app.command("set-cursor")
def set_cursor_theme(
    name: str = typer.Argument(..., help="Cursor theme name"),
    size: Optional[int] = typer.Option(None, "--size", "-s", help="Optional cursor pixel size (e.g. 24, 32)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate changes"),
) -> None:
    """Switch active mouse cursor theme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_cursor_theme(name, size=size)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")

@theme_app.command("icons")
def list_icon_themes() -> None:
    """List installed icon themes."""
    theme_ctl = ThemeController()
    icons = theme_ctl.list_icon_themes()
    current = theme_ctl.get_current_icon_theme()

    table = Table(title="[bold cyan]Installed Icon Themes[/bold cyan]", show_header=True, header_style="bold blue")
    table.add_column("Icon Theme", style="bold white")
    table.add_column("Status", width=12)

    for ic in icons:
        is_cur = (ic.lower() == current.lower())
        table.add_row(ic, "[bold green]Active[/bold green]" if is_cur else "")

    console.print(table)


@theme_app.command("set-icon")
def set_icon_theme(
    name: str = typer.Argument(..., help="Icon theme name (e.g. Fluent, breeze-dark, Papirus)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate changes"),
) -> None:
    """Switch active icon theme."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_icon_theme(name)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


@theme_app.command("set-wallpaper")
def set_wallpaper(
    path: Path = typer.Argument(..., help="Path to wallpaper image file"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate changes"),
) -> None:
    """Set desktop wallpaper image."""
    theme_ctl = ThemeController(dry_run=dry_run)
    ok, msg = theme_ctl.apply_wallpaper(path)
    console.print(f"[{'bold green' if ok else 'bold red'}]{msg}[/]")


# ==================== MOTION COMMANDS ====================

@motion_app.command("list")
def list_presets() -> None:
    """List all available window animation presets."""
    table = Table(title="[bold cyan]Available Motion Presets[/bold cyan]", show_header=True, header_style="bold blue")
    table.add_column("Preset Name", style="bold yellow", width=16)
    table.add_column("Factor", style="green", width=10)
    table.add_column("Description", style="white")

    for key, preset in MOTION_PRESETS.items():
        table.add_row(key, f"{preset.animation_factor}x", preset.description)

    console.print(table)


@motion_app.command("apply")
def apply_preset(
    preset_name: str = typer.Argument("denial", help="Preset name to apply (denial, glide, snappy, spring-wobbly)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate changes without writing files"),
) -> None:
    """Apply a motion preset to KWin (including Denial Flutter-style fluid scale)."""
    preset = MOTION_PRESETS.get(preset_name.lower())
    if not preset:
        console.print(f"[bold red]Error:[/bold red] Unknown preset '{preset_name}'. Run 'krice motion list' to view options.")
        raise typer.Exit(code=1)

    kwin = KWinController(dry_run=dry_run)

    console.print(Panel.fit(
        f"[bold cyan]Applying Motion Preset:[/bold cyan] [bold yellow]{preset.name}[/bold yellow]\n"
        f"[dim]{preset.description}[/dim]\n\n"
        f"• Animation Factor: [green]{preset.animation_factor}x[/green]\n"
        f"• Enabling Plugins: [green]{', '.join(preset.enabled_plugins)}[/green]\n"
        f"• Disabling Plugins: [red]{', '.join(preset.disabled_plugins)}[/red]",
        title="Motion Preset Application",
    ))

    # 1. Animation factor
    kwin.set_animation_factor(preset.animation_factor)

    # 2. Plugins
    for p in preset.enabled_plugins:
        kwin.set_plugin_status(p, True)
    for p in preset.disabled_plugins:
        kwin.set_plugin_status(p, False)

    # 3. Effect parameters
    for group, params in preset.plugin_configs.items():
        for k, v in params.items():
            kwin.set_effect_param(group.replace("Effect-", ""), k, v)

    # 4. Reconfigure KWin
    success, msg = kwin.reconfigure_kwin()
    if success:
        console.print(f"[bold green]✓[/bold green] {msg}")
    else:
        console.print(f"[bold yellow]![/bold yellow] {msg}")

    if preset.notes:
        console.print("\n[bold cyan]Tips & Notes:[/bold cyan]")
        for note in preset.notes:
            console.print(f"  • {note}")


@motion_app.command("tune")
def tune_motion(
    factor: Optional[float] = typer.Option(None, "--factor", "-f", help="Animation speed factor (e.g. 0.85)"),
    effect: Optional[str] = typer.Option(None, "--effect", "-e", help="Open/close effect (scale, glide, fade)"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate changes"),
) -> None:
    """Manually fine-tune animation duration factor and active window effect."""
    kwin = KWinController(dry_run=dry_run)

    if factor is not None:
        kwin.set_animation_factor(factor)
        console.print(f"[green]✓[/green] Set animation factor to [bold]{factor:.2f}x[/bold]")

    if effect:
        eff_lower = effect.lower()
        if eff_lower in ("scale", "glide", "fade", "squash"):
            for candidate in ("scale", "glide", "fade", "squash"):
                kwin.set_plugin_status(candidate, candidate == eff_lower)
            console.print(f"[green]✓[/green] Activated window effect [bold]{eff_lower}[/bold]")
        else:
            console.print(f"[bold red]Unknown effect:[/bold red] {effect}. Expected: scale, glide, fade, squash.")
            raise typer.Exit(code=1)

    kwin.reconfigure_kwin()


# ==================== SNAPSHOT COMMANDS ====================

@snapshot_app.command("save")
def snapshot_save(
    name: Optional[str] = typer.Argument(None, help="Optional profile name (e.g. cachy-desktop-v1)"),
    output: Optional[Path] = typer.Option(None, "--out", "-o", help="Custom output archive path (.pmz)"),
) -> None:
    """Export current KDE configurations, themes, and effects into a portable snapshot."""
    manager = SnapshotManager()
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
            f"[bold cyan]Profile Name:[/bold cyan] {data.get('name', 'N/A')}\n"
            f"[bold cyan]Created At:[/bold cyan] {data.get('created_at', 'N/A')}\n"
            f"[bold cyan]Source Host:[/bold cyan] {data.get('hostname', 'N/A')}\n"
            f"[bold cyan]Tracked Files:[/bold cyan]\n  • " + "\n  • ".join(data.get("files", [])),
            title=f"Snapshot Info: {archive.name}",
        ))
    except Exception as e:
        console.print(f"[bold red]Error reading snapshot:[/bold red] {e}")


@snapshot_app.command("load")
def snapshot_load(
    archive: Path = typer.Argument(..., help="Path to .pmz snapshot archive"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulate extraction without modifying files"),
    no_backup: bool = typer.Option(False, "--no-backup", help="Skip creating safety backup before overwrite"),
) -> None:
    """Restore a snapshot archive to current machine and reload KWin."""
    manager = SnapshotManager(dry_run=dry_run)
    try:
        restored = manager.restore_snapshot(archive, create_backup=not no_backup)
        action_str = "[Dry-run] Would restore" if dry_run else "Successfully restored"
        console.print(f"[bold green]✓[/bold green] {action_str} [bold]{len(restored)}[/bold] items from [cyan]{archive.name}[/cyan].")
        if not dry_run:
            console.print("[dim]KWin reconfigured automatically. Note: some panel changes may require logging out & back in.[/dim]")
    except Exception as e:
        console.print(f"[bold red]Error restoring snapshot:[/bold red] {e}")


# ==================== GENERAL / DEPS ====================

@app.command("check-deps")
def check_dependencies() -> None:
    """Check status of recommended KDE visual & theming packages on CachyOS."""
    helper = DependencyHelper()
    checks = helper.check_all()

    table = Table(title="[bold cyan]CachyOS / Arch Recommended Theming Tools[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("Package", style="bold yellow", width=25)
    table.add_column("Status", width=12)
    table.add_column("Purpose", style="dim")
    table.add_column("Install Command", style="green")

    for c in checks:
        status_text = "[green]Installed[/green]" if c.installed else "[yellow]Missing[/yellow]"
        table.add_row(c.name, status_text, c.description, c.install_command if not c.installed else "[dim]OK[/dim]")

    console.print(table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
