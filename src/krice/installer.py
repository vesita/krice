"""krice 内嵌安装器、依赖求解器与 Shell 提示符 Hook 自动配置模块。"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class PackageStatus:
    name: str
    category: str
    description: str
    installed: bool
    install_command: str
    essential: bool = False


@dataclass
class ShellHookStatus:
    shell: str
    rc_file: Path
    hooked: bool
    hook_code: str


@dataclass
class DoctorReport:
    packages: List[PackageStatus] = field(default_factory=list)
    hooks: List[ShellHookStatus] = field(default_factory=list)
    fonts_ready: bool = False
    font_details: str = ""
    pkg_manager: str = "pacman"
    has_aur_helper: bool = False
    aur_helper: str = ""


class DependencyHelper:
    """智能依赖检测、系统包管理器安装与 Shell 提示符 Hook 注入器。"""

    def __init__(self, home_dir: Optional[Path] = None) -> None:
        self.home = home_dir or Path.home()
        self.config_dir = Path(os.environ.get("XDG_CONFIG_HOME", str(self.home / ".config")))
        self.data_dir = Path(os.environ.get("XDG_DATA_HOME", str(self.home / ".local" / "share")))
        self.fonts_dir = self.data_dir / "fonts"

    def detect_package_manager(self) -> Tuple[str, str, bool]:
        """检测系统可用的包管理器与 AUR 助手（paru / yay / pacman 等）。"""
        aur_helper = ""
        has_aur = False
        for helper in ["paru", "yay"]:
            if shutil.which(helper):
                aur_helper = helper
                has_aur = True
                break

        if shutil.which("pacman"):
            pkg_mgr = "pacman"
        elif shutil.which("dnf"):
            pkg_mgr = "dnf"
        elif shutil.which("apt"):
            pkg_mgr = "apt"
        elif shutil.which("zypper"):
            pkg_mgr = "zypper"
        else:
            pkg_mgr = "未知"

        return pkg_mgr, aur_helper, has_aur

    def check_font_installed(self) -> Tuple[bool, str]:
        """检查系统中是否已安装 MesloLGS Nerd Font 或兼容的 Nerd Font 字体。"""
        # 1. 通过 fc-list 查询 fontconfig 数据库
        if shutil.which("fc-list"):
            try:
                res = subprocess.run(
                    ["fc-list", ":", "family"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                output = res.stdout.lower()
                if "meslolgs nerd font" in output:
                    return True, "MesloLGS Nerd Font (已安装并生效)"
                if "nerd font" in output:
                    return True, "已检测到通用 Nerd Font 图标字体"
            except Exception:
                pass

        # 2. 检查用户本地字体目录
        if self.fonts_dir.exists():
            for f in self.fonts_dir.glob("*"):
                if "meslo" in f.name.lower() or "nerd" in f.name.lower():
                    return True, f"已找到本地字体: {f.name}"

        # 3. 检查系统全局字体目录
        for p in [Path("/usr/share/fonts"), Path("/usr/local/share/fonts")]:
            if p.exists():
                try:
                    for f in p.rglob("*"):
                        if "meslo" in f.name.lower():
                            return True, f"已找到系统全局字体: {f.name}"
                except Exception:
                    pass

        return False, "缺少 Nerd Font 字体 (Shell 目录胶囊与 Git 图标需要 MesloLGS NF)"

    def check_shell_hooks(self) -> List[ShellHookStatus]:
        """检查 fish, zsh, bash 是否已正确配置 Starship 提示符挂钩。"""
        hooks: List[ShellHookStatus] = []

        # 1. Fish
        fish_config = self.config_dir / "fish" / "config.fish"
        fish_confd = self.config_dir / "fish" / "conf.d" / "starship.fish"
        fish_hooked = False
        if fish_confd.exists() and "starship init fish" in fish_confd.read_text(encoding="utf-8", errors="ignore"):
            fish_hooked = True
        elif fish_config.exists() and "starship init fish" in fish_config.read_text(encoding="utf-8", errors="ignore"):
            fish_hooked = True

        hooks.append(
            ShellHookStatus(
                shell="fish",
                rc_file=fish_config,
                hooked=fish_hooked,
                hook_code="starship init fish | source",
            )
        )

        # 2. Zsh
        zshrc = self.home / ".zshrc"
        zsh_hooked = False
        if zshrc.exists() and "starship init zsh" in zshrc.read_text(encoding="utf-8", errors="ignore"):
            zsh_hooked = True

        hooks.append(
            ShellHookStatus(
                shell="zsh",
                rc_file=zshrc,
                hooked=zsh_hooked,
                hook_code='eval "$(starship init zsh)"',
            )
        )

        # 3. Bash
        bashrc = self.home / ".bashrc"
        bash_hooked = False
        if bashrc.exists() and "starship init bash" in bashrc.read_text(encoding="utf-8", errors="ignore"):
            bash_hooked = True

        hooks.append(
            ShellHookStatus(
                shell="bash",
                rc_file=bashrc,
                hooked=bash_hooked,
                hook_code='eval "$(starship init bash)"',
            )
        )

        return hooks

    def check_all(self) -> List[PackageStatus]:
        """对核心美化、终端、字体与 CLI 工具链执行全量状态审计。"""
        pkg_mgr, aur_helper, has_aur = self.detect_package_manager()
        active_installer = aur_helper if has_aur else (f"sudo {pkg_mgr} -S" if pkg_mgr == "pacman" else f"sudo {pkg_mgr} install")

        font_installed, _ = self.check_font_installed()

        # 检查 Orchis / Vimix / Tela 主题资源
        orchis_installed = (
            Path("/usr/share/themes/Orchis-Light").exists()
            or (self.data_dir / "plasma" / "look-and-feel" / "com.github.vinceliuice.Orchis").exists()
        )
        tela_installed = (
            Path("/usr/share/icons/Tela-circle").exists()
            or (self.data_dir / "icons" / "Tela-circle").exists()
        )
        vimix_cursors_installed = (
            Path("/usr/share/icons/Vimix-cursors").exists()
            or (self.data_dir / "icons" / "Vimix-cursors").exists()
            or (self.home / ".icons" / "Vimix-cursors").exists()
        )

        checks = [
            # 1. 核心终端与 Shell 工具（必需）
            PackageStatus(
                name="kitty",
                category="终端模拟器",
                description="GPU 加速终端，支持原生 Tab、亚克力毛玻璃与真彩色",
                installed=shutil.which("kitty") is not None,
                install_command=f"{active_installer} kitty",
                essential=True,
            ),
            PackageStatus(
                name="starship",
                category="Shell 提示符",
                description="跨 Shell 现代化提示符，提供当前工作目录胶囊与 Git 状态指示",
                installed=shutil.which("starship") is not None,
                install_command=f"{active_installer} starship",
                essential=True,
            ),
            PackageStatus(
                name="MesloLGS Nerd Font",
                category="排版与图标字体",
                description="显示工作目录胶囊、Powerline 箭头与开发语言图标必需字体",
                installed=font_installed,
                install_command=f"{active_installer} ttf-meslo-nerd-font-powerlevel10k" if has_aur else "krice install --fonts",
                essential=True,
            ),
            PackageStatus(
                name="fastfetch",
                category="系统信息展板",
                description="极速系统配置与美化看板展示工具",
                installed=shutil.which("fastfetch") is not None,
                install_command=f"{active_installer} fastfetch",
                essential=True,
            ),
            # 2. 现代 CLI 生产力增强工具（推荐）
            PackageStatus(
                name="eza",
                category="现代化 CLI 工具",
                description="ls 现代化替代品，支持文件图标与 Git 状态色彩",
                installed=shutil.which("eza") is not None,
                install_command=f"{active_installer} eza",
                essential=False,
            ),
            PackageStatus(
                name="bat",
                category="现代化 CLI 工具",
                description="cat 现代化替代品，自带语法高亮与行号",
                installed=shutil.which("bat") is not None,
                install_command=f"{active_installer} bat",
                essential=False,
            ),
            PackageStatus(
                name="zoxide",
                category="现代化 CLI 工具",
                description="智能目录快速跳转工具（基于访问频率自动补全）",
                installed=shutil.which("zoxide") is not None,
                install_command=f"{active_installer} zoxide",
                essential=False,
            ),
            # 3. Orchis 桌面主题套件（外观美化）
            PackageStatus(
                name="Orchis Theme",
                category="KDE & GTK 主题",
                description="极简现代 Orchis 全局主题与 GTK 3/4 样式",
                installed=orchis_installed,
                install_command=f"{aur_helper} -S orchis-theme" if has_aur else "krice install --orchis",
                essential=False,
            ),
            PackageStatus(
                name="Tela-circle Icons",
                category="图标主题",
                description="高清圆形质感图标主题，完美契合 Orchis 风格",
                installed=tela_installed,
                install_command=f"{aur_helper} -S tela-circle-icon-theme" if has_aur else "krice install --icons",
                essential=False,
            ),
            PackageStatus(
                name="Vimix Cursors",
                category="鼠标指针主题",
                description="高清扁平质感鼠标指针主题",
                installed=vimix_cursors_installed,
                install_command=f"{aur_helper} -S vimix-cursors" if has_aur else "krice install --cursors",
                essential=False,
            ),
            # 4. Niri 平铺合成器与 Wayland 现代化生态
            PackageStatus(
                name="niri",
                category="平铺合成器",
                description="现代无限水平滚动平铺 Wayland 合成器",
                installed=shutil.which("niri") is not None,
                install_command=f"{active_installer} niri",
                essential=False,
            ),
            PackageStatus(
                name="waybar",
                category="Wayland 状态栏",
                description="高度可定制的现代化 Wayland 状态栏与侧边坞",
                installed=shutil.which("waybar") is not None,
                install_command=f"{active_installer} waybar",
                essential=False,
            ),
            PackageStatus(
                name="fuzzel",
                category="应用启动器",
                description="极速轻量级 Wayland 应用启动菜单与模糊搜索选择器",
                installed=shutil.which("fuzzel") is not None,
                install_command=f"{active_installer} fuzzel",
                essential=False,
            ),
            PackageStatus(
                name="swaybg",
                category="壁纸守护",
                description="极简高效的 Wayland 壁纸渲染服务",
                installed=shutil.which("swaybg") is not None,
                install_command=f"{active_installer} swaybg",
                essential=False,
            ),
        ]
        return checks

    def doctor(self) -> DoctorReport:
        """执行全方位诊断，生成工具链、字体与 Shell 挂钩健康报告。"""
        pkg_mgr, aur_helper, has_aur = self.detect_package_manager()
        font_ok, font_msg = self.check_font_installed()
        return DoctorReport(
            packages=self.check_all(),
            hooks=self.check_shell_hooks(),
            fonts_ready=font_ok,
            font_details=font_msg,
            pkg_manager=pkg_mgr,
            has_aur_helper=has_aur,
            aur_helper=aur_helper,
        )

    def inject_shell_hooks(self, shells: Optional[List[str]] = None) -> List[Tuple[str, bool, str]]:
        """自动在用户 Shell 配置文件中注入 Starship 工作目录前缀集成代码。"""
        results: List[Tuple[str, bool, str]] = []
        target_shells = shells or ["fish", "zsh", "bash"]

        for sh in target_shells:
            if sh == "fish":
                fish_dir = self.config_dir / "fish"
                fish_dir.mkdir(parents=True, exist_ok=True)
                fish_config = fish_dir / "config.fish"

                hook_snippet = (
                    "\n# >>> krice starship prompt integration >>>\n"
                    "if type -q starship\n"
                    "    starship init fish | source\n"
                    "end\n"
                    "# <<< krice starship prompt integration <<<\n"
                )

                if not fish_config.exists():
                    fish_config.write_text(hook_snippet, encoding="utf-8")
                    results.append(("fish", True, f"已创建 {fish_config} 并写入 Starship 提示符集成"))
                else:
                    content = fish_config.read_text(encoding="utf-8", errors="ignore")
                    if "starship init fish" not in content:
                        fish_config.write_text(content.rstrip() + "\n" + hook_snippet, encoding="utf-8")
                        results.append(("fish", True, f"已在 {fish_config} 中成功注入 Starship 提示符挂钩"))
                    else:
                        results.append(("fish", True, f"{fish_config} 中已包含 Starship 提示符配置"))

            elif sh == "zsh":
                zshrc = self.home / ".zshrc"
                hook_snippet = (
                    "\n# >>> krice starship prompt integration >>>\n"
                    'if command -v starship >/dev/null 2>&1; then\n'
                    '    eval "$(starship init zsh)"\n'
                    "fi\n"
                    "# <<< krice starship prompt integration <<<\n"
                )
                if not zshrc.exists():
                    zshrc.write_text(hook_snippet, encoding="utf-8")
                    results.append(("zsh", True, f"已创建 {zshrc} 并写入 Starship 提示符集成"))
                else:
                    content = zshrc.read_text(encoding="utf-8", errors="ignore")
                    if "starship init zsh" not in content:
                        zshrc.write_text(content.rstrip() + "\n" + hook_snippet, encoding="utf-8")
                        results.append(("zsh", True, f"已在 {zshrc} 中成功注入 Starship 提示符挂钩"))
                    else:
                        results.append(("zsh", True, f"{zshrc} 中已包含 Starship 提示符配置"))

            elif sh == "bash":
                bashrc = self.home / ".bashrc"
                hook_snippet = (
                    "\n# >>> krice starship prompt integration >>>\n"
                    'if command -v starship >/dev/null 2>&1; then\n'
                    '    eval "$(starship init bash)"\n'
                    "fi\n"
                    "# <<< krice starship prompt integration <<<\n"
                )
                if not bashrc.exists():
                    bashrc.write_text(hook_snippet, encoding="utf-8")
                    results.append(("bash", True, f"已创建 {bashrc} 并写入 Starship 提示符集成"))
                else:
                    content = bashrc.read_text(encoding="utf-8", errors="ignore")
                    if "starship init bash" not in content:
                        bashrc.write_text(content.rstrip() + "\n" + hook_snippet, encoding="utf-8")
                        results.append(("bash", True, f"已在 {bashrc} 中成功注入 Starship 提示符挂钩"))
                    else:
                        results.append(("bash", True, f"{bashrc} 中已包含 Starship 提示符配置"))

        return results

    def install_packages(self, package_names: List[str]) -> Tuple[bool, str]:
        """调用系统包管理器或 AUR 助手安装指定软件包。"""
        pkg_mgr, aur_helper, has_aur = self.detect_package_manager()
        if not package_names:
            return True, "无需安装任何软件包"

        if has_aur and aur_helper:
            cmd = [aur_helper, "-S", "--needed", "--noconfirm"] + package_names
        elif pkg_mgr == "pacman":
            cmd = ["sudo", "pacman", "-S", "--needed", "--noconfirm"] + package_names
        elif pkg_mgr == "dnf":
            cmd = ["sudo", "dnf", "install", "-y"] + package_names
        elif pkg_mgr == "apt":
            cmd = ["sudo", "apt-get", "install", "-y"] + package_names
        elif pkg_mgr == "zypper":
            cmd = ["sudo", "zypper", "install", "-y"] + package_names
        else:
            return False, f"当前系统包管理器不支持自动静默安装 ({pkg_mgr})，请手动安装: {' '.join(package_names)}"

        try:
            res = subprocess.run(cmd, check=False)
            if res.returncode == 0:
                return True, f"已成功安装: {' '.join(package_names)}"
            return False, f"包管理器执行退出，返回码: {res.returncode}"
        except Exception as e:
            return False, f"执行安装命令异常: {e}"
