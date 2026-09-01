"""Catalog of built-in motion presets for krice."""

from krice.presets import MotionPreset
from krice.presets.denial import DENIAL_PRESET, DENIAL_VIVID_PRESET

GLIDE_PRESET = MotionPreset(
    name="glide",
    description="Physical sheet/glide motion (smooth directional sliding with angular tilt and Squash minimize)",
    animation_factor=0.85,
    enabled_plugins=["glide", "squash", "morphingpopups", "blur"],
    disabled_plugins=["scale", "fade", "magiclamp"],
    plugin_configs={
        "Effect-Glide": {
            "InAngle": -3,
            "OutAngle": 3,
            "InDistance": 12,
            "OutDistance": 12,
            "Duration": 220,
        }
    },
    notes=["Window slides in like a physical sheet of paper with subtle angle tilt and Squash minimize."],
)

MAGIC_LAMP_PRESET = MotionPreset(
    name="magic-lamp",
    description="Genie / Magic Lamp wave animation (curved fluid flow into taskbar icon on minimize/restore)",
    animation_factor=0.80,
    enabled_plugins=["scale", "magiclamp", "morphingpopups", "blur"],
    disabled_plugins=["fade", "glide", "squash"],
    plugin_configs={
        "Effect-Scale": {
            "Duration": 240,
            "InScale": 0.85,
            "OutScale": 0.85,
        },
        "Effect-MagicLamp": {
            "AnimationDuration": 260,
        },
    },
    notes=["Curved genie wave motion into taskbar icon when minimizing and restoring windows."],
)

SNAPPY_PRESET = MotionPreset(
    name="snappy",
    description="Competitive / ultra-fast responsive animations (120Hz/240Hz optimized)",
    animation_factor=0.35,
    enabled_plugins=["scale", "squash", "morphingpopups"],
    disabled_plugins=["fade", "glide", "magiclamp", "wobblywindows"],
    plugin_configs={
        "Effect-Scale": {
            "Duration": 120,
            "InScale": 0.95,
        }
    },
    notes=["Minimal latency with fast squash for multi-tasking on high refresh rate displays."],
)

SPRING_WOBBLY_PRESET = MotionPreset(
    name="spring-wobbly",
    description="Tactile organic physics with subtle wobbly spring bounce, scale and Squash minimize",
    animation_factor=1.00,
    enabled_plugins=["scale", "squash", "wobblywindows", "morphingpopups", "blur"],
    disabled_plugins=["fade", "glide", "magiclamp"],
    plugin_configs={
        "Effect-Scale": {
            "Duration": 280,
            "InScale": 0.75,
        },
        "Effect-Wobblywindows": {
            "Drag": 80,
            "Stiffness": 15,
        },
    },
    notes=["Playful bouncing spring physics when moving, opening and minimizing windows."],
)

PRESETS: dict[str, MotionPreset] = {
    "denial": DENIAL_PRESET,
    "denial-vivid": DENIAL_VIVID_PRESET,
    "glide": GLIDE_PRESET,
    "magic-lamp": MAGIC_LAMP_PRESET,
    "snappy": SNAPPY_PRESET,
    "spring-wobbly": SPRING_WOBBLY_PRESET,
}
