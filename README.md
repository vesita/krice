"""# krice (KDE Plasma 6 & Terminal Rice Toolkit)

**krice** 是专为 **CachyOS / Arch Linux + KDE Plasma 6** 设计的全维度桌面美化（Rice）、终端全端配色同步、物理动效调优与跨设备配置打包工具箱。

---

## 🌟 核心能力

1. **🎨 视觉主题全链路编排 (`krice theme`)**：
   - **全面覆盖 KDE Plasma 6 视觉要素**：全局主题（Look & Feel）、配色方案（Color Schemes）、Plasma 桌面样式（面板与任务栏）、Qt6 部件引擎（Breeze / Kvantum / Fusion / Lightly）、Kvantum SVG 主题、Klassy 窗口圆角与毛玻璃边框、图标（Icons）、光标（Cursors）、字体设置（Fonts）、开机动效（Splash）与 GTK 3/4 样式暗色偏好同步。
   - **动态调色板提炼**：实时提取当前 KDE 配色方案的色彩模型（背景、前景色、强调色、选区高亮色），并支持一键将 KDE 配色反向映射至终端。

2. **💻 终端与 Shell 全生态配色同步 (`krice terminal`)**：
   - **主流终端全覆盖**：KDE 原生 Konsole、Alacritty、Kitty、Ghostty、Foot、WezTerm。
   - **命令行工具联动**：自动生成与调色板匹配的 **Starship** 现代化胶囊提示符（Pill Powerline）以及 **Fastfetch** 系统看板。
   - **双向联动**：支持应用内置预设（Nord、Catppuccin、Tokyo Night、Dracula、Gruvbox、Rosé Pine、Orchis 等），或使用 `krice terminal sync` 动态提取当前 KDE 配色一键注入全部终端。

3. **⚡ Denial-Style 物理流体动效 (`krice motion`)**：
   - 一键注入类似 `denialwm/denial`（Flutter EaseOutCubic / Spring）的窗口开关平滑缩放动效。
   - 内置动效预设：`denial`（流体缩放）、`denial-vivid`（深层动量放大）、`glide`（拟物滑翔）、`snappy`（高刷竞技）、`spring-wobbly`（弹性果冻）。
   - 自动消除 KWin 动效冲突（屏蔽原生生硬的 Fade，激活 Scale + Morphing Popups）。

4. **📦 跨电脑一键打包与无损还原 (`krice snapshot`)**：
   - 自动打包 KDE 核心配置文件（`kwinrc`、`kdeglobals`、`kcminputrc`、`plasmarc`、`ksplashrc`、小部件布局、Klassy、Kvantum、GTK、全部终端配置、Starship、Fastfetch、Fcitx5 等）为单一便携包（`.pmz`）。
   - 跨机器还原时支持自动安全备份（`--backup`）、差异预检（`--dry-run`）与 D-Bus KWin 热重载。

5. **🛠️ 桌面状态与工具链诊断 (`krice status` / `krice check-deps`)**：
   - 实时诊断 Wayland 会话、KWin 动效因子、部件样式引擎、已安装终端、毛玻璃、窗口装饰库。
   - 针对 CachyOS / Arch 自动检测并提供 `klassy-qt6`、`kvantum-qt6`、`starship`、`fastfetch` 等工具的一键安装指令。

---

## 🚀 常用指令速查

在项目根目录下通过 `uv run` 即可直接使用：

### 1. 桌面与终端状态概览
```bash
uv run krice status
uv run krice check-deps
```

### 2. 整合式桌面风格切换 (KDE + 终端 + 动效 一键同步)
```bash
# 查看所有整合式风格预设 (Nord, Catppuccin, Tokyo Night, Dracula, Gruvbox...)
uv run krice theme list

# 一键应用 CachyOS Nord 暗色风格 (KDE + 终端 + Starship + Fastfetch + Denial动效)
uv run krice theme apply cachy-nord

# 应用 Catppuccin Mocha 风格
uv run krice theme apply catppuccin-mocha

# 仅应用 KDE 桌面样式，跳过终端
uv run krice theme apply tokyo-night --no-terminal
```

### 3. 独立管理终端与 Shell 提示符
```bash
# 查看支持的调色板及当前系统检测到的终端
uv run krice terminal list

# 一键同步所有终端（Konsole, Alacritty, Kitty, Ghostty, Foot, WezTerm, Starship, Fastfetch）
uv run krice terminal apply catppuccin-mocha

# 动态提取当前 KDE 配色并直接注入到所有终端
uv run krice terminal sync

# 针对单一终端独立设置
uv run krice terminal set-alacritty cachy-nord
uv run krice terminal set-konsole dracula
uv run krice terminal set-kitty tokyo-night
uv run krice terminal set-starship gruvbox-dark

# 查看或导出特定调色板的 16 色 ANSI 色卡
uv run krice terminal export-palette cachy-nord
```

### 4. 细分管理 KDE 桌面视觉元素
```bash
# 配色方案 (Color Schemes)
uv run krice theme colors
uv run krice theme set-color CachyOSNord

# Qt6 部件样式引擎 (Widget Style Engines)
uv run krice theme widget-styles
uv run krice theme set-widget-style kvantum

# Kvantum SVG 主题
uv run krice theme kvantum-themes
uv run krice theme set-kvantum Nordic

# Plasma 桌面样式 (面板/启动器/系统托盘背景)
uv run krice theme plasma-style
uv run krice theme set-plasma-style Nordic

# 窗口装饰与 Klassy 圆角微调
uv run krice theme decorations
uv run krice theme set-decoration klassy --radius 12 --blur

# 全局外观包 (Global Look & Feel)
uv run krice theme global
uv run krice theme set-global Edna-Light

# 鼠标指针与图标
uv run krice theme cursors
uv run krice theme set-cursor Breeze_Dark --size 24
uv run krice theme icons
uv run krice theme set-icon Papirus-Dark

# 字体与开机动效
uv run krice theme fonts
uv run krice theme splash
uv run krice theme set-splash org.kde.breeze.desktop

# GTK 3/4 主题与暗色偏好同步
uv run krice theme gtk
uv run krice theme sync-gtk --dark

# 提取当前 KDE 调色板 HEX 摘要
uv run krice theme palette

# 壁纸切换
uv run krice theme set-wallpaper /path/to/wallpaper.png
```

### 5. 动效单独微调
```bash
# 查看动效预设
uv run krice motion list

# 启用 Denial 风格流体缩放
uv run krice motion apply denial

# 微调动画速度因数 (0.85x 为舒适流体，0.30x 为极速)
uv run krice motion tune --factor 0.85 --effect scale
```

### 6. 跨电脑配置导出与导入
```bash
# 1. 在当前电脑保存完整桌面及终端快照
uv run krice snapshot save --name my-cachy-kde

# 2. 查看快照内容清单
uv run krice snapshot info snapshots/my-cachy-kde.pmz

# 3. 在另一台 CachyOS 电脑上导入并一键应用
uv run krice snapshot load snapshots/my-cachy-kde.pmz
```

---

## 📁 项目目录结构

```
krice/
├── pyproject.toml              # 项目依赖声明 (uv 管理)
├── README.md                   # 完整使用文档
├── src/krice/
│   ├── cli.py                  # Rich + Typer 交互控制台
│   ├── inspector.py            # KDE & 终端环境状态诊断器
│   ├── installer.py            # 工具链与终端依赖检测器
│   ├── kwin_ctl.py             # KWin D-Bus & kwriteconfig6 控制器
│   ├── theme_ctl.py            # KDE 全维度主题与部件控制器
│   ├── terminal_ctl.py         # 终端 (Konsole/Alacritty/Kitty/Ghostty/Foot/WezTerm) 控制器
│   ├── snapshot.py             # 配置归档打包与跨机器还原引擎
│   └── presets/
│       ├── builtin_presets.py  # 动效预设库 (denial, glide, snappy...)
│       ├── terminal_palettes.py# 16 色 ANSI 终端调色板库
│       ├── prompt_presets.py   # Starship & Fastfetch 模板生成器
│       └── theme_presets.py    # 整合式 Rice 桌面预设库
├── tests/                      # Pytest 自动化测试套件
└── snapshots/                  # 导出的 .pmz 配置文件
```
"""
