#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ShotTrackTools Backend - Python execution engine
Receives stdin JSON, executes action, returns JSON result
"""

import sys
import json
import os

resolve_script_modules = os.path.join(
    os.environ.get('PROGRAMDATA', 'C:\\ProgramData'),
    'Blackmagic Design', 'DaVinci Resolve', 'Support', 'Developer', 'Scripting', 'Modules'
)
if resolve_script_modules not in sys.path:
    sys.path.insert(0, resolve_script_modules)

from shottracktools_utils import parse_track
from lib import renamer, sequential, png_exporter, remove_suffix


def get_resolve():
    if 'resolve' in globals():
        return resolve
    _main = sys.modules.get('__main__')
    if _main is not None:
        _r = getattr(_main, 'resolve', None)
        if _r is not None:
            return _r
    try:
        import DaVinciResolveScript as dvr
        return dvr.scriptapp("Resolve")
    except ImportError:
        return None


def execute(type, params):
    resolve = get_resolve()
    if not resolve:
        return {"success": False, "logs": ["[ERROR] Cannot connect to DaVinci Resolve"]}

    if type == "batch_renamer":
        r = renamer.run(resolve, params)
        return {"success": True, "logs": r["logs"], "undoData": r.get("undoData")}
    elif type == "batch_sequential":
        r = sequential.run(resolve, params)
        return {"success": True, "logs": r["logs"], "undoData": r.get("undoData")}
    elif type == "png_export":
        r = png_exporter.run(resolve, params)
        return {"success": True, "logs": r if isinstance(r, list) else r["logs"]}
    elif type == "remove_suffix":
        r = remove_suffix.run(resolve)
        return {"success": True, "logs": r["logs"], "undoData": r.get("undoData")}
    else:
        return {"success": False, "logs": ["[ERROR] Unknown type: {}".format(type)]}


def undo(undoData):
    resolve = get_resolve()
    if not resolve:
        return {"success": False, "logs": ["[ERROR] Cannot connect to DaVinci Resolve"]}

    logs = []
    type = undoData.get("type")

    if type in ("renamer", "sequential"):
        track_str = undoData.get("track")
        try:
            track_type, track_idx = parse_track(track_str)
        except ValueError as e:
            return {"success": False, "logs": ["[ERROR] {}".format(str(e))]}

        project = resolve.GetProjectManager().GetCurrentProject()
        timeline = project.GetCurrentTimeline()
        if not timeline:
            return {"success": False, "logs": ["[ERROR] No open timeline"]}

        items = timeline.GetItemListInTrack(track_type, track_idx)
        if not items:
            return {"success": False, "logs": ["[ERROR] No clips on track"]}

        start_map = {item["start"]: item["originalName"] for item in undoData.get("items", [])}
        restored = 0
        for item in items:
            start = item.GetStart()
            if start in start_map:
                original_name = start_map[start]
                current_name = item.GetName()
                if current_name != original_name:
                    item.SetName(original_name)
                    logs.append("  Restored: {} -> {}".format(current_name, original_name))
                    restored += 1
        logs.append("-" * 40)
        logs.append("Undo done: {} clip(s) restored.".format(restored))

    elif type == "remove_suffix":
        project = resolve.GetProjectManager().GetCurrentProject()
        if not project:
            return {"success": False, "logs": ["[ERROR] No open project"]}
        mediaPool = project.GetMediaPool()
        folder = mediaPool.GetCurrentFolder()
        if not folder:
            return {"success": False, "logs": ["[ERROR] No current folder"]}

        name_map = {item["newName"]: item["originalName"] for item in undoData.get("items", [])}
        restored = 0
        for clip in folder.GetClipList():
            name = clip.GetClipProperty("Clip Name")
            if name in name_map:
                original = name_map[name]
                clip.SetClipProperty("Clip Name", original)
                logs.append("  Restored: {} -> {}".format(name, original))
                restored += 1
        logs.append("-" * 40)
        logs.append("Undo done: {} clip(s) restored.".format(restored))

    return {"success": True, "logs": logs}


def main():
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        print(json.dumps({"success": False, "logs": ["[ERROR] Invalid JSON: {}".format(str(e))]}))
        return

    action = data.get("action")
    if action == "execute":
        result = execute(data.get("type"), data.get("params", {}))
    elif action == "undo":
        result = undo(data.get("undoData", {}))
    else:
        result = {"success": False, "logs": ["[ERROR] Unknown action: {}".format(action)]}

    print(json.dumps(result))


if __name__ == "__main__":
    main()
