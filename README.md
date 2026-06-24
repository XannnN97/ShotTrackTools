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

1. 确认以下路径存在（如不存在请手动创建）：
   ```
   C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Workflow Integration Plugins\
   ```

2. 将 `ShotTrackTools_v1.1.0/` 文件夹**整体复制**到上述路径中即可，**无需重命名**

3. **重启 DaVinci Resolve**

4. 在达芬奇中加载：
   ```
   Workspace → Workflow Integrations → ShotTrackTools
   ```

5. 插件窗口自动加载，左侧选择功能，右侧填写参数，点击**执行**

#### 方式二：Scripts 菜单（兼容，免费/Studio 均可）

独立脚本分散在 Scripts 菜单中运行，适合不需要统一界面的场景。

**安装步骤**：

1. 将 `legacy/` 目录下的 `.py` 文件复制到：
   ```
   %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\ShotTrackTools
   ```

2. **重启 DaVinci Resolve**

3. 在达芬奇中运行：
   ```
   Workspace → Scripts → Utility → ShotTrackTools
   ```

### 使用指南（Workflow Integration）

1. 启动插件后，弹出统一 HTML GUI 窗口
2. 左侧选择功能（批量替换 / 顺序递增 / PNG/XML 导出 / 去后缀）
3. 右侧填写参数，点击**执行**
4. 底部日志区域显示操作结果
5. 支持**中英文切换**（界面右上角）
6. 支持**撤回**（Undo）功能，执行后可恢复原始名称

> **注意**：v1.0.x 时代的 `ShotTrackTools_Configurator.py` 独立配置工具已被 Workflow Integration 统一 GUI 取代，`legacy/` 目录下的旧脚本仅作存档，不再推荐使用。

### 文件结构

```
ShotTrackTools/
├── README.md                          # 本说明文档
├── CHANGELOG.md                       # 版本更新日志
├── LICENSE                            # MIT 许可证
├── requirements.txt                   # 外部依赖声明（无）
├── .gitignore                         # Git 排除规则
├── PROJECT_MAINTENANCE.md            # 项目维护标准
├── test_shottracktools.py            # 单元测试
│
├── legacy/                            # 旧版脚本存档（v1.0.x）
│   ├── remove_png_suffix.py
│   ├── Batch_Shot_Renamer.py
│   ├── Batch_Shot_Sequential.py
│   ├── Timeline_Shot_to_PNG.py
│   └── ShotTrackTools_Configurator.py
│
└── ShotTrackTools_v1.1.0/            # Workflow Integration 插件（v1.1.0）
    ├── manifest.xml                   # 插件描述文件
    ├── package.json                   # Electron 配置
    ├── main.js                        # Electron 主进程
    ├── preload.js                     # 安全预加载（v19.0.2+ 兼容）
    ├── index.html                     # UI 入口页面
    ├── app.js                         # 前端逻辑（功能切换、参数收集、IPC）
    ├── style.css                      # 达芬奇风格样式
    ├── backend.py                     # Python 后端执行引擎
    ├── shottracktools_utils.py        # 公共模块（版本号、轨道解析）
    └── lib/
        ├── __init__.py
        ├── renamer.py                 # 批量替换逻辑
        ├── sequential.py              # 顺序递增逻辑
        ├── png_exporter.py            # PNG/XML 导出逻辑
        └── remove_suffix.py           # 去后缀逻辑
```

### 常见问题

**Q1：Workflow Integration 菜单中没有 ShotTrackTools**

- 确认安装路径是 `C:\ProgramData\...\Workflow Integration Plugins\com.xannnn97.shottracktools\`
- 确认文件夹内包含 `manifest.xml` 和 `main.js`
- 确认使用的是 **DaVinci Resolve Studio**（免费版不支持）
- 重启达芬奇后再次检查

**Q2：插件窗口无法获取 Resolve 对象**

- 确认 Python 已安装 `py` 命令（Windows 上 `py -3` 可用）
- 检查 Electron 启动时是否成功设置了 `PYTHONPATH` 和 `RESOLVE_SCRIPT_LIB` 环境变量
- 查看达芬奇 Console（Py3）是否有 Python 错误输出
- 检查 `main.js` 中的 `RESOLVE_SCRIPT_LIB` 路径是否指向正确的 `fusionscript.dll` 位置

**Q3：Scripts 菜单版本提示 "Cannot connect to DaVinci Resolve"**

- 旧版 Scripts 菜单的独立脚本仍可在 `Workspace → Scripts → Utility` 中使用
- 如果不需要旧版，可直接删除 `%APPDATA%\...\Fusion\Scripts\Utility\ShotTrackTools` 文件夹

**Q4：HTML 界面显示异常或无法操作**

- 确认 Electron 版本兼容（DaVinci Resolve v19.0.2+ 的 contextIsolation 限制）
- 检查 `preload.js` 是否正确加载
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

1. Ensure the following path exists (create manually if it doesn't):
   ```
   C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Workflow Integration Plugins\
   ```

2. Copy `ShotTrackTools_v1.1.0/` folder directly into the path above, **no need to rename**

3. **Restart DaVinci Resolve**

4. Load from Resolve menu:
   ```
   Workspace → Workflow Integrations → ShotTrackTools
   ```

5. The plugin window loads automatically. Select function on the left, fill parameters on the right, click **Execute**

#### Option B: Scripts Menu (Compatible, Free/Studio)

Individual scripts for the Scripts menu.

**Steps**:

1. Copy `.py` files from `legacy/` to:
   ```
   %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\ShotTrackTools
   ```

2. **Restart DaVinci Resolve**

3. Run from menu:
   ```
   Workspace → Scripts → Utility → ShotTrackTools
   ```

### Usage Guide (Workflow Integration)

1. Launch the plugin, the unified HTML GUI window appears
2. Select function on the left (Batch Replace / Sequential / PNG/XML Export / Remove Suffix)
3. Fill parameters on the right, click **Execute**
4. View operation results in the log panel at the bottom
5. Supports **CN/EN language switching** (top-right corner)
6. Supports **Undo** to restore original names after execution

> **Note**: The v1.0.x `ShotTrackTools_Configurator.py` standalone tool has been replaced by the Workflow Integration unified GUI. Scripts in `legacy/` are archived only and not recommended for use.

### File Structure

```
ShotTrackTools/
├── README.md                          # This document
├── CHANGELOG.md                       # Version history
├── LICENSE                            # MIT License
├── requirements.txt                   # External dependencies (none)
├── .gitignore                         # Git exclusion rules
├── PROJECT_MAINTENANCE.md            # Project maintenance standards
├── test_shottracktools.py            # Unit tests
│
├── legacy/                            # Legacy scripts (v1.0.x archive)
│   ├── remove_png_suffix.py
│   ├── Batch_Shot_Renamer.py
│   ├── Batch_Shot_Sequential.py
│   ├── Timeline_Shot_to_PNG.py
│   └── ShotTrackTools_Configurator.py
│
└── ShotTrackTools_v1.1.0/             # Workflow Integration plugin (v1.1.0)
    ├── manifest.xml                   # Plugin descriptor
    ├── package.json                   # Electron config
    ├── main.js                        # Electron main process
    ├── preload.js                     # Security preload (v19.0.2+ compatible)
    ├── index.html                     # UI entry page
    ├── app.js                         # Frontend logic (feature switching, params, IPC)
    ├── style.css                      # DaVinci-style theme
    ├── backend.py                     # Python backend execution engine
    ├── shottracktools_utils.py        # Common module (version, track parsing)
    └── lib/
        ├── __init__.py
        ├── renamer.py                 # Batch replace logic
        ├── sequential.py              # Sequential naming logic
        ├── png_exporter.py            # PNG/XML export logic
        └── remove_suffix.py           # Suffix removal logic
```

### FAQ

**Q1: ShotTrackTools not in Workflow Integration menu**

- Confirm installation path: `C:\ProgramData\...\Workflow Integration Plugins\com.xannnn97.shottracktools\`
- Confirm folder contains `manifest.xml` and `main.js`
- Confirm using **DaVinci Resolve Studio** (Free version does not support)
- Restart Resolve after installation

**Q2: Plugin window cannot connect to Resolve**

- Confirm Python `py` command available (`py -3` works on Windows)
- Check `PYTHONPATH` and `RESOLVE_SCRIPT_LIB` environment variables set by Electron
- Check DaVinci Resolve Console (Py3) for Python errors
- Verify `RESOLVE_SCRIPT_LIB` path in `main.js` points to correct `fusionscript.dll`

**Q3: Scripts menu version shows "Cannot connect to DaVinci Resolve"**

- Legacy scripts still available at `Workspace → Scripts → Utility`
- Delete `%APPDATA%\...\Fusion\Scripts\Utility\ShotTrackTools` if not needed

**Q4: HTML interface display or operation issues**

- Confirm Electron version compatibility (Resolve v19.0.2+ contextIsolation)
- Check `preload.js` loaded correctly
- Ensure screen resolution sufficient (1080p+ recommended)

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

[MIT License](LICENSE)

## Credits

Developed by XannnN97 for DaVinci Resolve workflow development.
