"""Catalog of built-in motion presets for krice."""

from krice.presets import MotionPreset
from krice.presets.denial import DENIAL_PRESET, DENIAL_VIVID_PRESET

GLIDE_PRESET = MotionPreset(
    name="glide",
    description="Physical sheet/glide motion (smooth directional sliding with angular tilt)",
    animation_factor=0.60,
    enabled_plugins=["glide", "squash", "morphingpopups", "blur", "slidingpopups", "diminactive"],
    disabled_plugins=["scale", "fade", "magiclamp"],
    plugin_configs={
        "Effect-Glide": {
            "InAngle": -4,
            "OutAngle": 4,
            "InDistance": 10,
            "OutDistance": 10,
            "Duration": 160,
        },
        "Effect-Diminactive": {
            "DimStrength": 10,
        },
    },
    notes=["Window slides in like a physical sheet of paper with subtle angle and quick response."],
)

MAGIC_LAMP_PRESET = MotionPreset(
    name="magic-lamp",
    description="Classic macOS Genie / Magic Lamp wave animation on minimize & restore",
    animation_factor=0.65,
    enabled_plugins=["scale", "magiclamp", "morphingpopups", "blur", "slidingpopups", "diminactive"],
    disabled_plugins=["fade", "glide", "squash"],
    plugin_configs={
        "Effect-Scale": {
            "Duration": 160,
            "InScale": 0.90,
            "OutScale": 0.90,
        },
        "Effect-Magiclamp": {
            "AnimationDuration": 200,
        },
        "Effect-Diminactive": {
            "DimStrength": 10,
        },
    },
    notes=["Classic genie wave curve on minimize and restore to taskbar icon."],
)

SNAPPY_PRESET = MotionPreset(
    name="snappy",
    description="Competitive / ultra-fast responsive animations (instant feedback)",
    animation_factor=0.30,
    enabled_plugins=["scale", "squash", "morphingpopups", "slidingpopups"],
    disabled_plugins=["fade", "glide", "magiclamp", "wobblywindows", "diminactive"],
    plugin_configs={
        "Effect-Scale": {
            "ScaleType": 0,
            "Duration": 90,
            "InScale": 0.95,
            "OutScale": 0.95,
        }
    },
    notes=["Blazing fast 90ms scale response for instantaneous UI reactivity."],
)

SPRING_WOBBLY_PRESET = MotionPreset(
    name="spring-wobbly",
    description="Tactile organic physics with subtle wobbly spring bounce and scale",
    animation_factor=0.75,
    enabled_plugins=["scale", "wobblywindows", "squash", "morphingpopups", "blur", "slidingpopups", "diminactive"],
    disabled_plugins=["fade", "glide", "magiclamp"],
    plugin_configs={
        "Effect-Scale": {
            "Duration": 180,
            "InScale": 0.85,
        },
        "Effect-Wobblywindows": {
            "Drag": 85,
            "Stiffness": 20,
        },
        "Effect-Diminactive": {
            "DimStrength": 10,
        },
    },
    notes=["Playful bouncing spring physics when moving and opening windows."],
)

PRESETS: dict[str, MotionPreset] = {
    "denial": DENIAL_PRESET,
    "denial-vivid": DENIAL_VIVID_PRESET,
    "glide": GLIDE_PRESET,
    "magic-lamp": MAGIC_LAMP_PRESET,
    "snappy": SNAPPY_PRESET,
    "spring-wobbly": SPRING_WOBBLY_PRESET,
}
