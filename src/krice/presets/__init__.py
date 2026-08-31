"""Preset configurations for KWin animations."""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class MotionPreset:
    name: str
    description: str
    animation_factor: float
    enabled_plugins: list[str] = field(default_factory=list)
    disabled_plugins: list[str] = field(default_factory=list)
    plugin_configs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
