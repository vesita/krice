"""KWin and KDE Plasma 6 configuration & D-Bus controller."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


class KWinController:
    """Manages KWin effects, animation duration factors, and live reconfiguration."""

    def __init__(self, dry_run: bool = False, home_dir: Optional[Path] = None) -> None:
        self.dry_run = dry_run
        self.home = home_dir or Path.home()
        self.config_dir = Path(os.environ.get("XDG_CONFIG_HOME", str(self.home / ".config")))
        self.kwriteconfig = shutil.which("kwriteconfig6") or shutil.which("kwriteconfig5") or "kwriteconfig6"
        self.kreadconfig = shutil.which("kreadconfig6") or shutil.which("kreadconfig5") or "kreadconfig6"
        self.qdbus = shutil.which("qdbus6") or shutil.which("qdbus") or "qdbus6"

    def read_config(self, file: str, group: str, key: str, default: str = "") -> str:
        """Reads a value from a KDE configuration file using kreadconfig or INI fallback."""
        # Direct file parse if custom home/config
        cfg_file = self.config_dir / file
        if cfg_file.exists():
            try:
                in_group = False
                for line in cfg_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                    s = line.strip()
                    if s.startswith("[") and s.endswith("]"):
                        in_group = (s[1:-1].strip() == group)
                    elif in_group and "=" in s and not s.startswith("#"):
                        k, v = s.split("=", 1)
                        if k.strip() == key:
                            return v.strip()
            except Exception:
                pass

        cmd = [self.kreadconfig, "--file", file, "--group", group, "--key", key]
        try:
            env = os.environ.copy()
            env["XDG_CONFIG_HOME"] = str(self.config_dir)
            res = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
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
            env = os.environ.copy()
            env["XDG_CONFIG_HOME"] = str(self.config_dir)
            res = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
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

    def load_effect(self, effect_name: str) -> bool:
        """Dynamically loads a KWin effect into live memory via D-Bus."""
        if self.dry_run:
            return True
        cmd = [self.qdbus, "org.kde.KWin", "/Effects", "org.kde.kwin.Effects.loadEffect", effect_name]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=3)
            return res.returncode == 0
        except Exception:
            return False

    def unload_effect(self, effect_name: str) -> bool:
        """Dynamically unloads a KWin effect from live memory via D-Bus."""
        if self.dry_run:
            return True
        cmd = [self.qdbus, "org.kde.KWin", "/Effects", "org.kde.kwin.Effects.unloadEffect", effect_name]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=3)
            return res.returncode == 0
        except Exception:
            return False

    def set_plugin_status(self, plugin_id: str, enabled: bool) -> bool:
        """Enables or disables a KWin effect plugin in kwinrc [Plugins] and hot-loads it in live memory."""
        ok = self.write_config("kwinrc", "Plugins", f"{plugin_id}Enabled", "true" if enabled else "false")
        if ok and not self.dry_run:
            if enabled:
                self.load_effect(plugin_id)
            else:
                self.unload_effect(plugin_id)
        return ok

    def set_effect_param(self, effect_name: str, key: str, value: Any) -> bool:
        """Sets a parameter under [Effect-{effect_name}] in kwinrc."""
        return self.write_config("kwinrc", f"Effect-{effect_name}", key, value)

    def reconfigure_kwin(self) -> tuple[bool, str]:
        """Triggers KWin live reconfiguration and effects reload via D-Bus."""
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

    def get_tabbox_layout(self) -> str:
        """Returns current Alt+Tab task switcher layout name."""
        return self.read_config("kwinrc", "TabBox", "LayoutName", default="org.kde.breeze.desktop")

    def set_tabbox_layout(self, layout_name: str) -> bool:
        """Sets the Alt+Tab task switcher layout and enables 3D plugins if needed."""
        ok = self.write_config("kwinrc", "TabBox", "LayoutName", layout_name)
        self.write_config("kwinrc", "TabBox", "ShowTabBox", "true")
        self.write_config("kwinrc", "TabBox", "HighlightWindows", "true")
        
        if layout_name == "coverswitch":
            self.set_plugin_status("coverswitch", True)
            self.set_plugin_status("flipswitch", False)
        elif layout_name == "flipswitch":
            self.set_plugin_status("flipswitch", True)
            self.set_plugin_status("coverswitch", False)
        return ok
    def get_kwin_effects_dir(self) -> Path:
        """Returns the local user KWin scripted effects directory."""
        data_home = os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))
        return Path(data_home) / "kwin" / "effects"
