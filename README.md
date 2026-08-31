# krice (KDE Plasma 6 Rice & Motion Toolkit)

**krice** 是专为 **CachyOS / Arch Linux + KDE Plasma 6** 设计的一站式桌面美化（Rice）、物理动效调优与跨设备配置同步工具箱。

---

## 🌟 核心能力

1. **🎨 视觉主题一站式编排 (`krice theme`)**：
   - 整合全局主题（Global Theme）、配色方案（Color Schemes）、光标（Cursors）、图标（Icons）、窗口装饰与壁纸。
   - 内置统一风格预设：`cachy-nord`、`edna-light`、`emerald-dark`、`breeze-twilight`。

2. **⚡ Denial-Style 物理流体动效 (`krice motion`)**：
   - 一键注入类似 `denialwm/denial`（Flutter EaseOutCubic / Spring）的窗口开关平滑缩放动效。
   - 内置动效预设：`denial`（流体缩放）、`glide`（拟物滑翔）、`snappy`（高刷竞技）、`spring-wobbly`（弹性果冻）。
   - 自动消除 KWin 动效冲突（屏蔽原生生硬的 Fade，激活 Scale + Morphing Popups）。

3. **📦 跨电脑一键打包与无损还原 (`krice snapshot`)**：
   - 自动打包 KDE 核心配置文件（`kwinrc`、`kdeglobals`、`kcminputrc`、`kglobalshortcutsrc`、小部件布局、Klassy 与 Kvantum 配置）为单一便携包（`.pmz`）。
   - 跨机器还原时支持自动安全备份（`--backup`）、差异预检（`--dry-run`）与 D-Bus KWin 热重载。

4. **🛠️ 桌面状态与工具链诊断 (`krice status` / `krice check-deps`)**：
   - 实时诊断 Wayland 会话、KWin 动效因子、毛玻璃、窗口装饰库。
   - 针对 CachyOS 自动检测 `klassy-qt6`、`kvantum-qt6`、`kwin-effect-forceblur-git` 等增强工具。

---

## 🚀 常用指令速查

在项目根目录下通过 `uv run` 即可直接使用：

### 1. 桌面状态概览
```bash
cd /home/vesita/coding/my/krice
uv run krice status
uv run krice check-deps
```

### 2. 视觉主题切换
```bash
# 查看所有整合式桌面风格预设
uv run krice theme list

# 一键应用 CachyOS Nord 暗色风格 (含配套动效)
uv run krice theme apply cachy-nord

# 独立管理细分元素
uv run krice theme colors                # 列出所有已安装配色方案
uv run krice theme set-color CachyOSNord # 快速切换配色
uv run krice theme global                # 查看全局主题包
uv run krice theme set-global Edna-Light # 切换全局主题
uv run krice theme cursors               # 查看鼠标指针
uv run krice theme set-cursor Breeze_Dark --size 24
uv run krice theme set-wallpaper /path/to/image.png
```

### 3. 动效单独微调
```bash
# 查看动效预设
uv run krice motion list

# 启用 Denial 风格流体缩放
uv run krice motion apply denial

# 微调动画速度因数 (0.85x 为舒适流体，0.30x 为极速)
uv run krice motion tune --factor 0.85 --effect scale
```

### 4. 跨电脑配置导出与导入
```bash
# 1. 在当前电脑保存完整桌面快照
uv run krice snapshot save my-cachy-kde

# 2. 查看快照内容清单
uv run krice snapshot info snapshots/my-cachy-kde.pmz

# 3. 在另一台 CachyOS 电脑上导入并一键应用
uv run krice snapshot load snapshots/my-cachy-kde.pmz
```

---

## 📁 项目目录结构

```
krice/
├── pyproject.toml         # 项目依赖声明 (uv 管理)
├── README.md              # 文档
├── src/krice/
│   ├── cli.py             # Rich + Typer 终端控制台
│   ├── inspector.py       # KDE 环境状态与引擎诊断
│   ├── installer.py       # CachyOS 依赖检测与安装指令
│   ├── kwin_ctl.py        # KWin D-Bus & kwriteconfig6 控制器
│   ├── theme_ctl.py       # 全局主题、配色、光标、图标、壁纸控制器
│   ├── snapshot.py        # 配置归档打包与还原引擎
│   └── presets/
│       ├── builtin_presets.py # 动效预设库 (denial, glide, snappy...)
│       └── theme_presets.py   # 完整 Rice 主题预设 (cachy-nord, edna-light...)
└── snapshots/             # 导出的 .pmz 配置文件
```
