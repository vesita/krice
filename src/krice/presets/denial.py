"""Denial-inspired Flutter fluid motion presets for KWin."""

from krice.presets import MotionPreset

# DenialWM style: Flutter EaseOutCubic/Spring scaling, clean deceleration, smooth dialog morphing
DENIAL_PRESET = MotionPreset(
    name="denial",
    description="DenialWM / Flutter-like fluid scale animation (visible 65% -> 100% Ease-Out deceleration)",
    animation_factor=1.15,
    enabled_plugins=[
        "scale",              # Primary window open/close scale effect
        "morphingpopups",     # Smooth popup transitions
        "blur",               # Background blur for translucent windows
        "slidingpopups",      # Fluid notifications & OSD
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
            "Duration": 320,   # ~320ms duration for visible curve progression
            "InScale": 0.65,   # Visibly springs from 65% scale to 100%
            "OutScale": 0.75,
        },
        "Effect-Blur": {
            "BlurStrength": 12,
            "NoiseStrength": 0,
        },
    },
    notes=[
        "Scales windows smoothly from 65% -> 100% with Ease-Out curve.",
        "Disables default fade-in to prevent choppy double animations.",
        "AnimationDurationFactor set to 1.15x for clearly noticeable momentum.",
    ],
)

# Denial Vivid: Ultra-prominent zoom-in from 50% scale
DENIAL_VIVID_PRESET = MotionPreset(
    name="denial-vivid",
    description="Ultra-vivid Denial fluid motion (deep 50% -> 100% zoom with pronounced momentum)",
    animation_factor=1.30,
    enabled_plugins=[
        "scale",
        "morphingpopups",
        "blur",
        "slidingpopups",
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
            "Duration": 380,
            "InScale": 0.50,   # Deep zoom from 50% scale
            "OutScale": 0.65,
        },
        "Effect-Blur": {
            "BlurStrength": 14,
            "NoiseStrength": 0,
        },
    },
    notes=[
        "Deep zoom-in from 50% window size for unmistakable fluid motion perception.",
    ],
)
