# ShotTrackTools

> **版本：v1.1.0**  
> **适用软件：DaVinci Resolve 21（Studio 版推荐）**  
> **操作系统：Windows 10/11**

[English](#english) | [中文](#中文)

---

## 中文

### 简介

ShotTrackTools 是一套用于 **DaVinci Resolve** 的 VFX/剪辑交接工作流辅助工具，专注于解决镜头号管理中的批量命名、后缀清理、透明 PNG 占位符生成等问题。

### 核心功能

| 功能 | 说明 |
|------|------|
| **批量替换** | 将时间线轨道上所有 Clip Name 中的指定文本批量替换为另一文本 |
| **顺序递增** | 按固定前缀和步长对时间线片段进行递增命名（如 `0010`, `0020`, `0030`） |
| **PNG/XML 导出** | 生成透明 PNG 占位符 + FCP 7 XML v5，可导入达芬奇重建轨道 |
| **去后缀** | 批量去掉媒体池内所有片段的 `.png` 后缀 |

### 安装方式（二选一）

#### 方式一：Workflow Integration（推荐，Studio 版）

统一 GUI 窗口，支持中英文切换，功能集中在一个面板中操作。

**系统要求**（无外部依赖）：
- DaVinci Resolve **Studio**（免费版不支持 Workflow Integration）
- Python 3.9+（64位）

**无需安装任何 Python 包**，PNG 生成使用 Python 内置 `zlib` / `struct` 模块。

**安装步骤**：

1. 在以下路径**新建文件夹** `com.xannnn97.shottracktools`：
   ```
   C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Workflow Integration Plugins\
   ```
   （如果 `Workflow Integration Plugins` 文件夹不存在，请手动创建）

2. 将 `workflow_integration/` 目录内的**所有文件和子文件夹**复制到 `com.xannnn97.shottracktools/` 中

3. **重启 DaVinci Resolve**

4. 在达芬奇中加载：
   ```
   Workspace → Workflow Integrations → ShotTrackTools
   ```

5. 点击 **Launch ShotTrackTools** 启动统一 GUI 窗口

#### 方式二：Scripts 菜单（兼容，免费/Studio 均可）

独立脚本分散在 Scripts 菜单中运行，适合不需要统一界面的场景。

**安装步骤**：

1. 将项目根目录下的 `.py` 文件复制到：
   ```
   %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\ShotTrackTools
   ```

2. **重启 DaVinci Resolve**

3. 在达芬奇中运行：
   ```
   Workspace → Scripts → Utility → ShotTrackTools
   ```

### 使用指南（Workflow Integration）

1. 启动插件后，弹出统一 GUI 窗口
2. 左侧选择功能（批量替换 / 顺序递增 / PNG/XML 导出 / 去后缀）
3. 右侧填写参数，点击**执行**
4. 底部日志区域显示操作结果
5. 支持**中英文切换**（界面左下角）
6. 支持**撤回**（Undo）功能，执行后可恢复原始名称

> **注意**：v1.0.x 时代的 `ShotTrackTools_Configurator.py` 独立配置工具已被 Workflow Integration 统一 GUI 取代，`legacy/` 目录下的旧脚本仅作存档，不再推荐使用。

### 文件结构

```
ShotTrackTools/
├── README.md                          # 本说明文档
├── CHANGELOG.md                       # 版本更新日志
├── LICENSE                            # MIT 许可证
├── requirements.txt                   # Python 依赖声明
├── .gitignore                         # Git 排除规则
├── test_shottracktools.py            # 单元测试
│
├── workflow_integration/             # Workflow Integration 插件（v1.1.0）
│   ├── manifest.xml                  # 插件描述文件
│   ├── package.json                  # Electron 配置
│   ├── main.js                       # Electron 主进程
│   ├── preload.js                    # 安全预加载（v19.0.2+ 兼容）
│   ├── index.html                    # 启动界面
│   ├── ShotTrackTools_Workflow.py   # 统一 GUI（tkinter，中英文）
│   ├── shottracktools_utils.py      # 公共模块
│   └── lib/
│       ├── renamer.py               # 批量替换逻辑
│       ├── sequential.py            # 顺序递增逻辑
│       ├── png_exporter.py          # PNG/XML 导出逻辑
│       └── remove_suffix.py         # 去后缀逻辑
│
├── shottracktools_utils.py          # 公共模块（v1.0.x 版本）
├── remove_png_suffix.py            # 去后缀（独立脚本）
├── Batch_Shot_Renamer.py           # 批量替换（独立脚本）
├── Batch_Shot_Sequential.py        # 顺序递增（独立脚本）
├── Timeline_Shot_to_PNG.py         # PNG/XML 导出（独立脚本）
└── ShotTrackTools_Configurator.py  # 参数配置 GUI（独立脚本）
```

### 常见问题

**Q1：Workflow Integration 菜单中没有 ShotTrackTools**

- 确认安装路径是 `C:\ProgramData\...\Workflow Integration Plugins\com.xannnn97.shottracktools\`
- 确认文件夹内包含 `manifest.xml` 和 `main.js`
- 确认使用的是 **DaVinci Resolve Studio**（免费版不支持）
- 重启达芬奇后再次检查

**Q2：点击 Launch 后 tkinter 窗口无法获取 Resolve 对象**

- 确认 Python 已安装 `py` 命令（Windows 上 `py -3` 可用）
- 检查 Electron 启动时是否成功设置了 `PYTHONPATH` 和 `RESOLVE_SCRIPT_LIB` 环境变量
- 查看达芬奇 Console（Py3）是否有 Python 错误输出

**Q3：Scripts 菜单版本提示 "Cannot connect to DaVinci Resolve"**

- 旧版 Scripts 菜单的独立脚本仍可在 `Workspace → Scripts → Utility` 中使用
- 如果不需要旧版，可直接删除 `%APPDATA%\...\Fusion\Scripts\Utility\ShotTrackTools` 文件夹

**Q4：tkinter 窗口无法打开或显示不完整**

- 确认 Python 安装时包含 tkinter（安装时勾选 tcl/tk 和 IDLE）
- 确认屏幕分辨率足够显示窗口内容（建议 1080p+）

---

## English

### Introduction

ShotTrackTools is a set of VFX/editorial handoff workflow utilities for **DaVinci Resolve**, focused on batch shot naming, suffix cleanup, and transparent PNG placeholder generation.

### Core Features

| Feature | Description |
|---------|-------------|
| **Batch Replace** | Batch replace text in timeline Clip Names (e.g. `sq1300` → `sq1400`) |
| **Sequential Naming** | Sequential naming with fixed prefix and step (e.g. `0010`, `0020`, `0030`) |
| **PNG/XML Export** | Generate transparent PNG placeholders + FCP 7 XML v5 for timeline reconstruction |
| **Remove Suffix** | Batch remove `.png` suffix from Media Pool clips |

### Installation

#### Option A: Workflow Integration (Recommended, Studio Only)

Unified GUI with bilingual (CN/EN) support.

**Requirements** (No external dependencies):
- DaVinci Resolve **Studio** (Free version does not support Workflow Integration)
- Python 3.9+ (64-bit)

**No Python packages need to be installed**. PNG generation uses Python's built-in `zlib` / `struct` modules.

**Steps**:

1. Create a new folder `com.xannnn97.shottracktools` at:
   ```
   C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Workflow Integration Plugins\
   ```
   (Create `Workflow Integration Plugins` manually if it doesn't exist)

2. Copy all files from `workflow_integration/` into `com.xannnn97.shottracktools/`

3. **Restart DaVinci Resolve**

4. Load from Resolve menu:
   ```
   Workspace → Workflow Integrations → ShotTrackTools
   ```

5. Click **Launch ShotTrackTools** to open the unified GUI

#### Option B: Scripts Menu (Compatible, Free/Studio)

Individual scripts for the Scripts menu.

**Steps**:

1. Copy `.py` files from project root to:
   ```
   %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\ShotTrackTools
   ```

2. **Restart DaVinci Resolve**

3. Run from menu:
   ```
   Workspace → Scripts → Utility → ShotTrackTools
   ```

### File Structure

See the Chinese section above for the full tree.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

[MIT License](LICENSE)

## Credits

Developed by XAN for BaseFX VFX pipeline workflows.
