#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch Sequential - 批量顺序递增命名时间线轨道上的 Clip Name
Workflow Integration 版本，返回日志列表而非直接打印
"""

import os

from shottracktools_utils import parse_track


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


def run(resolve, cfg):
    """
    执行顺序递增命名

    Args:
        resolve: DaVinci Resolve 对象
        cfg (dict): 配置参数

    Returns:
        list[str]: 日志信息列表
    """
    logs = []
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    if not timeline:
        logs.append("[ERROR] No open timeline. Please open a timeline first.")
        return logs

    logs.append("Timeline: {}".format(timeline.GetName()))
    logs.append("Target track: {}".format(cfg["track"]))
    logs.append("Prefix: {} | Start: {} | Step: {} | Padding: {}".format(
        cfg["prefix"], cfg["start"], cfg["step"], cfg["padding"]))
    logs.append("Remove suffix: {}".format(cfg["remove_suffix"]))
    logs.append("-" * 40)

    try:
        track_type, track_idx = parse_track(cfg["track"])
    except ValueError as e:
        logs.append("[ERROR] {}".format(str(e)))
        return logs

    items = timeline.GetItemListInTrack(track_type, track_idx)
    if not items:
        logs.append("[ERROR] No clips on {} track".format(cfg["track"]))
        return logs

    logs.append("{} track has {} clip(s)".format(cfg["track"], len(items)))
    items = sorted(items, key=lambda x: x.GetStart())
    renamed = 0
    undo_items = []

    for i, item in enumerate(items):
        name = item.GetName()
        if not name:
            name = item.GetProperty("Clip Name")
        if not name:
            logs.append("  [SKIP] Failed to get name for clip #{}".format(i + 1))
            continue

        old_name = name
        working = os.path.splitext(old_name)[0] if cfg["remove_suffix"] else old_name

        # 记录原始名称
        undo_items.append({"start": item.GetStart(), "originalName": old_name})

        num = cfg["start"] + (i * cfg["step"])
        new_name = "{}{}".format(cfg["prefix"], str(num).zfill(cfg["padding"]))

        if new_name != old_name:
            item.SetName(new_name)
            logs.append("  {} -> {}".format(working, new_name))
            renamed += 1
        else:
            logs.append("  [UNCHANGED] {}".format(old_name))

    logs.append("-" * 40)
    logs.append("Done: {} clips total, {} renamed.".format(len(items), renamed))
    logs.append("Note: Only timeline display names were changed, Media Pool unchanged.")
    return {
        "logs": logs,
        "undoData": {
            "type": "sequential",
            "track": cfg["track"],
            "items": undo_items
        }
    }
