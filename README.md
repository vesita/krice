# krice (KDE Plasma 6 & Terminal Rice Toolkit)

**krice** 是专为 **CachyOS / Arch Linux + KDE Plasma 6 (Wayland)** 量身定制的全维度桌面美化（Rice）、终端全生态调色联动、物理流体动效调优与跨设备配置无损迁移工具箱。

---

## 🌟 核心能力

1. **🎨 桌面视觉主题全链路编排 (`krice theme`)**：
   - **全面覆盖 KDE Plasma 6 核心要素**：全局外观（Look & Feel）、配色方案（Color Schemes）、Plasma 桌面面板样式（Panel/Bar）、Qt6 控件引擎（Breeze / Kvantum / Fusion）、Kvantum SVG 主题、窗口装饰（org.kde.breeze 亚像素精准渲染 / Klassy）、图标（Icons）、鼠标指针（Cursors）、系统字体（Fonts）、开机欢迎屏幕（Splash）与 GTK 3/4 样式统一联动。
   - **智能调色板提取**：实时从当前 KDE 配色中提取色彩模型（背景色、前景色、强调蓝、选区高亮色），并支持一键反向注入多终端。

2. **💻 Kitty 终端与 Shell 提示符全生态联动 (`krice terminal`)**：
   - **Kitty 终端一等公民支持**：包含 GPU 加速渲染、顶部斜切 Powerline Tab（Slanted Tabs）、`0.78` 浅亮色半透明磨砂亚克力毛玻璃（Frosted Acrylic Blur）、天然内边距与实时透明度调节快捷键（`Ctrl+Shift+O` / `Ctrl+Shift+U`）。
   - **精准字体排版**：明确指定官方 `MesloLGS Nerd Font`（11.5pt），彻底根除因 `monospace` 别名解析至中日韩 CJK 字体引起的英文字符双倍宽字距/稀疏 bug。
   - **Shell 现代化工作目录胶囊提示符**：自动生成与配色匹配的 **Starship** 现代化工作目录胶囊（Directory Pill）、Git 状态与执行耗时指示器，以及 **Fastfetch** 系统硬件看板。

3. **⚡ 物理流体与高刷动效调优 (`krice motion`)**：
   - **消除 60Hz 帧步进滞后感**：动效缩放因子校准至 `0.50x`，配合 150ms 弹簧缩放与 `92% -> 100%` Ease-Out 弹出曲线。
   - **非激活窗口微暗（Dim Inactive）**：开启 10% 柔和失焦暗化，窗口层级与焦点切换清晰顺滑。
   - **缩略图网格切换器（Thumbnail Grid）**：开启现代缩略图网格任务切换器，替代传统卡片。
   - **硬件级背景毛玻璃**：KWin 合成器模糊强度（BlurStrength）调优至 `12`，亚克力质感深邃通透。

4. **📦 跨机器配置打包、无损还原与依赖自愈 (`krice snapshot` / `krice install`)**：
   - **精准打包范围**：聚焦于 **Orchis 主题套件、KWin 动效与毛玻璃、Kitty 终端、Starship 提示符与 Fish/Zsh/Bash Shell 配置、本地字体与指针图标**，生成单一便携快照（`.pmz`）。
   - **内嵌智能安装器与依赖自愈**：目标机器若缺少 Kitty、Starship、MesloLGS Nerd Font 或 Shell Hook，运行 `krice install --all` 或 `krice snapshot load --install-deps` 即可全自动一键补齐所有软件包、字体并自动注入 Shell 工作目录提示符！

5. **🏥 系统健康诊断与工具链审计 (`krice doctor` / `krice status`)**：
   - 实时诊断 Wayland 会话、KWin 动效参数、已安装终端、字体有效性与三大 Shell（Fish / Zsh / Bash）的前缀提示符挂钩状态。

---

## 🚀 常用指令速查

在项目根目录下通过 `uv run` 即可直接执行：

### 1. 系统诊断与环境检查
```bash
# 查看当前 KDE 桌面主题、动效与终端集成总览看板
uv run krice status

# 全面诊断工具链依赖、Nerd Fonts 字体与 Shell 挂钩健康状态
uv run krice doctor
```

### 2. 内嵌安装器（补齐依赖、字体与 Shell 提示符）
```bash
# 一键自动安装所有缺失软件包、下载 MesloLGS 字体并配置 Shell 提示符
uv run krice install --all

# 仅在 fish、zsh、bash 中注入 Starship 工作目录前缀提示符
uv run krice install --hooks

# 仅下载并安装 MesloLGS Nerd Font 官方全套字重至 ~/.local/share/fonts/
uv run krice install --fonts
```

### 3. 全局桌面方案一键切换 (KDE + Kitty + Shell + 动效)
```bash
# 查看所有预设的全局美化方案 (cachy-nord, catppuccin-latte, tokyo-night...)
uv run krice theme list

# 一键应用 CachyOS Nord 风格 (全套 KDE + Kitty + Starship + Fastfetch + 动效)
uv run krice theme apply cachy-nord

# 应用 Catppuccin 浅色奶油风格
uv run krice theme apply catppuccin-latte
```

### 4. Kitty 终端与 Shell 提示符管理
```bash
# 查看所有 16 色 ANSI 调色板
uv run krice terminal list

# 从当前 KDE 桌面活动配色中智能提取并一键同步所有终端
uv run krice terminal sync

# 单独为 Kitty 应用浅色调色板（保持半透明磨砂毛玻璃与斜切 Tab）
uv run krice terminal set-kitty nord-light
uv run krice terminal set-kitty catppuccin-latte

# 单独为 Starship 提示符应用配色
uv run krice terminal set-starship nord-light
```

#### 💡 Kitty 常用快捷键：
- **`Ctrl + Shift + T`**：新建 Tab
- **`Ctrl + Shift + W`**：关闭当前 Tab
- **`Ctrl + Shift + Left / Right`**：左右切换 Tab
- **`Ctrl + Shift + 1 ~ 5`**：快速直达指定 Tab
- **`Ctrl + Shift + Enter`**：垂直分屏（Vertical Split）
- **`Ctrl + Shift + D`**：水平分屏（Horizontal Split）
- **`Ctrl + Shift + H / J / K / L`**：分屏方向导航
- **`Ctrl + Shift + O`**：**实时减小不透明度（更透亮 / 玻璃感更强）**
- **`Ctrl + Shift + U`**：**实时增大不透明度（字更实）**
- **`Ctrl + Shift + Delete`**：恢复默认推荐透明度 (`0.78`)

### 5. 动效管理与调优
```bash
# 查看动效预设方案
uv run krice motion list

# 启用 Denial 风格流体物理缩放
uv run krice motion apply denial

# 设置动画缩放因子 (0.50x 为高刷极速流体，1.0x 为默认速度)
uv run krice motion set-factor 0.50

# 设置 Alt+Tab 任务切换器为缩略图网格
uv run krice motion set-switcher thumbnail_grid
```

### 6. 跨电脑配置导出与无损还原
```bash
# 1. 在当前电脑打包保存完整的 Rice 资产快照 (.pmz)
uv run krice snapshot save --name cachy-orchis-rice

# 2. 查看快照归档包含的文件与元数据
uv run krice snapshot info snapshots/cachy-orchis-rice.pmz

# 3. 在另一台电脑上一键还原并自动补齐依赖与 Shell 提示符
uv run krice snapshot load snapshots/cachy-orchis-rice.pmz --install-deps
```

---

## 📁 项目目录结构

```
krice/
├── pyproject.toml              # 项目依赖声明 (uv 管理)
├── README.md                   # 完整中文使用指南
├── src/krice/
│   ├── cli.py                  # Rich + Typer 交互控制台与中文界面
│   ├── inspector.py            # KDE & 终端环境状态诊断器
│   ├── installer.py            # 内嵌智能安装器、依赖求解器与 Shell Hook 注入器
│   ├── kwin_ctl.py             # KWin D-Bus & kwriteconfig6 合成器控制器
│   ├── theme_ctl.py            # KDE 全维度主题与部件控制器
│   ├── terminal_ctl.py         # Kitty, Alacritty, Konsole 终端与 Starship 控制器
│   ├── snapshot.py             # 配置归档打包与跨机器还原引擎
│   └── presets/
│       ├── builtin_presets.py  # 动效预设库 (denial, glide, snappy...)
│       ├── terminal_palettes.py# 16 色 ANSI 终端高清调色板
│       ├── prompt_presets.py   # Starship 工作目录胶囊与 Fastfetch 模板
│       └── theme_presets.py    # 整合式 Rice 桌面预设库
├── tests/                      # Pytest 自动化测试套件
└── snapshots/                  # 便携式 .pmz 快照归档
```
