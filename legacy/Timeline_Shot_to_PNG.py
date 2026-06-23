#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Timeline Shot to PNG + XML - 读取时间线轨道，生成 PNG 和 FCP 7 XML v5
支持：从外部配置文件读取参数，无需修改脚本文件

版本: v1.0.1

使用方法：
1. 双击运行 ShotTrackTools_Configurator.py 配置参数（只需运行一次，或参数变更时）
2. 在达芬奇中运行：Workspace > Scripts > Utility > ShotTrackTools > Timeline_Shot_to_PNG
3. 查看 Console（Py3）输出日志
4. 在达芬奇中导入生成的 XML：File > Import > Timeline
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
    "output_dir": "",
    "remove_suffix": True,
}
_SCHEMA = {
    "track": ("png_track", str),
    "output_dir": ("output_dir", str),
    "remove_suffix": ("png_remove_suffix", None),
}
# =================================================


def generate_png(filepath):
    """使用 Pillow 生成 1x1 透明 PNG"""
    from PIL import Image
    img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    img.save(filepath)


def generate_fcp7_xml_v5(timeline, track_items, output_dir, fps, remove_suffix):
    """生成 FCP 7 XML v5 文件，达芬奇完美支持导入"""
    import os

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


def main():
    cfg = stu.get_params(_SCHEMA, _DEFAULTS)

    # 检查 Pillow 是否可用
    try:
        from PIL import Image
        pillow_available = True
    except ImportError:
        pillow_available = False

    # 获取当前项目和时间线
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("错误：没有打开的时间线，请先打开一个时间线")
        return

    # 确定输出目录
    output_dir = cfg["output_dir"]
    if not output_dir:
        output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    os.makedirs(output_dir, exist_ok=True)

    # 获取时间线帧率
    try:
        fps = float(timeline.GetSetting("timelineFrameRate"))
    except:
        try:
            fps = float(project.GetSetting("timelineFrameRate"))
        except:
            fps = 24.0
            print("[警告] 无法获取时间线帧率，默认使用 24fps")

    print("时间线:", timeline.GetName())
    print("目标轨道:", cfg["track"])
    print("输出目录:", output_dir)
    print("Pillow 可用:", pillow_available)
    print("时间线帧率:", fps)
    print("-" * 40)

    # 读取目标轨道
    track_type, track_idx = stu.parse_track(cfg["track"])
    items = timeline.GetItemListInTrack(track_type, track_idx)
    if not items:
        print("错误：{} 轨道上没有片段".format(cfg["track"]))
        return

    print("{} 轨道共 {} 个片段".format(cfg["track"], len(items)))
    items = sorted(items, key=lambda x: x.GetStart())

    shots = []
    png_count = 0

    for i, item in enumerate(items):
        name = item.GetName()
        if not name:
            name = item.GetProperty("Clip Name")
        if not name:
            print("  [跳过] 第 {} 个片段名称获取失败".format(i + 1))
            continue

        clean_name = os.path.splitext(name)[0] if cfg["remove_suffix"] else name

        shots.append({
            "name": clean_name,
            "start": item.GetStart(),
            "end": item.GetEnd(),
        })

        if pillow_available:
            filepath = os.path.join(output_dir, "{}.png".format(clean_name))
            generate_png(filepath)
            print("  [生成 PNG] {}.png".format(clean_name))
            png_count += 1
        else:
            print("  [记录] {}".format(clean_name))

    # 生成 FCP 7 XML v5
    xml_path = generate_fcp7_xml_v5(timeline, items, output_dir, fps, cfg["remove_suffix"])
    print("  [生成 XML] {}".format(xml_path))

    if not pillow_available:
        json_path = os.path.join(output_dir, "shot_list.json")
        import json
        json_data = {
            "project": project.GetName(),
            "timeline": timeline.GetName(),
            "track": cfg["track"],
            "output_dir": output_dir,
            "shots": shots,
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print("-" * 40)
        print("Pillow 未安装，PNG 未生成。")
        print("已导出 JSON 列表: {}".format(json_path))
        print("请安装 Pillow 后重新运行：pip install pillow")
    else:
        print("-" * 40)
        print("完成！共 {} 个片段".format(len(shots)))
        print("生成 PNG: {} 个".format(png_count))
        print("生成 XML: {}".format(xml_path))
        print("输出目录: {}".format(output_dir))
        print("")
        print("【导入达芬奇】")
        print("1. 在达芬奇中，点击菜单：File > Import > Timeline")
        print("2. 选择生成的 shot_track.xml")
        print("3. 选择导入到新时间线或现有时间线")
        print("4. 确保 PNG 文件路径与 XML 中 pathurl 一致")


if __name__ == "__main__":
    main()
