"""krice 内置 KWin 窗口流体动效预设方案库。"""

from krice.presets import MotionPreset
from krice.presets.denial import DENIAL_PRESET, DENIAL_VIVID_PRESET

GLIDE_PRESET = MotionPreset(
    name="glide",
    description="物理滑翔动效（带有轻微倾角的平滑方向性滑动）",
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
    notes=["窗口如实体纸张般快速滑入，带有微小倾角与灵敏响应。"],
)

MAGIC_LAMP_PRESET = MotionPreset(
    name="magic-lamp",
    description="经典 macOS 神灯波浪卷轴最小化与恢复动效",
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
    notes=["最小化和恢复至任务栏图标时呈现优美的神灯弧线折叠波浪。"],
)

SNAPPY_PRESET = MotionPreset(
    name="snappy",
    description="高刷电竞 / 极速响应流体动效（即时反馈）",
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
    notes=["极速 90ms 缩放响应，带来零延迟的即时操作反馈。"],
)

SPRING_WOBBLY_PRESET = MotionPreset(
    name="spring-wobbly",
    description="触觉弹性物理动效（带有轻微果冻弹簧回弹与流体缩放）",
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
    notes=["移动和打开窗口时带有自然的果冻弹簧物理回弹质感。"],
)

PRESETS: dict[str, MotionPreset] = {
    "denial": DENIAL_PRESET,
    "denial-vivid": DENIAL_VIVID_PRESET,
    "glide": GLIDE_PRESET,
    "magic-lamp": MAGIC_LAMP_PRESET,
    "snappy": SNAPPY_PRESET,
    "spring-wobbly": SPRING_WOBBLY_PRESET,
}
