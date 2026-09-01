"""Helper for checking and installing KDE & Terminal enhancement tools on CachyOS / Arch Linux."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from typing import List


@dataclass
class PackageCheck:
    name: str
    category: str
    description: str
    installed: bool
    install_command: str


class DependencyHelper:
    """Detects installed theming, motion, and terminal helpers and provides one-click install commands."""

    def check_all(self) -> List[PackageCheck]:
        helper = shutil.which("paru") or shutil.which("yay") or "paru"

        checks = [
            PackageCheck(
                name="klassy-qt6",
                category="Window Decoration & Corners",
                description="Ultra-customizable window decoration (independent corner radius, thin borders)",
                installed=shutil.which("klassy-settings") is not None,
                install_command=f"{helper} -S klassy-qt6",
            ),
            PackageCheck(
                name="kvantum-qt6",
                category="Widget & Blur Engine",
                description="SVG-based Qt6 widget style engine with deep opacity, blur, and theme support",
                installed=shutil.which("kvantummanager") is not None,
                install_command=f"{helper} -S kvantum kvantum-qt6",
            ),
            PackageCheck(
                name="kwin-effect-forceblur-git",
                category="Compositor Effect",
                description="Forces blur behind specified windows (e.g. Alacritty, Kitty, Neovim)",
                installed=shutil.which("kwin_forceblur_config") is not None,
                install_command=f"{helper} -S kwin-effect-forceblur-git",
            ),
            PackageCheck(
                name="starship",
                category="Shell Prompt",
                description="Fast, highly customizable cross-shell prompt with rich Nerd Font iconography",
                installed=shutil.which("starship") is not None,
                install_command=f"{helper} -S starship",
            ),
            PackageCheck(
                name="fastfetch",
                category="System Info Fetcher",
                description="Blazing fast neofetch alternative with customizable logo and color palettes",
                installed=shutil.which("fastfetch") is not None,
                install_command=f"{helper} -S fastfetch",
            ),
            PackageCheck(
                name="alacritty",
                category="Terminal Emulator",
                description="GPU-accelerated, lightweight terminal emulator with live config reload",
                installed=shutil.which("alacritty") is not None,
                install_command=f"{helper} -S alacritty",
            ),
            PackageCheck(
                name="kitty",
                category="Terminal Emulator",
                description="Fast, feature-rich, GPU-based terminal emulator with truecolor & tabs",
                installed=shutil.which("kitty") is not None,
                install_command=f"{helper} -S kitty",
            ),
            PackageCheck(
                name="ghostty",
                category="Terminal Emulator",
                description="Fast, native GPU-rendered terminal emulator with modern typography",
                installed=shutil.which("ghostty") is not None,
                install_command=f"{helper} -S ghostty",
            ),
            PackageCheck(
                name="foot",
                category="Terminal Emulator",
                description="Fast, lightweight, Wayland-native terminal emulator",
                installed=shutil.which("foot") is not None,
                install_command=f"{helper} -S foot",
            ),
            PackageCheck(
                name="konsave",
                category="KDE Snapshot Utility",
                description="CLI utility to backup and restore whole KDE configuration profiles",
                installed=shutil.which("konsave") is not None,
                install_command="pip install konsave",
            ),
        ]
        return checks
