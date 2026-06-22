#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch Shot Sequential - 批量顺序递增命名时间线轨道上的 Clip Name
支持：从外部配置文件读取参数，无需修改脚本文件

版本: v1.0.1

修改逻辑：只修改时间线片段的显示名（SetName），不修改媒体池名称
避免素材复用导致所有引用同步变更的问题

使用方法：
1. 双击运行 ShotTrackTools_Configurator.py 配置参数
2. 在达芬奇中运行：Workspace > Scripts > Utility > ShotTrackTools > Batch_Shot_Sequential
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
    "prefix": "2Esq1400_",
    "start": 10,
    "step": 10,
    "padding": 4,
    "remove_suffix": True,
}
_SCHEMA = {
    "track": ("seq_track", str),
    "prefix": ("seq_prefix", str),
    "start": ("seq_start", int),
    "step": ("seq_step", int),
    "padding": ("seq_padding", int),
    "remove_suffix": ("seq_remove_suffix", None),
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
    print("前缀: {} | 起始: {} | 步长: {} | 位数: {}".format(
        cfg["prefix"], cfg["start"], cfg["step"], cfg["padding"]))
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

        # 顺序递增命名
        num = cfg["start"] + (i * cfg["step"])
        new_name = "{}{}".format(cfg["prefix"], str(num).zfill(cfg["padding"]))

        if new_name != old_name:
            # 只修改时间线片段的显示名，不修改媒体池
            item.SetName(new_name)
            print("  {} -> {}".format(working, new_name))
            renamed += 1
        else:
            print("  [无变化] {}".format(old_name))

    print("-" * 40)
    print("完成：共 {} 个片段，重命名 {} 个。".format(len(items), renamed))
    print("说明：只修改了时间线显示名，媒体池中的原始文件名未变更。")


if __name__ == "__main__":
    main()
