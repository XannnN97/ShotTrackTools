#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EDL Exporter - 生成 CMX3600 格式 EDL 文件
从目标轨道读取时间线片段信息，生成标准 EDL
"""

import os

from shottracktools_utils import parse_track


_DEFAULTS = {
    "track": "V1",
    "output_dir": "",
    "filename": "shot_track",
}
_SCHEMA = {
    "track": ("edl_track", str),
    "output_dir": ("output_dir", str),
    "filename": ("edl_filename", str),
}


def frames_to_timecode(frames, fps):
    """将帧数转换为 HH:MM:SS:FF 时间码"""
    total_seconds = frames / fps
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    fr = int(frames % fps)
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, fr)


def generate_edl(timeline, track_items, output_dir, filename, fps):
    """生成 CMX3600 EDL 文件"""
    timeline_name = timeline.GetName()
    edl_path = os.path.join(output_dir, "{}.edl".format(filename))

    edl_lines = []
    edl_lines.append("TITLE: {}".format(timeline_name))
    edl_lines.append("FCM: NON-DROP FRAME")
    edl_lines.append("")

    for i, item in enumerate(track_items):
        event_num = str(i + 1).zfill(3)
        name = item.GetName()
        if not name:
            name = item.GetProperty("Clip Name")
        if not name:
            continue

        start = item.GetStart()
        end = item.GetEnd()
        duration = end - start

        # 时间码
        tc_in = frames_to_timecode(start, fps)
        tc_out = frames_to_timecode(end, fps)
        # 源时间码（占位符 PNG 无源时间码，使用与记录相同）
        src_in = tc_in
        src_out = tc_out

        # 素材名称截断到约 8 字符（EDL 格式限制）
        reel_name = name[:8] if len(name) > 8 else name.ljust(8)

        # EDL 事件行：001  REELNAME  V  C  00:00:00:00 00:00:01:14 00:00:00:00 00:00:01:14
        edl_lines.append("{}    {} V C        {} {} {} {}".format(
            event_num, reel_name, src_in, src_out, tc_in, tc_out
        ))
        # FROM CLIP NAME 注释
        edl_lines.append("* FROM CLIP NAME: {}".format(name))
        edl_lines.append("")

    with open(edl_path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\r\n".join(edl_lines))

    return edl_path


def run(resolve, cfg):
    """
    执行 EDL 导出

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

    # 确定输出目录
    output_dir = cfg["output_dir"]
    if not output_dir:
        output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    os.makedirs(output_dir, exist_ok=True)

    # 检查目录可写性
    if not os.access(output_dir, os.W_OK):
        logs.append("[ERROR] Output directory is not writable: {}".format(output_dir))
        return logs

    # 获取帧率
    try:
        fps = float(timeline.GetSetting("timelineFrameRate"))
    except:
        try:
            fps = float(project.GetSetting("timelineFrameRate"))
        except:
            fps = 24.0
            logs.append("[WARNING] Unable to get timeline framerate, defaulting to 24fps")

    logs.append("Timeline: {}".format(timeline.GetName()))
    logs.append("Target track: {}".format(cfg["track"]))
    logs.append("Output directory: {}".format(output_dir))
    logs.append("Timeline FPS: {}".format(fps))
    logs.append("-" * 40)

    try:
        track_type, track_idx = parse_track(cfg["track"])
    except ValueError as e:
        logs.append("[ERROR] {}".format(str(e)))
        return logs

    items = timeline.GetItemListInTrack(track_type, track_idx)
    if not items:
        logs.append("[INFO] 您选择的轨道 {} 目前没有素材，请检查正确的目标轨道".format(cfg["track"]))
        return logs

    logs.append("{} track has {} clip(s)".format(cfg["track"], len(items)))
    items = sorted(items, key=lambda x: x.GetStart())

    filename = cfg.get("filename", "shot_track")
    edl_path = generate_edl(timeline, items, output_dir, filename, fps)
    logs.append("[EDL] {}".format(edl_path))

    logs.append("-" * 40)
    logs.append("Done! {} clips exported".format(len(items)))
    logs.append("EDL: {}".format(edl_path))
    logs.append("Output directory: {}".format(output_dir))

    return logs
