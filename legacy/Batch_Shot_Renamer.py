#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch Shot Renamer - 批量替换时间线轨道上的 Clip Name
支持：从外部配置文件读取参数，无需修改脚本文件

版本: v1.0.1

修改逻辑：只修改时间线片段的显示名（SetName），不修改媒体池名称
避免素材复用导致所有引用同步变更的问题

使用方法：
1. 双击运行 ShotTrackTools_Configurator.py 配置参数
2. 在达芬奇中运行：Workspace > Scripts > Utility > ShotTrackTools > Batch_Shot_Renamer
3. 查看 Console（Py3）输出日志
"""

import os
import sys

# 确保能导入同级目录的公共模块
_script_dir = None
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # 在达芬奇中运行时 __file__ 可能未定义
    if hasattr(sys, 'argv') and sys.argv:
        _script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    if not _script_dir:
        _script_dir = os.getcwd()
if _script_dir and _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

import shottracktools_utils as stu

resolve = stu.get_resolve()


# ==================== 默认参数 ====================
_DEFAULTS = {
    "track": "V10",
    "search": "sq1300",
    "replace": "sq1400",
    "remove_suffix": True,
}
_SCHEMA = {
    "track": ("track", str),
    "search": ("search", str),
    "replace": ("replace", str),
    "remove_suffix": ("remove_suffix", None),
}
# =================================================


def main():
    cfg = stu.get_params(_SCHEMA, _DEFAULTS)

    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("错误：没有打开的时间线，请先打开一个时间线")
        return

    print("时间线:", timeline.GetName())
    print("目标轨道:", cfg["track"])
    print("查找: '{}' -> 替换: '{}'".format(cfg["search"], cfg["replace"]))
    print("去掉后缀:", cfg["remove_suffix"])
    print("-" * 40)

    track_type, track_idx = stu.parse_track(cfg["track"])
    items = timeline.GetItemListInTrack(track_type, track_idx)
    if not items:
        print("错误：{} 轨道上没有片段".format(cfg["track"]))
        return

    print("{} 轨道共 {} 个片段".format(cfg["track"], len(items)))
    items = sorted(items, key=lambda x: x.GetStart())
    renamed = 0

    for i, item in enumerate(items):
        name = item.GetName()
        if not name:
            name = item.GetProperty("Clip Name")
        if not name:
            print("  [跳过] 第 {} 个片段名称获取失败".format(i + 1))
            continue

        old_name = name
        working = os.path.splitext(old_name)[0] if cfg["remove_suffix"] else old_name

        if cfg["search"] in working:
            new_name = working.replace(cfg["search"], cfg["replace"])
            if new_name != old_name:
                # 只修改时间线片段的显示名，不修改媒体池
                item.SetName(new_name)
                print("  {} -> {}".format(working, new_name))
                renamed += 1
            else:
                print("  [无变化] {}".format(old_name))
        else:
            print("  [跳过] {} 中未找到 '{}'".format(working, cfg["search"]))

    print("-" * 40)
    print("完成：共 {} 个片段，重命名 {} 个。".format(len(items), renamed))
    print("说明：只修改了时间线显示名，媒体池中的原始文件名未变更。")


if __name__ == "__main__":
    main()
