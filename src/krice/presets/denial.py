"""Denial-inspired Flutter fluid motion presets for KWin."""

from krice.presets import MotionPreset

# DenialWM style: Snappy Flutter EaseOut scaling (0.50x, 150ms, 92%->100%), Squash minimize & Smooth window focus switching
DENIAL_PRESET = MotionPreset(
    name="denial",
    description="DenialWM / Flutter-like fluid scale animation (snappy 0.50x speed, 92%->100% micro-pop, Squash minimize)",
    animation_factor=0.50,
    enabled_plugins=[
        "scale",              # Primary window open/close scale effect
        "squash",             # Fluid minimize / restore to taskbar icon
        "morphingpopups",     # Smooth popup transitions
        "blur",               # Background blur for translucent windows
        "slidingpopups",      # Smooth OSD / notifications
        "diminactive",        # Subtle background dimming on window focus switch
    ],
    disabled_plugins=[
        "fade",               # Disable plain fade to avoid conflict with scale
        "glide",              # Disable glide to prioritize isotropic scale
        "magiclamp",
    ],
    plugin_configs={
        "Effect-Scale": {
            "ScaleType": 0,    # 0 = Window center, 1 = Cursor position
            "Duration": 150,   # 150ms crisp duration for instant fluid pop without 60Hz stepping
            "InScale": 0.92,   # Subtle 92% -> 100% pop for zero visual drag
            "OutScale": 0.92,
        },
        "Effect-Blur": {
            "BlurStrength": 10,
            "NoiseStrength": 0,
        },
        "Effect-Diminactive": {
            "DimStrength": 10,  # 10% subtle dimming on inactive windows for clear switching feedback
        },
    },
    notes=[
        "Crisp 150ms / 0.50x speed calibration eliminating 60Hz display frame stepping.",
        "Subtle 92% -> 100% Ease-Out pop with zero drag or sluggishness.",
        "Squash animation smoothly collapses/expands windows to/from taskbar icons.",
        "DimInactive provides smooth visual focus transition when clicking between open windows.",
    ],
)

# Denial Vivid: Pronounced zoom with fluid snappy speed
DENIAL_VIVID_PRESET = MotionPreset(
    name="denial-vivid",
    description="Vivid Denial fluid motion (pronounced zoom from 80% scale with 0.60x snappy speed)",
    animation_factor=0.60,
    enabled_plugins=[
        "scale",
        "squash",
        "morphingpopups",
        "blur",
        "slidingpopups",
        "diminactive",
    ],
    disabled_plugins=[
        "fade",
        "glide",
        "magiclamp",
    ],
    plugin_configs={
        "Effect-Scale": {
            "ScaleType": 0,
            "Duration": 180,
            "InScale": 0.80,
            "OutScale": 0.85,
        },
        "Effect-Blur": {
            "BlurStrength": 12,
            "NoiseStrength": 0,
        },
        "Effect-Diminactive": {
            "DimStrength": 12,
        },
    },
    notes=[
        "Pronounced zoom-in from 80% window size with fluid Squash minimize and focus transitions.",
    ],
)
