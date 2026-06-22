#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch Shot Renamer - 批量替换时间线轨道上的 Clip Name
支持：从外部配置文件读取参数，无需修改脚本文件

修改逻辑：只修改时间线片段的显示名（SetName），不修改媒体池名称
避免素材复用导致所有引用同步变更的问题

使用方法：
1. 双击运行 ShotTrackTools_Configurator.py 配置参数
2. 在达芬奇中运行：Workspace > Scripts > Utility > ShotTrackTools > Batch_Shot_Renamer
3. 查看 Console（Py3）输出日志
"""

import os
import json

if 'resolve' not in globals():
    import DaVinciResolveScript as dvr
    resolve = dvr.scriptapp("Resolve")


# ==================== 默认参数 ====================
DEFAULT_CONFIG = {
    "track": "V10",
    "search": "sq1300",
    "replace": "sq1400",
    "remove_suffix": True,
}
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".shottracktools", "config.json")
# =================================================


def get_params():
    """读取配置文件，如果不存在则使用默认参数"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
            print("[Config] 已读取配置文件:", CONFIG_FILE)
            return {
                "track": str(config.get("track", DEFAULT_CONFIG["track"])),
                "search": str(config.get("search", DEFAULT_CONFIG["search"])),
                "replace": str(config.get("replace", DEFAULT_CONFIG["replace"])),
                "remove_suffix": config.get("remove_suffix", DEFAULT_CONFIG["remove_suffix"]),
            }
        except Exception as e:
            print("[Config] 读取配置文件失败: {}".format(str(e)))
            print("[Config] 将使用默认参数")
    else:
        print("[Config] 配置文件不存在，使用默认参数")
        print("[Config] 提示：运行 ShotTrackTools_Configurator.py 可配置参数")
    return DEFAULT_CONFIG


def parse_track(track_str):
    """解析 V10 / A1 格式为 (track_type, track_index)"""
    track_str = track_str.strip().upper()
    if not track_str or track_str[0] not in ("V", "A"):
        raise ValueError("轨道格式错误，请使用 V10 / V1 / A1")
    try:
        idx = int(track_str[1:])
    except ValueError:
        raise ValueError("轨道号必须是数字")
    return ("video" if track_str[0] == "V" else "audio", idx)


def main():
    cfg = get_params()

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

    track_type, track_idx = parse_track(cfg["track"])
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
