# Contributing to ShotTrackTools

> 感谢您对 ShotTrackTools 项目的关注！本文档将帮助您了解如何参与贡献。

## 语言 Language

本文档同时提供 [中文](#中文) 和 [English](#english)。

---

## 中文

### 如何参与

我们欢迎以下形式的贡献：

- **报告 Bug**：在 GitHub Issues 中提交问题，帮助改进插件稳定性
- **功能建议**：提出新功能想法或改进现有功能
- **代码贡献**：修复 Bug 或实现新功能（通过 Pull Request）
- **文档改进**：修正 README、CHANGELOG 或其他文档中的错误
- **使用反馈**：在实际工作中使用插件并提供反馈

### 报告 Bug

在提交 Bug 之前，请先检查 [现有 Issues](https://github.com/XannnN97/ShotTrackTools/issues) 是否已有人报告相同问题。

#### Bug 报告模板

提交 Bug 时，请在 Issue 中包含以下信息：

| 项目 | 说明 |
|------|------|
| **DaVinci Resolve 版本** | 例如：DaVinci Resolve 21 Studio |
| **操作系统** | 例如：Windows 11 23H2 |
| **Python 版本** | 在终端运行 `py --version` 或 `python3 --version` |
| **插件版本** | 在插件界面右上角查看版本号 |
| **问题描述** | 清晰描述发生了什么 |
| **复现步骤** | 按顺序列出能稳定复现问题的操作步骤 |
| **预期结果** | 描述您认为应该发生什么 |
| **实际结果** | 描述实际发生了什么 |
| **日志输出** | 复制插件底部日志区域的完整输出（如有） |
| **截图** | 如有界面问题，请附上截图 |

**示例**：

```
DaVinci Resolve 版本：DaVinci Resolve 21 Studio
操作系统：Windows 11 23H2
Python 版本：Python 3.11.4
插件版本：v1.2.0

问题描述：EDL 导出时提示"No clips on track"

复现步骤：
1. 打开一个有时间线的新项目
2. 在 V1 轨道放置至少一个片段
3. 选择 ShotTrackTools → EDL 导出
4. 选择 V1 轨道，点击执行

预期结果：生成 EDL 文件

实际结果：提示"No clips on track"，但轨道上确实有素材

日志输出：
[INFO] Timeline: Timeline 1
[INFO] Target track: V1
[INFO] 您选择的轨道 V1 目前没有素材，请检查正确的目标轨道
```

### 功能建议

提交功能建议时，请包含：

- **功能描述**：这个功能做什么
- **使用场景**：为什么需要这个功能，在什么工作流中会用到
- **预期行为**：描述功能应该如何工作
- **优先级**：对您的日常工作有多重要（低/中/高）

### 开发环境设置

如果您计划提交代码，请按以下步骤配置开发环境：

#### 基本要求

- **DaVinci Resolve Studio**：Workflow Integration 仅支持 Studio 版
- **Python 3.9+**：64 位版本
- **Git**：已安装并配置 GitHub 访问
- **文本编辑器/IDE**：VS Code、Sublime Text 或任何您熟悉的编辑器

#### 克隆仓库

```bash
git clone https://github.com/XannnN97/ShotTrackTools.git
cd ShotTrackTools
```

#### 目录结构理解

```
ShotTrackTools/
├── ShotTrackTools_v1.2.0/    # 当前版本（主开发目录）
│   ├── manifest.xml           # 插件描述文件
│   ├── main.js                # Electron 主进程
│   ├── backend.py             # Python 后端执行引擎
│   ├── app.js                 # 前端逻辑
│   ├── shottracktools_utils.py # 公共工具模块
│   └── lib/                   # 功能模块
│       ├── renamer.py
│       ├── sequential.py
│       ├── png_exporter.py
│       ├── remove_suffix.py
│       └── edl_exporter.py
│
├── legacy/                     # 旧版脚本存档（只读，不修改）
├── test_shottracktools.py      # 单元测试
└── README.md                   # 项目文档
```

**开发时只修改 `ShotTrackTools_v1.2.0/` 目录下的文件。**

### 代码提交规范

#### Git 提交信息格式

所有提交信息必须遵循以下格式：

```
<type>: <description>
```

| 类型 | 用途 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: add EDL export support` |
| `fix` | Bug 修复 | `fix: handle empty track gracefully` |
| `docs` | 文档更新 | `docs: update README for v1.2.0` |
| `refactor` | 重构代码 | `refactor: extract shared module` |
| `chore` | 工程化/杂项 | `chore: ignore generated EDL files` |
| `test` | 测试相关 | `test: add PNG generation test` |
| `style` | 代码格式（无逻辑变更） | `style: fix indentation` |

#### 提交原子化原则

- 一个 commit 只做一件事
- 不要将功能代码和文档更新混在一起提交（除非文档是功能的一部分）
- 如果修改了多个文件，确保它们都属于同一个逻辑变更

### 版本号更新

如果您修改了功能代码，必须同步更新以下文件中的版本号：

| 文件 | 版本号位置 |
|------|-----------|
| `shottracktools_utils.py` | `__version__ = "x.x.x"` |
| `manifest.xml` | `<Version>x.x.x</Version>` |
| `package.json` | `"version": "x.x.x"` |
| `README.md` | `> **版本：vx.x.x**` |
| `CHANGELOG.md` | 添加新版本条目 |

**版本号规则**：

- `patch`（第三位）：Bug 修复、小改进（如 1.2.0 → 1.2.1）
- `minor`（第二位）：新功能、向后兼容（如 1.2.0 → 1.3.0）
- `major`（第一位）：破坏性变更（如 1.2.0 → 2.0.0）

### Pull Request 流程

1. **Fork 仓库**：从 [XannnN97/ShotTrackTools](https://github.com/XannnN97/ShotTrackTools) Fork 到您的个人账号
2. **创建分支**：从 `master` 创建功能分支
   ```bash
   git checkout -b feat/your-feature-name
   ```
3. **开发与测试**：修改代码并在本地测试（在 DaVinci Resolve 中实际运行）
4. **提交更改**：按规范编写提交信息
5. **推送到 Fork**：
   ```bash
   git push origin feat/your-feature-name
   ```
6. **创建 PR**：在 GitHub 上创建 Pull Request，描述：
   - 修改了什么
   - 为什么需要这个修改
   - 测试方式
   - 是否有破坏性变更

### 测试要求

在提交代码前，请确保：

- [ ] 修改的功能在 DaVinci Resolve 中实际测试通过
- [ ] 相关功能未受本次修改影响（回归测试）
- [ ] 如果修改了后端，前端界面同步适配
- [ ] 版本号已更新（如适用）
- [ ] CHANGELOG.md 已添加条目（如适用）
- [ ] README.md 已同步（如适用）

### 代码风格

#### Python

- 使用 UTF-8 编码，文件头包含 `# -*- coding: utf-8 -*-`
- 使用 4 空格缩进
- 函数和变量使用 `snake_case`
- 模块导入顺序：标准库 → 第三方库 → 本地模块
- 中文日志和错误消息使用中文，代码注释可根据偏好使用中文或英文

#### JavaScript

- 使用 2 空格缩进
- 使用 `const` 和 `let`，避免 `var`
- 字符串优先使用单引号
- 回调函数使用箭头函数

### 常见问题

**Q：我没有 DaVinci Resolve Studio，可以贡献代码吗？**

A：可以，但您的修改需要由有 Studio 版环境的贡献者测试后才能合并。请在 PR 中明确说明您未在 Studio 环境中测试。

**Q：我可以修改 `legacy/` 目录下的旧脚本吗？**

A：不建议。`legacy/` 是 v1.0.x 时代的存档，只保留历史记录。所有新开发应在 `ShotTrackTools_v1.2.0/` 中进行。

**Q：我发现文档中有错别字，可以直接提交 PR 吗？**

A：可以，对于小修正（如错别字、链接修复），直接提交 PR 即可，不需要创建 Issue。

---

## English

### How to Contribute

We welcome contributions in the following forms:

- **Bug Reports**: Submit issues on GitHub to help improve plugin stability
- **Feature Requests**: Propose new features or improvements
- **Code Contributions**: Fix bugs or implement new features via Pull Requests
- **Documentation**: Fix errors in README, CHANGELOG, or other docs
- **Usage Feedback**: Use the plugin in real work and share feedback

### Reporting Bugs

Before submitting a bug, please check [existing Issues](https://github.com/XannnN97/ShotTrackTools/issues) to see if it has already been reported.

#### Bug Report Template

Please include the following information when submitting a bug:

| Item | Description |
|------|-------------|
| **DaVinci Resolve Version** | e.g., DaVinci Resolve 21 Studio |
| **Operating System** | e.g., Windows 11 23H2 |
| **Python Version** | Run `py --version` or `python3 --version` in terminal |
| **Plugin Version** | Check version number in the top-right corner of the plugin UI |
| **Bug Description** | Clear description of what happened |
| **Reproduction Steps** | Step-by-step instructions to reproduce the issue |
| **Expected Result** | What you expected to happen |
| **Actual Result** | What actually happened |
| **Log Output** | Copy the full log output from the plugin's bottom panel (if available) |
| **Screenshots** | Attach screenshots if it's a UI issue |

### Feature Requests

When submitting a feature request, please include:

- **Feature Description**: What the feature does
- **Use Case**: Why you need it, in what workflow it would be used
- **Expected Behavior**: How the feature should work
- **Priority**: How important it is to your daily work (low/medium/high)

### Development Environment Setup

If you plan to submit code, please set up your development environment as follows:

#### Prerequisites

- **DaVinci Resolve Studio**: Workflow Integration is Studio-only
- **Python 3.9+**: 64-bit version
- **Git**: Installed and configured for GitHub access
- **Text Editor/IDE**: VS Code, Sublime Text, or any editor you prefer

#### Clone the Repository

```bash
git clone https://github.com/XannnN97/ShotTrackTools.git
cd ShotTrackTools
```

#### Directory Structure

```
ShotTrackTools/
├── ShotTrackTools_v1.2.0/    # Current version (main dev directory)
│   ├── manifest.xml           # Plugin descriptor
│   ├── main.js                # Electron main process
│   ├── backend.py             # Python backend execution engine
│   ├── app.js                 # Frontend logic
│   ├── shottracktools_utils.py # Common utilities
│   └── lib/                   # Feature modules
│       ├── renamer.py
│       ├── sequential.py
│       ├── png_exporter.py
│       ├── remove_suffix.py
│       └── edl_exporter.py
│
├── legacy/                     # Legacy scripts archive (read-only)
├── test_shottracktools.py      # Unit tests
└── README.md                   # Project documentation
```

**Only modify files under `ShotTrackTools_v1.2.0/` during development.**

### Commit Message Convention

All commit messages must follow this format:

```
<type>: <description>
```

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat: add EDL export support` |
| `fix` | Bug fix | `fix: handle empty track gracefully` |
| `docs` | Documentation | `docs: update README for v1.2.0` |
| `refactor` | Code refactoring | `refactor: extract shared module` |
| `chore` | Engineering/misc | `chore: ignore generated EDL files` |
| `test` | Testing | `test: add PNG generation test` |
| `style` | Code formatting only | `style: fix indentation` |

#### Atomic Commits

- One commit should do one thing
- Do not mix feature code and documentation updates in one commit (unless docs are part of the feature)
- If multiple files are modified, ensure they all belong to the same logical change

### Version Number Updates

If you modify functional code, you must sync version numbers in the following files:

| File | Version Location |
|------|-----------------|
| `shottracktools_utils.py` | `__version__ = "x.x.x"` |
| `manifest.xml` | `<Version>x.x.x</Version>` |
| `package.json` | `"version": "x.x.x"` |
| `README.md` | `> **Version: vx.x.x**` |
| `CHANGELOG.md` | Add new version entry |

**Version Rules**:

- `patch` (third digit): Bug fixes, small improvements (e.g., 1.2.0 → 1.2.1)
- `minor` (second digit): New features, backward compatible (e.g., 1.2.0 → 1.3.0)
- `major` (first digit): Breaking changes (e.g., 1.2.0 → 2.0.0)

### Pull Request Process

1. **Fork the Repository**: Fork from [XannnN97/ShotTrackTools](https://github.com/XannnN97/ShotTrackTools) to your personal account
2. **Create a Branch**: Create a feature branch from `master`
   ```bash
   git checkout -b feat/your-feature-name
   ```
3. **Develop and Test**: Modify code and test locally (run in DaVinci Resolve)
4. **Commit Changes**: Write commit messages following the convention
5. **Push to Fork**:
   ```bash
   git push origin feat/your-feature-name
   ```
6. **Create PR**: Open a Pull Request on GitHub, describing:
   - What was changed
   - Why the change is needed
   - How it was tested
   - Whether there are breaking changes

### Testing Requirements

Before submitting code, please ensure:

- [ ] The modified feature has been tested in DaVinci Resolve
- [ ] Related features have not been affected by this change (regression test)
- [ ] If the backend was modified, the frontend UI is adapted accordingly
- [ ] Version numbers are updated (if applicable)
- [ ] CHANGELOG.md has been updated (if applicable)
- [ ] README.md has been synced (if applicable)

### Code Style

#### Python

- Use UTF-8 encoding, include `# -*- coding: utf-8 -*-` at the top
- Use 4 spaces for indentation
- Use `snake_case` for functions and variables
- Import order: standard library → third-party → local modules
- Chinese logs and error messages in Chinese; code comments in Chinese or English per preference

#### JavaScript

- Use 2 spaces for indentation
- Use `const` and `let`, avoid `var`
- Prefer single quotes for strings
- Use arrow functions for callbacks

### Common Questions

**Q: I don't have DaVinci Resolve Studio. Can I still contribute code?**

A: Yes, but your changes will need to be tested by someone with a Studio environment before merging. Please state clearly in your PR that you have not tested in a Studio environment.

**Q: Can I modify scripts in the `legacy/` directory?**

A: Not recommended. `legacy/` is an archive from v1.0.x, kept for historical reference only. All new development should happen in `ShotTrackTools_v1.2.0/`.

**Q: I found a typo in the documentation. Can I submit a PR directly?**

A: Yes, for minor fixes (typos, broken links), you can submit a PR directly without creating an Issue.

---

> Thank you for contributing to ShotTrackTools!

---

**Last Updated**: 2025-06-25
