# ShotTrackTools 更新日志

## [1.2.0] - 2025-06-24

### 新增功能
- **目标轨道实时下拉菜单**：自动检测当前时间线的所有视频/音频轨道，3 秒轮询自动刷新，切换时间线后自动更新
- **配置持久化**：每个功能独立保存上次使用的参数，切换功能时自动恢复，覆盖写入 JSON（文件大小恒定 1 KB）
- **EDL 导出**：新增目标轨道 EDL 导出功能，生成 CMX3600 标准格式，支持自定义文件名和输出目录

### 改进
- **无素材友好提示**：当用户选择空轨道时，日志显示 "您选择的轨道 X 目前没有素材，请检查正确的目标轨道" 而非红色报错
- **项目文件夹重命名**：`workflow_integration/` → `ShotTrackTools_v1.1.0/`，安装时无需重命名，直接复制即可
- **README 文件结构同步**：中文/英文文件结构树更新为实际目录，安装步骤简化

### 工程化
- 新增 `lib/edl_exporter.py` 模块，生成 CMX3600 EDL 格式
- 后端新增 `get_timeline_info` 接口，返回时间线名称和轨道列表
- 后端新增 `get_config` / `set_config` 接口，支持配置持久化
- 前端 `app.js` 重写：添加轨道下拉菜单、配置缓存、EDL 选项卡、3 秒轮询
- 前端 `main.js` 和 `preload.js` 扩展 IPC：支持 `getTracks`、`getConfig`、`setConfig`

---

## [1.1.0] - 2025-06-23

### Workflow Integration 插件（正式发布）
- 新增官方 Workflow Integration 插件架构，通过 `Workspace → Workflow Integrations` 菜单加载
- **纯 HTML UI**：单 Electron 窗口内完成所有操作，无第二弹窗，深色主题接近达芬奇风格
- 支持中英文语言切换（运行时即时切换）
- 左侧功能导航 + 右侧参数表单 + 底部日志输出区域
- **撤回（Undo）功能**：支持批量替换、顺序递增、去后缀的撤回，自动记录原始名称
- 基于 Electron 包装器（main.js + preload.js + index.html + app.js + style.css）+ Python 后端的混合架构
- 适配 DaVinci Resolve v19.0.2+ 安全限制（contextIsolation + sandboxing）
- 通过 IPC 通信启动 Python 子进程，自动注入 `PYTHONPATH` 和 `RESOLVE_SCRIPT_LIB` 环境变量
- 核心功能逻辑（lib/目录）从 Scripts 菜单版本提取为独立模块，返回日志列表而非直接打印

### 架构重构
- 新增 `ShotTrackTools_v1.1.0/` 目录，包含完整的插件结构
- 提取 `lib/renamer.py`、`lib/sequential.py`、`lib/png_exporter.py`、`lib/remove_suffix.py`
- 每个功能模块独立为 `run(resolve, cfg)` 接口，返回日志
- 新增 `backend.py` 作为 Python 后端执行引擎（接收 stdin JSON，返回 stdout JSON）
- 各模块返回 undoData 支持撤回操作

### 工程化改进
- 新增 `legacy/` 文件夹，旧版 Scripts 菜单独立脚本归档整理
- 根目录只保留文档、配置和新版 `ShotTrackTools_v1.1.0/` 文件夹
- **移除 Pillow 依赖**：PNG 生成使用 Python 标准库 `zlib` / `struct` 实现，无需任何外部 Python 包
- 修复 XML 生成循环缩进问题，确保每个 clipitem 标签正确闭合

### 修复
- 修复 `renamer.py` `undo_items` 未初始化导致 `NameError`
- 修复 `backend.py` 对 `png_exporter` list/dict 返回值的兼容性处理
- 修复 Electron 中 `findPythonCommand` 返回含空格字符串导致 `spawn ENOENT`
- 修复 Python 子进程无法找到 `DaVinciResolveScript` 模块的问题（注入 PYTHONPATH）
- 修复 `.gitignore` 中 `*.xml` 全局排除导致 `manifest.xml` 被忽略的问题（GitHub Issue #1）
- 修复 `.gitignore` 中 `*.png` 全局排除过于宽泛的问题（移除用户运行产物排除规则）

### 工程化改进（后续）
- 清理根目录 `shottracktools_utils.py` 版本漂移（Issue #2）
- 修复 Undo 匹配键使用 `GetStart()` 单键的问题，改为 `start` + `originalName` 双键匹配（Issue #4）
- `RESOLVE_SCRIPT_LIB` 路径从硬编码改为多路径探测（C/D/E 盘 + 32/64位）（Issue #6）
- `png_exporter.py` 添加输出目录可写性检查（Issue #7）
- 添加 PNG 导出后"缩放到帧尺寸"提示（Issue #5）
- `main.js` 添加 Python 子进程 60 秒超时机制（Issue #9）
- 新增 PNG 生成单元测试（Issue #3）
- README.md 更新命名空间为 `com.xannnn97.shottracktools`（Issue #11）
- README.md 标注 Configurator 已被 Workflow Integration 取代（Issue #10）

---

## [1.0.1] - 2025-06-22

### 工程化改进
- 提取公共模块 `shottracktools_utils.py`，消除 `parse_track()` 和 `get_params()` 在 3 个脚本中的重复代码
- 统一版本号管理（`__version__ = "1.0.1"`），Configurator 窗口标题显示版本
- 新增 `.gitignore` 文件，排除缓存、生成文件和用户配置
- 新增 `requirements.txt`，声明 Pillow 依赖
- 新增 MIT 许可证
- 新增 `CHANGELOG.md`

### 错误处理增强
- Configurator 增强参数校验：轨道格式、非空检查、数字范围（步长>0、位数1-10）
- 输出目录自动创建（如果填写且不存在）
- 保存失败时显示更清晰的错误列表（逐条列出）

### 其他
- 各脚本模块导入方式统一，支持从达芬奇 Scripts 目录和外部直接运行

---

## [1.0.0] - 2025-06-18

### 初始发布
- `remove_png_suffix` - 批量去掉媒体池内所有片段的 `.png` 后缀
- `Batch_Shot_Renamer` - 批量替换时间线轨道上的 Clip Name
- `Batch_Shot_Sequential` - 按顺序递增命名时间线轨道片段
- `Timeline_Shot_to_PNG` - 根据时间线轨道生成透明 PNG + FCP 7 XML v5
- `ShotTrackTools_Configurator` - 外部参数配置 GUI 工具
- 完整的 `README.md` 安装与使用说明文档
