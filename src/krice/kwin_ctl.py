"""KWin 与 KDE Plasma 6 合成器配置与 D-Bus 控制器。"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional


class KWinController:
    """管理 KWin 动效插件、动画持续时间缩放因子与合成器实时热重载。"""

    def __init__(self, dry_run: bool = False, home_dir: Optional[Path] = None) -> None:
        self.dry_run = dry_run
        self.home = home_dir or Path.home()
        self.config_dir = Path(os.environ.get("XDG_CONFIG_HOME", str(self.home / ".config")))
        self.kwriteconfig = shutil.which("kwriteconfig6") or shutil.which("kwriteconfig5") or "kwriteconfig6"
        self.kreadconfig = shutil.which("kreadconfig6") or shutil.which("kreadconfig5") or "kreadconfig6"
        self.qdbus = shutil.which("qdbus6") or shutil.which("qdbus") or "qdbus6"

    def read_config(self, file: str, group: str, key: str, default: str = "") -> str:
        """从 KDE 配置文件中读取指定分组的键值（支持 kreadconfig 与直接 INI 文件解析回退）。"""
        # 若指定了自定义主目录，则优先直接解析文件
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
        """调用 kwriteconfig 向 KDE 配置文件中写入指定值。"""
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
        """获取当前 KDE 动画持续时间缩放因子（1.0 为标准速度，0.0 为即时关闭）。"""
        raw = self.read_config("kdeglobals", "KDE", "AnimationDurationFactor", default="1.0")
        try:
            return float(raw)
        except ValueError:
            return 1.0

    def set_animation_factor(self, factor: float) -> bool:
        """设置 kdeglobals 中的 AnimationDurationFactor。"""
        factor = max(0.0, min(5.0, factor))
        return self.write_config("kdeglobals", "KDE", "AnimationDurationFactor", f"{factor:.2f}")

    def get_plugin_status(self, plugin_id: str) -> bool:
        """检查 kwinrc [Plugins] 中指定动效插件是否开启。"""
        raw = self.read_config("kwinrc", "Plugins", f"{plugin_id}Enabled", default="false")
        return raw.lower() in ("true", "1", "yes")

    def load_effect(self, effect_name: str) -> bool:
        """通过 D-Bus 接口向实时运行中的 KWin 内存直接加载指定动效。"""
        if self.dry_run:
            return True
        try:
            res = subprocess.run(
                [self.qdbus, "org.kde.KWin", "/Effects", "org.kde.kwin.Effects.loadEffect", effect_name],
                capture_output=True,
                check=False,
            )
            return res.returncode == 0
        except Exception:
            return False

    def unload_effect(self, effect_name: str) -> bool:
        """通过 D-Bus 接口从实时运行中的 KWin 内存卸载指定动效。"""
        if self.dry_run:
            return True
        try:
            res = subprocess.run(
                [self.qdbus, "org.kde.KWin", "/Effects", "org.kde.kwin.Effects.unloadEffect", effect_name],
                capture_output=True,
                check=False,
            )
            return res.returncode == 0
        except Exception:
            return False

    def set_plugin_status(self, plugin_id: str, enabled: bool) -> bool:
        """在 kwinrc 中开启或禁用指定动效插件，并同步在内存中热加载/卸载。"""
        ok = self.write_config("kwinrc", "Plugins", f"{plugin_id}Enabled", "true" if enabled else "false")
        if enabled:
            self.load_effect(plugin_id)
        else:
            self.unload_effect(plugin_id)
        return ok

    def set_effect_param(self, effect_name: str, key: str, value: Any) -> bool:
        """设置 kwinrc 中 [Effect-{effect_name}] 下的特定物理参数。"""
        return self.write_config("kwinrc", f"Effect-{effect_name}", key, value)

    def reconfigure_kwin(self) -> tuple[bool, str]:
        """通过 D-Bus 触发 KWin 实时热重载合成器与动效配置。"""
        if self.dry_run:
            return True, "[演练模拟] 已触发 KWin 合成器热重载"
        try:
            res = subprocess.run(
                [self.qdbus, "org.kde.KWin", "/KWin", "org.kde.KWin.reconfigure"],
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0:
                return True, "KWin 合成器热重载成功"
            return False, f"D-Bus 返回非零退出码: {res.stderr.strip()}"
        except Exception as e:
            return False, f"调用 D-Bus 重载失败: {e}"

    def get_tabbox_layout(self) -> str:
        """获取当前 Alt+Tab 任务切换器的布局名称。"""
        return self.read_config("kwinrc", "TabBox", "LayoutName", default="org.kde.breeze.desktop")

    def set_tabbox_layout(self, layout_name: str) -> bool:
        """设置 Alt+Tab 任务切换器的布局并在需要时开启 3D 插件支持。"""
        ok = self.write_config("kwinrc", "TabBox", "LayoutName", layout_name)
        if layout_name in ("coverswitch", "flipswitch"):
            self.set_plugin_status(layout_name, True)
        elif layout_name == "thumbnail_grid":
            self.set_plugin_status("coverswitch", False)
            self.set_plugin_status("flipswitch", False)
        return ok

    def get_kwin_effects_dir(self) -> Path:
        """获取本地用户 KWin 自定义脚本动效存储目录。"""
        data_home = os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))
        return Path(data_home) / "kwin" / "effects"
