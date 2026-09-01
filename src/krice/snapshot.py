"""Snapshot & Restore manager for KDE Plasma configuration and themes portability."""

from __future__ import annotations

import io
import json
import os
import shutil
import socket
import tarfile
from datetime import datetime
from pathlib import Path
from typing import Any

from krice.kwin_ctl import KWinController

TRACKED_TARGETS = [
    # Core KDE configuration files
    ("config", "kwinrc"),
    ("config", "kdeglobals"),
    ("config", "kglobalshortcutsrc"),
    ("config", "kwinrulesrc"),
    ("config", "kcminputrc"),
    ("config", "plasmarc"),
    ("config", "ksplashrc"),
    ("config", "plasma-org.kde.plasma.desktop-appletsrc"),
    ("config", "plasmashellrc"),
    ("config", "kfontinst"),
    ("config", "konsolerc"),
    # Third-party theme engine & toolkit configurations
    ("config", "klassy"),
    ("config", "Kvantum"),
    ("config", "gtk-3.0"),
    ("config", "gtk-4.0"),
    ("config", "xsettingsd"),
    # Terminal & Shell theme configurations
    ("config", "alacritty"),
    ("config", "kitty"),
    ("config", "ghostty"),
    ("config", "foot"),
    ("config", "wezterm"),
    ("config", "starship.toml"),
    ("config", "fastfetch"),
    ("config", "fish/config.fish"),
    # Input Method (Fcitx5) configurations & themes
    ("config", "fcitx5"),
    # Local custom themes & effects assets
    ("data", "kwin/effects"),
    ("data", "aurorae/themes"),
    ("data", "kwin/scripts"),
    ("data", "color-schemes"),
    ("data", "konsole"),
    ("data", "plasma/look-and-feel"),
    ("data", "plasma/desktoptheme"),
    ("data", "Kvantum"),
    ("data", "fcitx5/themes"),
]


class SnapshotManager:
    """Creates portable snapshots of KDE configs/themes and restores them on another machine."""

    def __init__(self, dry_run: bool = False, home_dir: Path | None = None) -> None:
        self.dry_run = dry_run
        self.home = home_dir or Path.home()
        self.config_dir = Path(os.environ.get("XDG_CONFIG_HOME", str(self.home / ".config")))
        self.data_dir = Path(os.environ.get("XDG_DATA_HOME", str(self.home / ".local" / "share")))
        self.backup_dir = self.home / ".cache" / "krice" / "backups"

    def _resolve_source(self, category: str, rel_path: str) -> Path:
        if category == "config":
            return self.config_dir / rel_path
        elif category == "data":
            return self.data_dir / rel_path
        return self.home / rel_path

    def create_snapshot(self, output_path: Path | None = None, name: str | None = None) -> Path:
        """Packages tracked KDE configurations and themes into a compressed archive (.pmz / tar.gz)."""
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        profile_name = name or f"kde_profile_{timestamp}"

        if output_path is None:
            output_dir = Path.cwd() / "snapshots"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{profile_name}.pmz"
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)

        metadata: dict[str, Any] = {
            "name": profile_name,
            "created_at": now.isoformat(),
            "hostname": socket.gethostname(),
            "files": [],
        }

        # Create tarball
        with tarfile.open(output_path, "w:gz") as tar:
            for category, rel_path in TRACKED_TARGETS:
                src = self._resolve_source(category, rel_path)
                if src.exists():
                    arcname = f"{category}/{rel_path}"
                    tar.add(src, arcname=arcname, recursive=True)
                    metadata["files"].append(arcname)

            # Add metadata JSON inside the archive
            meta_bytes = json.dumps(metadata, indent=2, ensure_ascii=False).encode("utf-8")
            tarinfo = tarfile.TarInfo(name="metadata.json")
            tarinfo.size = len(meta_bytes)
            tarinfo.mtime = int(now.timestamp())
            tar.addfile(tarinfo, io.BytesIO(meta_bytes))

        return output_path

    def inspect_snapshot(self, snapshot_path: Path) -> dict[str, Any]:
        """Reads metadata and contents of a snapshot archive without extracting."""
        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot not found: {snapshot_path}")

        with tarfile.open(snapshot_path, "r:gz") as tar:
            try:
                meta_file = tar.extractfile("metadata.json")
                if meta_file:
                    return json.loads(meta_file.read().decode("utf-8"))
            except KeyError:
                pass
            return {"files": tar.getnames()}

    def restore_snapshot(self, snapshot_path: Path, create_backup: bool = True) -> list[str]:
        """Restores a snapshot archive into current user's ~/.config and ~/.local/share."""
        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot not found: {snapshot_path}")

        restored_items: list[str] = []

        if create_backup and not self.dry_run:
            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            cur_backup_dir = self.backup_dir / f"backup_before_{now_str}"
            cur_backup_dir.mkdir(parents=True, exist_ok=True)
            for category, rel_path in TRACKED_TARGETS:
                src = self._resolve_source(category, rel_path)
                if src.exists():
                    dst = cur_backup_dir / category / rel_path
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        if src.is_dir():
                            shutil.copytree(src, dst, symlinks=True, ignore_dangling_symlinks=True, dirs_exist_ok=True)
                        else:
                            shutil.copy2(src, dst, follow_symlinks=False)
                    except Exception:
                        pass

        with tarfile.open(snapshot_path, "r:gz") as tar:
            for member in tar.getmembers():
                if member.name == "metadata.json":
                    continue

                parts = Path(member.name).parts
                if not parts:
                    continue
                category = parts[0]
                rel_path = Path(*parts[1:])

                if category == "config":
                    target_base = self.config_dir
                elif category == "data":
                    target_base = self.data_dir
                else:
                    continue

                dest = target_base / rel_path
                restored_items.append(str(dest))

                if not self.dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if member.isdir():
                        dest.mkdir(parents=True, exist_ok=True)
                    elif member.issym():
                        if dest.is_symlink() or dest.exists():
                            try:
                                dest.unlink()
                            except Exception:
                                pass
                        try:
                            os.symlink(member.linkname, dest)
                        except Exception:
                            pass
                    elif member.isreg():
                        extracted = tar.extractfile(member)
                        if extracted:
                            dest.write_bytes(extracted.read())

        # Live reload KWin
        if not self.dry_run:
            kwin = KWinController()
            kwin.reconfigure_kwin()

        return restored_items
