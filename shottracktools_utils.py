#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ShotTrackTools 公共工具模块
提供配置读写、轨道解析、版本号等共享功能

供 Batch_Shot_Renamer、Batch_Shot_Sequential、Timeline_Shot_to_PNG 调用
"""

__version__ = "1.0.1"

import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".shottracktools")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def get_resolve():
    """获取 DaVinci Resolve 对象，支持外部执行"""
    if 'resolve' in globals():
        return resolve
    try:
        import DaVinciResolveScript as dvr
        return dvr.scriptapp("Resolve")
    except ImportError:
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


def get_params(schema, defaults):
    """
    从配置文件读取参数，按 schema 映射和转换

    Args:
        schema (dict): 参数映射，如 {"track": ("track", str)}
            键为返回字典的键名，值为 (配置文件中的键名, 类型转换函数)
            类型转换函数为 None 表示不做转换
        defaults (dict): 各参数的默认值

    Returns:
        dict: 读取并转换后的参数字典
    """
    config = load_config()
    result = {}

    if config:
        print("[Config] 已读取配置文件:", CONFIG_FILE)
    else:
        print("[Config] 配置文件不存在，使用默认参数")
        print("[Config] 提示：运行 ShotTrackTools_Configurator.py 可配置参数")

    for key, (config_key, converter) in schema.items():
        raw = config.get(config_key, defaults.get(key))
        if converter is not None:
            try:
                result[key] = converter(raw)
            except (ValueError, TypeError):
                result[key] = defaults.get(key)
        else:
            result[key] = raw if raw is not None else defaults.get(key)

    return result
