#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PNG Exporter - 生成透明 PNG 占位符 + FCP 7 XML v5
Workflow Integration 版本，返回日志列表而非直接打印
"""

import os
import json
import struct
import zlib

from shottracktools_utils import parse_track


_DEFAULTS = {
    "track": "V10",
    "output_dir": "",
    "remove_suffix": True,
}
_SCHEMA = {
    "track": ("png_track", str),
    "output_dir": ("output_dir", str),
    "remove_suffix": ("png_remove_suffix", None),
}


def generate_png(filepath):
    """生成 1x1 透明 PNG，纯 Python 标准库实现，无需 Pillow"""
    width = 1
    height = 1
    raw_data = b'\x00\x00\x00\x00'  # RGBA 全透明

    # 扫描行：filter byte 0 + raw data
    scanline = b'\x00' + raw_data
    compressed = zlib.compress(scanline)

    # PNG 签名
    signature = b'\x89PNG\r\n\x1a\n'

    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = _make_chunk(b'IHDR', ihdr_data)

    # IDAT chunk
    idat = _make_chunk(b'IDAT', compressed)

    # IEND chunk
    iend = _make_chunk(b'IEND', b'')

    with open(filepath, 'wb') as f:
        f.write(signature + ihdr + idat + iend)


def _make_chunk(chunk_type, data):
    chunk = chunk_type + data
    crc = zlib.crc32(chunk) & 0xffffffff
    return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)


def generate_fcp7_xml_v5(timeline, track_items, output_dir, fps, remove_suffix):
    """生成 FCP 7 XML v5 文件"""
    timeline_name = timeline.GetName()
    total_duration = max([item.GetEnd() for item in track_items]) if track_items else 0

    xml_lines = []
    xml_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml_lines.append('<xmeml version="5">')
    xml_lines.append('  <project>')
    xml_lines.append('    <name>{}</name>'.format(timeline_name))
    xml_lines.append('    <children>')
    xml_lines.append('      <sequence id="seq-1">')
    xml_lines.append('        <name>{} Shot Track</name>'.format(timeline_name))
    xml_lines.append('        <duration>{}</duration>'.format(total_duration))
    xml_lines.append('        <rate>')
    xml_lines.append('          <timebase>{}</timebase>'.format(fps))
    xml_lines.append('          <ntsc>FALSE</ntsc>')
    xml_lines.append('        </rate>')
    xml_lines.append('        <timecode>')
    xml_lines.append('          <rate>')
    xml_lines.append('            <timebase>{}</timebase>'.format(fps))
    xml_lines.append('            <ntsc>FALSE</ntsc>')
    xml_lines.append('          </rate>')
    xml_lines.append('          <string>00:00:00:00</string>')
    xml_lines.append('          <frame>0</frame>')
    xml_lines.append('          <displayformat>NDF</displayformat>')
    xml_lines.append('        </timecode>')
    xml_lines.append('        <media>')
    xml_lines.append('          <video>')
    xml_lines.append('            <format>')
    xml_lines.append('              <samplecharacteristics>')
    xml_lines.append('                <rate>')
    xml_lines.append('                  <timebase>{}</timebase>'.format(fps))
    xml_lines.append('                  <ntsc>FALSE</ntsc>')
    xml_lines.append('                </rate>')
    xml_lines.append('                <width>1920</width>')
    xml_lines.append('                <height>1080</height>')
    xml_lines.append('                <anamorphic>FALSE</anamorphic>')
    xml_lines.append('                <pixelaspectratio>square</pixelaspectratio>')
    xml_lines.append('                <fielddominance>none</fielddominance>')
    xml_lines.append('              </samplecharacteristics>')
    xml_lines.append('            </format>')
    xml_lines.append('            <track>')

    for i, item in enumerate(track_items):
        name = item.GetName()
        if not name:
            name = item.GetProperty("Clip Name")
        if not name:
            continue

        clean_name = os.path.splitext(name)[0] if remove_suffix else name
        png_filename = "{}.png".format(clean_name)
        png_path = os.path.join(output_dir, png_filename)
        file_url = "file:///" + png_path.replace("\\", "/")

        start = item.GetStart()
        end = item.GetEnd()
        duration = end - start
        file_id = "file-{}".format(i)
        clip_id = "clip-{}".format(i)
        master_id = "master-{}".format(i)

        xml_lines.append('              <clipitem id="{}">'.format(clip_id))
        xml_lines.append('                <masterclipid>{}</masterclipid>'.format(master_id))
        xml_lines.append('                <name>{}</name>'.format(clean_name))
        xml_lines.append('                <duration>{}</duration>'.format(duration))
        xml_lines.append('                <rate>')
        xml_lines.append('                  <timebase>{}</timebase>'.format(fps))
        xml_lines.append('                  <ntsc>FALSE</ntsc>')
        xml_lines.append('                </rate>')
        xml_lines.append('                <start>{}</start>'.format(start))
        xml_lines.append('                <end>{}</end>'.format(end))
        xml_lines.append('                <in>0</in>')
        xml_lines.append('                <out>{}</out>'.format(duration))
        xml_lines.append('                <file id="{}">'.format(file_id))
        xml_lines.append('                  <name>{}</name>'.format(png_filename))
        xml_lines.append('                  <pathurl>{}</pathurl>'.format(file_url))
        xml_lines.append('                  <rate>')
        xml_lines.append('                    <timebase>{}</timebase>'.format(fps))
        xml_lines.append('                    <ntsc>FALSE</ntsc>')
        xml_lines.append('                  </rate>')
        xml_lines.append('                  <duration>1</duration>')
        xml_lines.append('                  <media>')
        xml_lines.append('                    <video>')
        xml_lines.append('                      <samplecharacteristics>')
        xml_lines.append('                        <rate>')
        xml_lines.append('                          <timebase>{}</timebase>'.format(fps))
        xml_lines.append('                          <ntsc>FALSE</ntsc>')
        xml_lines.append('                        </rate>')
        xml_lines.append('                        <width>1</width>')
        xml_lines.append('                        <height>1</height>')
        xml_lines.append('                        <anamorphic>FALSE</anamorphic>')
        xml_lines.append('                        <pixelaspectratio>square</pixelaspectratio>')
        xml_lines.append('                        <fielddominance>none</fielddominance>')
        xml_lines.append('                      </samplecharacteristics>')
        xml_lines.append('                    </video>')
        xml_lines.append('                  </media>')
        xml_lines.append('                </file>')
        xml_lines.append('                <sourcetrack>')
        xml_lines.append('                  <mediatype>video</mediatype>')
        xml_lines.append('                </sourcetrack>')
        xml_lines.append('              </clipitem>')

    xml_lines.append('            </track>')
    xml_lines.append('          </video>')
    xml_lines.append('        </media>')
    xml_lines.append('      </sequence>')
    xml_lines.append('    </children>')
    xml_lines.append('  </project>')
    xml_lines.append('</xmeml>')

    xml_path = os.path.join(output_dir, "shot_track.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))

    return xml_path


def run(resolve, cfg):
    """
    执行 PNG/XML 导出

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
        logs.append("[ERROR] No clips on {} track".format(cfg["track"]))
        return logs

    logs.append("{} track has {} clip(s)".format(cfg["track"], len(items)))
    items = sorted(items, key=lambda x: x.GetStart())

    png_count = 0

    for i, item in enumerate(items):
        name = item.GetName()
        if not name:
            name = item.GetProperty("Clip Name")
        if not name:
            logs.append("  [SKIP] Failed to get name for clip #{}".format(i + 1))
            continue

        clean_name = os.path.splitext(name)[0] if cfg["remove_suffix"] else name

        filepath = os.path.join(output_dir, "{}.png".format(clean_name))
        generate_png(filepath)
        logs.append("  [PNG] {}.png".format(clean_name))
        png_count += 1

    xml_path = generate_fcp7_xml_v5(timeline, items, output_dir, fps, cfg["remove_suffix"])
    logs.append("  [XML] {}".format(xml_path))

    logs.append("-" * 40)
    logs.append("Done! {} clips total".format(len(items)))
    logs.append("PNG generated: {}".format(png_count))
    logs.append("XML: {}".format(xml_path))
    logs.append("Output directory: {}".format(output_dir))
    logs.append("")
    logs.append("[Import to Resolve]")
    logs.append("1. File > Import > Timeline")
    logs.append("2. Select shot_track.xml")
    logs.append("3. Import to new or existing timeline")
    logs.append("4. Ensure PNG paths match XML pathurl")

    return logs
