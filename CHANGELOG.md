# ShotTrackTools 更新日志

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
