"""DenialWM / Flutter 灵动物理流体动效预设方案。"""

from krice.presets import MotionPreset

# DenialWM 风格：灵动极速 Flutter EaseOut 缩放 (0.50x 缩放因子, 150ms 持续时间, 92%->100% 微弹), Squash 挤压折叠与顺滑失焦暗化
DENIAL_PRESET = MotionPreset(
    name="denial",
    description="DenialWM / Flutter 灵动流体缩放动效（0.50x 极速, 92%->100% 微弹, Squash 任务栏折叠）",
    animation_factor=0.50,
    enabled_plugins=[
        "scale",              # 核心窗口打开/关闭缩放动效
        "squash",             # 任务栏图标挤压/展开最小化动效
        "morphingpopups",     # 弹出菜单与气泡平滑形变
        "blur",               # 半透明窗口背景毛玻璃模糊
        "slidingpopups",      # 通知气泡与 OSD 平滑滑动
        "diminactive",        # 窗口焦点切换时非激活窗口 10% 柔和失焦暗化
    ],
    disabled_plugins=[
        "fade",               # 禁用生硬的淡入淡出，避免与缩放动效冲突
        "glide",              # 禁用滑动以优先保证等比例流体缩放
        "magiclamp",
    ],
    plugin_configs={
        "Effect-Scale": {
            "ScaleType": 0,    # 0 = 窗口中心缩放, 1 = 鼠标位置缩放
            "Duration": 150,   # 150ms 紧凑持续时间，消除 60Hz 屏幕帧步进拖沓感
            "InScale": 0.92,   # 92% -> 100% 微弹弹出，绝无拖泥带水之感
            "OutScale": 0.92,
        },
        "Effect-Blur": {
            "BlurStrength": 12, # 12 级深度亚克力磨砂高斯模糊
            "NoiseStrength": 0,
        },
        "Effect-Diminactive": {
            "DimStrength": 10,  # 非激活窗口 10% 柔和微暗，焦点切换清晰自然
        },
    },
    notes=[
        "精准校准 150ms / 0.50x 极速因子，彻底消除 60Hz 显示器刷新率下的帧步进延迟感。",
        "92% -> 100% Ease-Out 微缩放弹出曲线，提供如同 iOS / Flutter 的灵动画布质感。",
        "Squash 挤压折叠动效在最小化与恢复时顺滑收缩至任务栏图标。",
        "DimInactive 在多窗口鼠标点击切换焦点时提供平滑的视觉过渡反馈。",
    ],
)

# Denial Vivid：更具视觉张力的深层流体缩放
DENIAL_VIVID_PRESET = MotionPreset(
    name="denial-vivid",
    description="Vivid 鲜活流体缩放（80% 深层放大，0.60x 灵动速度）",
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
        "从 80% 窗口尺寸展开的深层流体放大动效，搭配 Squash 任务栏折叠与焦点微暗。",
    ],
)
