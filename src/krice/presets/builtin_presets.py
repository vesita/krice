"""Catalog of built-in motion presets for krice."""

from krice.presets import MotionPreset
from krice.presets.denial import DENIAL_PRESET, DENIAL_VIVID_PRESET

GLIDE_PRESET = MotionPreset(
    name="glide",
    description="Physical sheet/glide motion (smooth directional sliding with angular tilt)",
    animation_factor=0.90,
    enabled_plugins=["glide", "morphingpopups", "blur"],
    disabled_plugins=["scale", "fade", "squash"],
    plugin_configs={
        "Effect-Glide": {
            "InAngle": -5,
            "OutAngle": 5,
            "InDistance": 15,
            "OutDistance": 15,
            "Duration": 250,
        }
    },
    notes=["Window slides in like a physical sheet of paper with subtle angle."],
)

SNAPPY_PRESET = MotionPreset(
    name="snappy",
    description="Competitive / ultra-fast responsive animations (120Hz/240Hz optimized)",
    animation_factor=0.35,
    enabled_plugins=["scale", "morphingpopups"],
    disabled_plugins=["fade", "glide", "squash", "magiclamp", "wobblywindows"],
    plugin_configs={
        "Effect-Scale": {
            "Duration": 120,
            "InScale": 0.95,
        }
    },
    notes=["Minimal latency for fast multi-tasking and high refresh rate displays."],
)

SPRING_WOBBLY_PRESET = MotionPreset(
    name="spring-wobbly",
    description="Tactile organic physics with subtle wobbly spring bounce and scale",
    animation_factor=1.10,
    enabled_plugins=["scale", "wobblywindows", "morphingpopups", "blur"],
    disabled_plugins=["fade", "glide", "squash"],
    plugin_configs={
        "Effect-Scale": {
            "Duration": 300,
            "InScale": 0.70,
        },
        "Effect-Wobblywindows": {
            "Drag": 80,
            "Stiffness": 15,
        },
    },
    notes=["Playful bouncing spring physics when moving and opening windows."],
)

PRESETS: dict[str, MotionPreset] = {
    "denial": DENIAL_PRESET,
    "denial-vivid": DENIAL_VIVID_PRESET,
    "glide": GLIDE_PRESET,
    "snappy": SNAPPY_PRESET,
    "spring-wobbly": SPRING_WOBBLY_PRESET,
}
