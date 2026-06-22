# ShotTrackTools 安装与使用说明文档

> 版本：v1.0  
> 适用软件：DaVinci Resolve 21  
> 操作系统：Windows 10/11

---

## 一、工具包简介

ShotTrackTools 是一套用于 DaVinci Resolve 的辅助脚本，专为 VFX/剪辑交接工作流设计，解决镜头号管理中的批量命名、后缀清理、透明 PNG 占位符生成等问题。

### 包含工具

| 工具 | 文件名 | 功能 |
|------|--------|------|
| **remove_png_suffix** | `remove_png_suffix.py` | 批量去掉媒体池内所有片段的 `.png` 后缀 |
| **Batch_Shot_Renamer** | `Batch_Shot_Renamer.py` | 批量替换时间线片段的 Clip Name（如 `sq1300` → `sq1400`） |
| **Batch_Shot_Sequential** | `Batch_Shot_Sequential.py` | 按顺序递增命名（如 `0010`, `0020`, `0030`...） |
| **Timeline_Shot_to_PNG** | `Timeline_Shot_to_PNG.py` | 根据时间线轨道生成透明 PNG + FCP 7 XML v5 |
| **ShotTrackTools_Configurator** | `ShotTrackTools_Configurator.py` | 外部参数配置工具（带 GUI 窗口） |

---

## 二、安装步骤

### 2.1 系统要求

- **DaVinci Resolve 21**（免费版或 Studio 版均可）
- **Python 3.6+**（64位）
- **Pillow**（Python 图像库，用于生成 PNG）

### 2.2 安装 Python 3

1. 访问 https://www.python.org/downloads/
2. 下载并安装 **Python 3.11+**（安装时勾选 **"Add Python to PATH"**）
3. 打开 **CMD** 或 **PowerShell**，验证安装：
   ```cmd
   python --version
   ```
   应显示类似 `Python 3.11.4`

### 2.3 安装 Pillow

在 CMD 或 PowerShell 中运行：

```cmd
pip install pillow
```

安装成功后，应提示 `Successfully installed pillow-x.x.x`。

### 2.4 安装脚本到达芬奇

将本文件夹内的 **所有 `.py` 文件**复制到以下路径：

```
%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\ShotTrackTools
```

**快速打开路径的方法**：
1. 按 `Win + R`，输入 `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility`，按回车
2. 在打开的文件夹中，**新建文件夹** `ShotTrackTools`
3. 将以下文件复制进去：
   - `remove_png_suffix.py`
   - `Batch_Shot_Renamer.py`
   - `Batch_Shot_Sequential.py`
   - `Timeline_Shot_to_PNG.py`
   - `ShotTrackTools_Configurator.py`

### 2.5 重启达芬奇

复制完成后，**必须关闭并重新打开 DaVinci Resolve**，脚本菜单只在启动时扫描。

### 2.6 验证安装

打开达芬奇，点击菜单栏：

**Workspace → Scripts → Utility → ShotTrackTools**

应显示以下 5 个脚本：
- `remove_png_suffix`
- `Batch_Shot_Renamer`
- `Batch_Shot_Sequential`
- `Timeline_Shot_to_PNG`
- `ShotTrackTools_Configurator`

---

## 三、使用说明

### 3.1 通用使用流程（所有含参数的脚本）

所有需要参数的脚本（`Batch_Shot_Renamer`、`Batch_Shot_Sequential`、`Timeline_Shot_to_PNG`）采用以下统一的工作流程：

#### 步骤 1：配置参数（只需运行一次）

运行 **`ShotTrackTools_Configurator`** 脚本（在达芬奇中运行，或双击文件夹中的 `.py` 文件），在弹出的 GUI 窗口中填写参数，点击 **保存配置**。

参数会保存到 `C:\Users\你的用户名\.shottracktools\config.json`。

#### 步骤 2：运行脚本

在达芬奇中打开目标时间线，点击对应的脚本运行。脚本会自动读取配置文件中的参数，无需手动修改代码。

---

### 3.2 remove_png_suffix（去掉后缀）

**用途**：导入 PNG 占位符到媒体池后，去掉 `.png` 后缀，使 Clip Name 显示纯净镜头号。

**使用步骤**：
1. 在达芬奇中，切换到 **媒体（Media）** 页面
2. 在媒体池中选中需要处理的文件夹
3. 点击 **Workspace → Scripts → Utility → ShotTrackTools → remove_png_suffix**
4. 在 **Console（Py3）** 中查看输出结果

**效果**：所有以 `.png` 结尾的 Clip Name 会去掉后缀，如 `2Esq1400_0010.png` → `2Esq1400_0010`

---

### 3.3 Batch_Shot_Renamer（批量替换）

**用途**：将时间线轨道上所有片段名称中的指定文本批量替换为另一文本。

**示例**：将 `V10` 轨道上所有 `sq1300` 替换为 `sq1400`，保留后续编号不变。

**配置参数**（在 Configurator 中设置）：
- **目标轨道**：如 `V10`
- **查找内容**：如 `sq1300`
- **替换为**：如 `sq1400`
- **去掉文件后缀**：勾选则先去掉 `.png`/`.mov` 再替换

**使用步骤**：
1. 在 Configurator 中配置参数 → 保存
2. 在达芬奇中打开目标时间线
3. 点击 **Batch_Shot_Renamer**
4. 查看 Console 输出确认结果

---

### 3.4 Batch_Shot_Sequential（顺序递增命名）

**用途**：按固定格式和步长对时间线轨道上的片段进行递增命名。

**示例**：`2Esq1400_0010`, `2Esq1400_0020`, `2Esq1400_0030`...（步长 10，位数 4）

**配置参数**（在 Configurator 中设置）：
- **目标轨道**：如 `V10`
- **前缀**：如 `2Esq1400_`
- **起始编号**：如 `10`
- **步长**：如 `10`
- **编号位数**：如 `4`（生成 `0010`, `0020`）
- **去掉文件后缀**：勾选则先去掉 `.png`/`.mov`

**使用步骤**：
1. 在 Configurator 中配置参数 → 保存
2. 在达芬奇中打开目标时间线
3. 点击 **Batch_Shot_Sequential**
4. 查看 Console 输出确认结果

---

### 3.5 Timeline_Shot_to_PNG（PNG + XML 生成）

**用途**：读取时间线轨道上的片段列表，生成透明 PNG 占位符 + FCP 7 XML v5，可直接导入达芬奇重建一条轨道。

**配置参数**（在 Configurator 中设置）：
- **目标轨道**：如 `V10`
- **输出目录**：PNG 和 XML 的保存路径（留空则使用桌面）
- **去掉文件后缀**：勾选则去掉 `.png`/`.mov`

**使用步骤**：
1. 在 Configurator 中配置参数 → 保存
2. 在达芬奇中打开目标时间线
3. 点击 **Timeline_Shot_to_PNG**
4. 在 Console 中查看输出，确认生成文件
5. 前往输出目录，确认以下文件已生成：
   - `xxx.png`（每个片段对应一个透明 PNG）
   - `shot_track.xml`（FCP 7 XML v5，可导入达芬奇）
6. 在达芬奇中导入 XML：**File → Import → Timeline**，选择 `shot_track.xml`
7. 选择导入到 **新时间线** 或 **现有时间线**

**注意事项**：
- 确保 PNG 文件路径与 XML 中的 `pathurl` 一致（如果移动了 PNG 文件位置，需重新生成 XML）
- 导入 XML 时，如果提示 "当前XML版本是1.0"，说明版本不兼容，请使用最新脚本重新生成

---

## 四、团队分发说明

### 分发步骤

1. 确保团队电脑已安装：
   - Python 3.6+（64位）
   - Pillow（`pip install pillow`）

2. 将本文件夹内的 **5 个 `.py` 文件**复制到达芬奇 Scripts 目录：
   ```
   %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\ShotTrackTools
   ```

3. 重启达芬奇，验证菜单中出现 ShotTrackTools

4. 首次使用时运行 **ShotTrackTools_Configurator** 配置参数即可

---

## 五、常见问题

### Q1：运行脚本时提示 "[Config] 配置文件不存在"

**原因**：尚未运行 ShotTrackTools_Configurator 配置参数。  
**解决**：先运行 **ShotTrackTools_Configurator**，填写参数后点击 **保存配置**，然后再运行其他脚本。

### Q2：运行脚本时提示 "没有打开的时间线"

**原因**：运行脚本时，达芬奇中没有当前打开的时间线。  
**解决**：在达芬奇中打开一个项目和时间线，然后再运行脚本。

### Q3：运行脚本时提示 "错误：V10 轨道上没有片段"

**原因**：配置的目标轨道（如 `V10`）在当前时间线上没有片段。  
**解决**：检查时间线中该轨道是否有素材，或在 Configurator 中修改目标轨道为实际存在的轨道（如 `V1`）。

### Q4：Timeline_Shot_to_PNG 提示 Pillow 未安装

**原因**：Python 环境中缺少 Pillow 库。  
**解决**：在 CMD 中运行 `pip install pillow`，然后重新运行脚本。

### Q5：导入 XML 后 PNG 文件显示离线（红色）

**原因**：PNG 文件被移动了位置，或 XML 中的 `pathurl` 与实际路径不一致。  
**解决**：
- 方法 A：将 PNG 文件移回 XML 中指定的路径
- 方法 B：重新运行 `Timeline_Shot_to_PNG` 生成新的 PNG 和 XML（确保输出目录正确）

### Q6：脚本在达芬奇中无法运行（没有任何反应）

**原因**：可能脚本路径错误，或文件未正确复制。  
**解决**：
1. 确认文件在 `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\ShotTrackTools` 中
2. 确认文件扩展名是 `.py`（不是 `.py.txt`）
3. 重启达芬奇

### Q7：ShotTrackTools_Configurator 的窗口打不开

**原因**：Python 的 tkinter 模块在某些精简安装中可能缺失。  
**解决**：重新安装 Python 时选择 **"Install for all users"** 并勾选 **tcl/tk and IDLE** 选项。

---

## 六、文件清单

```
ShotTrackTools/
  ├── README.md                          # 本说明文档
  ├── remove_png_suffix.py              # 去掉媒体池后缀（无参数）
  ├── Batch_Shot_Renamer.py            # 批量替换 Clip Name（读取配置）
  ├── Batch_Shot_Sequential.py         # 顺序递增命名（读取配置）
  ├── Timeline_Shot_to_PNG.py          # 生成 PNG + XML（读取配置）
  └── ShotTrackTools_Configurator.py   # 参数配置 GUI 工具
```

---

## 七、技术支持

本工具包基于 DaVinci Resolve Python API 开发，受限于 API 本身的功能范围。如果遇到 API 无法支持的额外需求（如通过脚本自动切割时间线片段），需要在达芬奇中手动完成。

如有问题，请检查：
1. 达芬奇 Console（Py3）中的输出日志
2. 本说明文档中的常见问题部分
3. 确认脚本文件路径正确
