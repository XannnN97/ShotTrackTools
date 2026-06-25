#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ShotTrackTools 公共工具模块 (Workflow Integration v1.1.0)
提供配置读写、轨道解析、版本号等共享功能
"""

__version__ = "1.2.0"

import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".shottracktools")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def get_resolve():
    """获取 DaVinci Resolve 对象，支持外部执行"""
    if 'resolve' in globals():
        return resolve
    import sys
    _main = sys.modules.get('__main__')
    if _main is not None:
        _main_resolve = getattr(_main, 'resolve', None)
        if _main_resolve is not None:
            return _main_resolve

    # 尝试从外部 Python 进程连接 Resolve
    import sys
    import os

    # 添加 Resolve Scripting 模块路径到 sys.path
    resolve_script_modules = os.path.join(
        os.environ.get('PROGRAMDATA', 'C:\\ProgramData'),
        'Blackmagic Design', 'DaVinci Resolve', 'Support', 'Developer', 'Scripting', 'Modules'
    )
    if resolve_script_modules not in sys.path:
        sys.path.insert(0, resolve_script_modules)

    try:
        import DaVinciResolveScript as dvr
        resolve = dvr.scriptapp("Resolve")
        if resolve:
            return resolve
    except ImportError:
        pass

    return None


def load_config():
    """读取 ShotTrackTools 配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("[Config] 读取配置文件失败: {}".format(str(e)))
    return {}


def save_config(config):
    """保存 ShotTrackTools 配置文件"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def parse_track(track_str):
    """
    解析轨道字符串，如 V10 / A1 格式为 (track_type, track_index)
    Args:
        track_str (str): 轨道字符串，如 "V10" 或 "A1"
    Returns:
        tuple: ("video" | "audio", int) 轨道类型和索引
    Raises:
        ValueError: 格式错误时抛出
    """
    track_str = track_str.strip().upper()
    if not track_str or track_str[0] not in ("V", "A"):
        raise ValueError("轨道格式错误，请使用 V10 / V1 / A1")
    try:
        idx = int(track_str[1:])
    except ValueError:
        raise ValueError("轨道号必须是数字")
    return ("video" if track_str[0] == "V" else "audio", idx)


def get_timeline_info():
    """
    获取当前时间线和轨道列表信息
    Returns:
        dict: {"timelineName": str, "tracks": ["V1", "V2", "A1", ...]} 或 None
    """
    resolve = get_resolve()
    if not resolve:
        return None
    project = resolve.GetProjectManager().GetCurrentProject()
    if not project:
        return None
    timeline = project.GetCurrentTimeline()
    if not timeline:
        return None

    tracks = []
    # 获取视频轨道
    for i in range(1, 20):
        try:
            items = timeline.GetItemListInTrack("video", i)
            if items is not None:
                tracks.append("V{}".format(i))
        except Exception:
            break
    # 获取音频轨道
    for i in range(1, 20):
        try:
            items = timeline.GetItemListInTrack("audio", i)
            if items is not None:
                tracks.append("A{}".format(i))
        except Exception:
            break

    return {
        "timelineName": timeline.GetName(),
        "tracks": tracks
    }
