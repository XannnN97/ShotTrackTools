#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Remove PNG Suffix - 批量去掉媒体池内所有片段的 .png 后缀
Workflow Integration 版本，返回日志列表而非直接打印
"""


def run(resolve):
    """
    执行后缀清理

    Args:
        resolve: DaVinci Resolve 对象

    Returns:
        list[str]: 日志信息列表
    """
    logs = []
    project = resolve.GetProjectManager().GetCurrentProject()
    if not project:
        logs.append("[ERROR] No project is currently open.")
        return logs

    mediaPool = project.GetMediaPool()
    folder = mediaPool.GetCurrentFolder()
    if not folder:
        logs.append("[ERROR] Could not get current media pool folder.")
        return logs

    clips = folder.GetClipList()
    if not clips:
        logs.append("[INFO] No clips found in current folder.")
        return logs

    renamed_count = 0
    undo_items = []
    for clip in clips:
        name = clip.GetClipProperty("Clip Name")
        if name and name.endswith(".png"):
            new_name = name[:-4]
            undo_items.append({"originalName": name, "newName": new_name})
            clip.SetClipProperty("Clip Name", new_name)
            renamed_count += 1
            logs.append("  Renamed: {} -> {}".format(name, new_name))

    logs.append("-" * 40)
    logs.append("Done! {} clip(s) renamed in '{}'.".format(renamed_count, folder.GetName()))
    return {
        "logs": logs,
        "undoData": {
            "type": "remove_suffix",
            "folderName": folder.GetName(),
            "items": undo_items
        }
    }
