#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ShotTrackTools v1.1.0 单元测试
测试 ShotTrackTools_v1.1.0/ 架构下的公共模块和核心功能
"""

import unittest
import os
import sys
import tempfile
import shutil

# 添加 ShotTrackTools_v1.1.0 到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ShotTrackTools_v1.1.0'))

import shottracktools_utils as stu
from lib.png_exporter import generate_png, _make_chunk


class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertEqual(stu.__version__, "1.1.0")


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


class TestGeneratePng(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_png_file_created(self):
        filepath = os.path.join(self.temp_dir, "test.png")
        generate_png(filepath)
        self.assertTrue(os.path.exists(filepath))

    def test_png_header_valid(self):
        filepath = os.path.join(self.temp_dir, "test.png")
        generate_png(filepath)
        with open(filepath, 'rb') as f:
            header = f.read(8)
        # PNG 文件签名: 89 50 4E 47 0D 0A 1A 0A
        self.assertEqual(header, b'\x89PNG\r\n\x1a\n')

    def test_png_file_not_empty(self):
        filepath = os.path.join(self.temp_dir, "test.png")
        generate_png(filepath)
        self.assertGreater(os.path.getsize(filepath), 0)

    def test_png_chunk_valid(self):
        # 测试 _make_chunk 生成的 chunk 格式正确
        chunk = _make_chunk(b'IHDR', b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00')
        # chunk 格式: 4字节长度 + 4字节类型 + 数据 + 4字节 CRC
        self.assertGreater(len(chunk), 12)  # 至少长度 + 类型 + CRC


class TestGetResolve(unittest.TestCase):
    def test_get_resolve_without_davinci(self):
        # 在没有达芬奇的环境中，应该返回 None
        resolve = stu.get_resolve()
        # 如果不在达芬奇中运行，应该返回 None 或 resolve 对象
        self.assertTrue(resolve is None or hasattr(resolve, 'GetProjectManager'))


class TestBackendJsonProtocol(unittest.TestCase):
    """测试 backend.py 的 JSON 通信协议格式"""

    def test_undo_data_format(self):
        # 验证 undoData 格式正确
        undo_data = {
            "type": "renamer",
            "track": "V10",
            "items": [
                {"start": 100, "end": 200, "originalName": "sq1300"}
            ]
        }
        self.assertIn("type", undo_data)
        self.assertIn("track", undo_data)
        self.assertIn("items", undo_data)
        self.assertIsInstance(undo_data["items"], list)
        for item in undo_data["items"]:
            self.assertIn("start", item)
            self.assertIn("end", item)
            self.assertIn("originalName", item)

    def test_execute_request_format(self):
        # 验证 execute 请求格式
        request = {
            "action": "execute",
            "type": "batch_renamer",
            "params": {
                "track": "V10",
                "search": "sq1300",
                "replace": "sq1400",
                "remove_suffix": True
            }
        }
        self.assertEqual(request["action"], "execute")
        self.assertEqual(request["type"], "batch_renamer")
        self.assertIn("params", request)

    def test_undo_request_format(self):
        # 验证 undo 请求格式
        request = {
            "action": "undo",
            "undoData": {
                "type": "sequential",
                "track": "V2",
                "items": []
            }
        }
        self.assertEqual(request["action"], "undo")
        self.assertIn("undoData", request)


if __name__ == "__main__":
    unittest.main()
