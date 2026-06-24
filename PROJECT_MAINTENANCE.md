# ShotTrackTools 项目维护标准

> 每次项目维护（开发、修复、迭代）完成后，必须按此清单逐项检查。

---

## 一、提交前检查清单

### 1. 代码完整性检查

- [ ] 新增/修改的文件是否在预期的目录中？
- [ ] 根目录是否仍然保持整洁（无散落文件）？
- [ ] `legacy/` 目录中的旧文件是否被意外修改？
- [ ] 是否有临时文件残留（`.pyc`, `__pycache__/`, `.pyc`, `.pyo`）？

### 2. `.gitignore` 合规检查

- [ ] `.gitignore` 的排除规则是否过于宽泛？（如 `*.xml`, `*.png` 等）
- [ ] 排除规则是否误伤了项目必需的源文件或配置文件？
- [ ] 用户运行产物（如 Desktop 上的 PNG/XML）是否真的需要排除？（通常不在项目目录中）
- [ ] 使用 `git ls-files --others --ignored --exclude-standard` 检查是否有被错误忽略的文件
- [ ] 使用 `git ls-files` 确认所有必需文件已跟踪

### 3. 文档同步检查

- [ ] `CHANGELOG.md` 是否更新了本次修改？
- [ ] `README.md` 是否反映了最新功能/安装方式？
- [ ] 版本号是否在所有相关文件一致？（`shottracktools_utils.py`, `manifest.xml`, `package.json`）
- [ ] 如果修改了文件结构，README 中的文件树是否同步？
- [ ] 中英文文档是否同时更新？

### 4. 测试与验证

- [ ] 单元测试是否通过？（`py -3 test_shottracktools.py`）
- [ ] 修改的功能是否在实际环境中验证？
- [ ] 相关功能是否受本次修改影响？（回归检查）
- [ ] 如果修改了后端，前端是否同步适配？

### 5. Git 提交规范

- [ ] 提交信息是否遵循 `<type>: <description>` 格式？
- [ ] 提交是否原子化？（一个 commit 只做一件事）
- [ ] 提交后工作树是否干净？（`git status` 无未跟踪文件）
- [ ] 提交是否已推送到 GitHub？
- [ ] GitHub 仓库是否与本地一致？（`git log` 对比）

---

## 二、提交后检查清单

### 6. GitHub 远程验证

- [ ] 在 GitHub 网页上确认所有修改的文件已推送
- [ ] 检查被修改的文件列表是否完整（无遗漏）
- [ ] 检查 `README.md` 在 GitHub 上的渲染效果
- [ ] 检查 CHANGELOG 的 Markdown 格式是否正确

### 7. Issue 管理

- [ ] 本次修复是否关联了 GitHub Issue？
- [ ] 已修复的 Issue 是否在 GitHub 上关闭？
- [ ] 关闭 Issue 时是否添加了修复说明和 commit 引用？
- [ ] 未修复的 Issue 是否已更新状态/进度？

---

## 三、版本发布检查清单（仅在发布新版本时执行）

- [ ] 版本号在 `__version__`, `manifest.xml`, `package.json`, `CHANGELOG.md` 中是否一致？
- [ ] 是否已打 Git 标签？（`git tag v1.x.x`）
- [ ] 是否已推送标签？（`git push origin --tags`）
- [ ] 是否更新了安装指南中的版本引用？
- [ ] 是否有破坏性变更？如有，是否在 CHANGELOG 和 README 中明确说明？

---

## 四、Git 提交信息规范

| 类型 | 用途 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: add undo support` |
| `fix` | Bug 修复 | `fix: resolve XML loop indentation` |
| `docs` | 文档更新 | `docs: update README for v1.1.0` |
| `refactor` | 重构代码 | `refactor: extract shared module` |
| `chore` | 工程化/杂项 | `chore: clean up temp files` |
| `test` | 测试相关 | `test: add PNG generation test` |
| `style` | 代码格式（无逻辑变更） | `style: fix indentation` |

---

## 五、项目目录规范

```
ShotTrackTools/
├── .gitignore              # 只排除编译缓存、IDE、OS、分发目录
├── CHANGELOG.md            # 所有版本变更必须记录
├── LICENSE
├── README.md               # 中英文双语
├── requirements.txt        # 外部依赖声明（无依赖则注明）
├── test_shottracktools.py  # 单元测试
├── PROJECT_MAINTENANCE.md  # 本文件
│
├── legacy/                 # 旧版脚本存档，只读
│   └── ...
│
└── ShotTrackTools_v1.1.0/   # 当前版本插件
    ├── manifest.xml        # 必须在 Git 中，不可被 .gitignore 排除
    ├── package.json
    ├── main.js
    ├── preload.js
    ├── index.html
    ├── app.js
    ├── style.css
    ├── backend.py
    ├── shottracktools_utils.py
    └── lib/
        ├── __init__.py
        ├── renamer.py
        ├── sequential.py
        ├── png_exporter.py
        └── remove_suffix.py
```

---

## 六、常见错误预防

### `.gitignore` 误用
❌ **错误**：`*.xml` — 排除所有 XML 文件，包括 `manifest.xml`
✅ **正确**：不全局排除源代码和配置文件，只排除编译产物和缓存

### 版本号漂移
❌ **错误**：`shottracktools_utils.py` 在多个位置有不同版本号
✅ **正确**：只有一个 `__version__` 定义在 `ShotTrackTools_v1.1.0/shottracktools_utils.py`

### 文档遗漏
❌ **错误**：功能修复后 CHANGELOG 和 README 未更新
✅ **正确**：代码修改和文档修改在同一个 commit 或紧密相邻的 commit 中

---

> 最后更新：2025-06-24
