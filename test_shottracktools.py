#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ShotTrackTools 单元测试
测试可在外部独立验证的纯函数逻辑
"""

import unittest
import os
import sys
import json
import tempfile
import shutil

# 添加项目目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shottracktools_utils as stu


class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertEqual(stu.__version__, "1.0.1")


class TestParseTrack(unittest.TestCase):
    def test_video_tracks(self):
        self.assertEqual(stu.parse_track("V1"), ("video", 1))
        self.assertEqual(stu.parse_track("V10"), ("video", 10))
        self.assertEqual(stu.parse_track("v5"), ("video", 5))
        self.assertEqual(stu.parse_track("  V99  "), ("video", 99))

    def test_audio_tracks(self):
        self.assertEqual(stu.parse_track("A1"), ("audio", 1))
        self.assertEqual(stu.parse_track("a10"), ("audio", 10))

    def test_invalid_format(self):
        with self.assertRaises(ValueError) as ctx:
            stu.parse_track("")
        self.assertIn("轨道格式错误", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            stu.parse_track("X1")
        self.assertIn("轨道格式错误", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            stu.parse_track("V")
        self.assertIn("轨道号必须是数字", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            stu.parse_track("Vabc")
        self.assertIn("轨道号必须是数字", str(ctx.exception))


class TestLoadConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_config_file = stu.CONFIG_FILE
        # 临时替换配置文件路径
        stu.CONFIG_FILE = os.path.join(self.temp_dir, "config.json")
        stu.CONFIG_DIR = self.temp_dir

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        stu.CONFIG_FILE = self.original_config_file
        stu.CONFIG_DIR = os.path.dirname(self.original_config_file)

    def test_load_existing_config(self):
        test_data = {"track": "V5", "search": "sq100"}
        with open(stu.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(test_data, f)
        config = stu.load_config()
        self.assertEqual(config["track"], "V5")
        self.assertEqual(config["search"], "sq100")

    def test_load_nonexistent_config(self):
        config = stu.load_config()
        self.assertEqual(config, {})

    def test_save_and_load_config(self):
        test_data = {"track": "V20", "start": 100}
        stu.save_config(test_data)
        config = stu.load_config()
        self.assertEqual(config["track"], "V20")
        self.assertEqual(config["start"], 100)


class TestGetParams(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_config_file = stu.CONFIG_FILE
        stu.CONFIG_FILE = os.path.join(self.temp_dir, "config.json")
        stu.CONFIG_DIR = self.temp_dir

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        stu.CONFIG_FILE = self.original_config_file
        stu.CONFIG_DIR = os.path.dirname(self.original_config_file)

    def test_with_defaults_only(self):
        schema = {
            "track": ("track", str),
            "search": ("search", str),
        }
        defaults = {"track": "V1", "search": "sq100"}
        params = stu.get_params(schema, defaults)
        self.assertEqual(params["track"], "V1")
        self.assertEqual(params["search"], "sq100")

    def test_with_config_override(self):
        schema = {
            "track": ("track", str),
            "start": ("seq_start", int),
        }
        defaults = {"track": "V1", "start": 10}
        test_config = {"track": "V5", "seq_start": "50"}
        with open(stu.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(test_config, f)
        params = stu.get_params(schema, defaults)
        self.assertEqual(params["track"], "V5")
        self.assertEqual(params["start"], 50)

    def test_invalid_type_falls_back(self):
        schema = {
            "start": ("seq_start", int),
        }
        defaults = {"start": 10}
        test_config = {"seq_start": "not_a_number"}
        with open(stu.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(test_config, f)
        params = stu.get_params(schema, defaults)
        self.assertEqual(params["start"], 10)  # 回退到默认值

    def test_no_converter(self):
        schema = {
            "flag": ("flag", None),
        }
        defaults = {"flag": True}
        test_config = {"flag": False}
        with open(stu.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(test_config, f)
        params = stu.get_params(schema, defaults)
        self.assertEqual(params["flag"], False)


if __name__ == "__main__":
    unittest.main()
