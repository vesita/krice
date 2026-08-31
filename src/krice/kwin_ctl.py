"""KWin and KDE Plasma 6 configuration & D-Bus controller."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


class KWinController:
    """Manages KWin effects, animation duration factors, and live reconfiguration."""

    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.kwriteconfig = shutil.which("kwriteconfig6") or shutil.which("kwriteconfig5") or "kwriteconfig6"
        self.kreadconfig = shutil.which("kreadconfig6") or shutil.which("kreadconfig5") or "kreadconfig6"
        self.qdbus = shutil.which("qdbus6") or shutil.which("qdbus") or "qdbus6"

    def read_config(self, file: str, group: str, key: str, default: str = "") -> str:
        """Reads a value from a KDE configuration file using kreadconfig."""
        cmd = [self.kreadconfig, "--file", file, "--group", group, "--key", key]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            output = res.stdout.strip()
            return output if output else default
        except Exception:
            return default

    def write_config(self, file: str, group: str, key: str, value: Any) -> bool:
        """Writes a value to a KDE configuration file using kwriteconfig."""
        val_str = str(value)
        if self.dry_run:
            return True
        cmd = [self.kwriteconfig, "--file", file, "--group", group, "--key", key, val_str]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            return res.returncode == 0
        except Exception:
            return False

    def get_animation_factor(self) -> float:
        """Returns the current KDE AnimationDurationFactor (1.0 is standard, 0.0 is instant)."""
        raw = self.read_config("kdeglobals", "KDE", "AnimationDurationFactor", default="1.0")
        try:
            return float(raw)
        except ValueError:
            return 1.0

    def set_animation_factor(self, factor: float) -> bool:
        """Sets the KDE AnimationDurationFactor in kdeglobals."""
        factor = max(0.0, min(5.0, factor))
        return self.write_config("kdeglobals", "KDE", "AnimationDurationFactor", f"{factor:.2f}")

    def get_plugin_status(self, plugin_id: str) -> bool:
        """Checks if a KWin effect plugin is enabled in kwinrc [Plugins]."""
        raw = self.read_config("kwinrc", "Plugins", f"{plugin_id}Enabled", default="false")
        return raw.lower() in ("true", "1", "yes")

    def set_plugin_status(self, plugin_id: str, enabled: bool) -> bool:
        """Enables or disables a KWin effect plugin in kwinrc [Plugins]."""
        return self.write_config("kwinrc", "Plugins", f"{plugin_id}Enabled", "true" if enabled else "false")

    def set_effect_param(self, effect_name: str, key: str, value: Any) -> bool:
        """Sets a parameter under [Effect-{effect_name}] in kwinrc."""
        return self.write_config("kwinrc", f"Effect-{effect_name}", key, value)

    def reconfigure_kwin(self) -> tuple[bool, str]:
        """Triggers KWin live reconfiguration via D-Bus."""
        if self.dry_run:
            return True, "[Dry-run] Simulated qdbus6 org.kde.KWin /KWin reconfigure"

        cmd = [self.qdbus, "org.kde.KWin", "/KWin", "reconfigure"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=5)
            if res.returncode == 0:
                return True, "KWin reconfigured successfully via D-Bus."
            return False, f"Failed to reconfigure KWin: {res.stderr.strip()}"
        except Exception as e:
            return False, f"Error calling D-Bus reconfigure: {e}"

    def get_kwin_effects_dir(self) -> Path:
        """Returns the local user KWin scripted effects directory."""
        data_home = os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))
        return Path(data_home) / "kwin" / "effects"
