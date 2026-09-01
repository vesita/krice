"""Denial-inspired Flutter fluid motion presets for KWin."""

from krice.presets import MotionPreset

# DenialWM style: Flutter EaseOutCubic/Spring scaling, clean deceleration, smooth dialog morphing
DENIAL_PRESET = MotionPreset(
    name="denial",
    description="DenialWM / Flutter-like fluid scale animation (responsive 0.80x speed with smooth Ease-Out deceleration)",
    animation_factor=0.80,
    enabled_plugins=[
        "scale",              # Primary window open/close scale effect
        "morphingpopups",     # Smooth popup transitions
        "blur",               # Background blur for translucent windows
    ],
    disabled_plugins=[
        "fade",               # Disable plain fade to avoid conflict with scale
        "glide",              # Disable glide to prioritize isotropic scale
        "squash",
        "magiclamp",
    ],
    plugin_configs={
        "Effect-Scale": {
            "ScaleType": 0,    # 0 = Window center, 1 = Cursor position
            "Duration": 240,   # ~240ms duration for responsive curve progression
            "InScale": 0.85,   # Clean subtle zoom from 85% scale to 100%
            "OutScale": 0.85,
        },
        "Effect-Blur": {
            "BlurStrength": 10,
            "NoiseStrength": 0,
        },
    },
    notes=[
        "Scales windows smoothly from 85% -> 100% with Ease-Out curve.",
        "Calibrated to 0.80x factor for responsive, lag-free opening on 60Hz-240Hz screens.",
        "Disables default fade-in to prevent choppy double animations.",
    ],
)

# Denial Vivid: Prominent zoom-in with fluid deceleration
DENIAL_VIVID_PRESET = MotionPreset(
    name="denial-vivid",
    description="Vivid Denial fluid motion (pronounced zoom from 70% scale with 0.85x fluid speed)",
    animation_factor=0.85,
    enabled_plugins=[
        "scale",
        "morphingpopups",
        "blur",
    ],
    disabled_plugins=[
        "fade",
        "glide",
        "squash",
        "magiclamp",
    ],
    plugin_configs={
        "Effect-Scale": {
            "ScaleType": 0,
            "Duration": 260,
            "InScale": 0.70,   # Pronounced zoom from 70% scale
            "OutScale": 0.80,
        },
        "Effect-Blur": {
            "BlurStrength": 12,
            "NoiseStrength": 0,
        },
    },
    notes=[
        "Pronounced zoom-in from 70% window size for distinctive fluid momentum.",
    ],
)
