#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch Renamer - 批量替换时间线轨道上的 Clip Name
Workflow Integration 版本，返回日志列表而非直接打印
"""

import os

from shottracktools_utils import parse_track


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


def run(resolve, cfg):
    """
    执行批量替换

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
    logs.append("Search: '{}' -> Replace: '{}'".format(cfg["search"], cfg["replace"]))
    logs.append("Remove suffix: {}".format(cfg["remove_suffix"]))
    logs.append("-" * 40)

    try:
        track_type, track_idx = parse_track(cfg["track"])
    except ValueError as e:
        logs.append("[ERROR] {}".format(str(e)))
        return logs

    items = timeline.GetItemListInTrack(track_type, track_idx)
    if not items:
        logs.append("[INFO] 您选择的轨道 {} 目前没有素材，请检查正确的目标轨道".format(cfg["track"]))
        return {"logs": logs, "undoData": None}

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

        # 记录原始名称（含起始/结束帧，用于撤回双键匹配）
        undo_items.append({"start": item.GetStart(), "end": item.GetEnd(), "originalName": old_name})

        if cfg["search"] in working:
            new_name = working.replace(cfg["search"], cfg["replace"])
            if new_name != old_name:
                item.SetName(new_name)
                logs.append("  {} -> {}".format(working, new_name))
                renamed += 1
            else:
                logs.append("  [UNCHANGED] {}".format(old_name))
        else:
            logs.append("  [SKIP] '{}' not found in {}".format(cfg["search"], working))

    logs.append("-" * 40)
    logs.append("Done: {} clips total, {} renamed.".format(len(items), renamed))
    logs.append("Note: Only timeline display names were changed, Media Pool unchanged.")
    return {
        "logs": logs,
        "undoData": {
            "type": "renamer",
            "track": cfg["track"],
            "items": undo_items
        }
    }
