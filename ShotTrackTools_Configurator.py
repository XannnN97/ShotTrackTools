#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ShotTrackTools Configurator - 外部配置工具
用于在达芬奇外部配置参数，供达芬奇脚本读取

版本: v1.0.1

使用方法：
1. 双击运行此文件（需要 Python 3.x）
2. 填写参数后点击"保存配置"
3. 在达芬奇中运行对应脚本，自动读取配置

安装路径：
与 ShotTrackTools 文件夹放在一起即可，或者放在桌面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys

# 确保能导入同级目录的公共模块
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

import shottracktools_utils as stu

VERSION = stu.__version__
CONFIG_DIR = stu.CONFIG_DIR
CONFIG_FILE = stu.CONFIG_FILE


def load_config():
    return stu.load_config()


def save_config(config):
    stu.save_config(config)


class ConfiguratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ShotTrackTools Configurator v{}".format(VERSION))
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # 加载已有配置
        self.config = load_config()

        # 主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 标题
        title = ttk.Label(main_frame, text="ShotTrackTools 参数配置", font=("Arial", 14, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        # 说明
        desc = ttk.Label(main_frame, text="配置完成后，在达芬奇中运行脚本即可自动读取", foreground="gray")
        desc.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        # === Batch_Shot_Renamer (Replace) 参数 ===
        ttk.Label(main_frame, text="【Batch Shot Renamer (Replace)】", font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))

        ttk.Label(main_frame, text="目标轨道:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.track_var = tk.StringVar(value=self.config.get("track", "V10"))
        ttk.Entry(main_frame, textvariable=self.track_var, width=20).grid(row=3, column=1, sticky=tk.W, pady=2)

        ttk.Label(main_frame, text="查找内容:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.search_var = tk.StringVar(value=self.config.get("search", "sq1300"))
        ttk.Entry(main_frame, textvariable=self.search_var, width=20).grid(row=4, column=1, sticky=tk.W, pady=2)

        ttk.Label(main_frame, text="替换为:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.replace_var = tk.StringVar(value=self.config.get("replace", "sq1400"))
        ttk.Entry(main_frame, textvariable=self.replace_var, width=20).grid(row=5, column=1, sticky=tk.W, pady=2)

        self.suffix_var = tk.BooleanVar(value=self.config.get("remove_suffix", True))
        ttk.Checkbutton(main_frame, text="去掉文件后缀", variable=self.suffix_var).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=2)

        # === Batch_Shot_Sequential 参数 ===
        ttk.Label(main_frame, text="【Batch Shot Sequential (顺序递增)】", font=("Arial", 10, "bold")).grid(row=7, column=0, columnspan=3, sticky=tk.W, pady=(15, 5))

        ttk.Label(main_frame, text="目标轨道:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.seq_track_var = tk.StringVar(value=self.config.get("seq_track", "V10"))
        ttk.Entry(main_frame, textvariable=self.seq_track_var, width=20).grid(row=8, column=1, sticky=tk.W, pady=2)

        ttk.Label(main_frame, text="前缀 (如 2Esq1400_):").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.seq_prefix_var = tk.StringVar(value=self.config.get("seq_prefix", "2Esq1400_"))
        ttk.Entry(main_frame, textvariable=self.seq_prefix_var, width=20).grid(row=9, column=1, sticky=tk.W, pady=2)

        ttk.Label(main_frame, text="起始编号:").grid(row=10, column=0, sticky=tk.W, pady=2)
        self.seq_start_var = tk.StringVar(value=str(self.config.get("seq_start", "10")))
        ttk.Entry(main_frame, textvariable=self.seq_start_var, width=10).grid(row=10, column=1, sticky=tk.W, pady=2)

        ttk.Label(main_frame, text="步长:").grid(row=11, column=0, sticky=tk.W, pady=2)
        self.seq_step_var = tk.StringVar(value=str(self.config.get("seq_step", "10")))
        ttk.Entry(main_frame, textvariable=self.seq_step_var, width=10).grid(row=11, column=1, sticky=tk.W, pady=2)

        ttk.Label(main_frame, text="编号位数:").grid(row=12, column=0, sticky=tk.W, pady=2)
        self.seq_padding_var = tk.StringVar(value=str(self.config.get("seq_padding", "4")))
        ttk.Entry(main_frame, textvariable=self.seq_padding_var, width=10).grid(row=12, column=1, sticky=tk.W, pady=2)

        self.seq_suffix_var = tk.BooleanVar(value=self.config.get("seq_remove_suffix", True))
        ttk.Checkbutton(main_frame, text="去掉文件后缀", variable=self.seq_suffix_var).grid(row=13, column=0, columnspan=2, sticky=tk.W, pady=2)

        # === Timeline_Shot_to_PNG 参数 ===
        ttk.Label(main_frame, text="【Timeline Shot to PNG】", font=("Arial", 10, "bold")).grid(row=14, column=0, columnspan=3, sticky=tk.W, pady=(15, 5))

        ttk.Label(main_frame, text="目标轨道:").grid(row=15, column=0, sticky=tk.W, pady=2)
        self.png_track_var = tk.StringVar(value=self.config.get("png_track", "V10"))
        ttk.Entry(main_frame, textvariable=self.png_track_var, width=20).grid(row=15, column=1, sticky=tk.W, pady=2)

        ttk.Label(main_frame, text="输出目录:").grid(row=16, column=0, sticky=tk.W, pady=2)
        self.output_var = tk.StringVar(value=self.config.get("output_dir", ""))
        ttk.Entry(main_frame, textvariable=self.output_var, width=30).grid(row=16, column=1, sticky=tk.W, pady=2)
        ttk.Button(main_frame, text="浏览...", command=self.browse_output, width=8).grid(row=16, column=2, sticky=tk.W, padx=(5, 0))

        self.png_suffix_var = tk.BooleanVar(value=self.config.get("png_remove_suffix", True))
        ttk.Checkbutton(main_frame, text="去掉文件后缀", variable=self.png_suffix_var).grid(row=17, column=0, columnspan=2, sticky=tk.W, pady=2)

        # 按钮区
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=18, column=0, columnspan=3, pady=(20, 0))

        ttk.Button(btn_frame, text="保存配置", command=self.save, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="加载默认", command=self.load_defaults, width=15).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="退出", command=self.root.quit, width=15).grid(row=0, column=2, padx=5)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status = ttk.Label(main_frame, textvariable=self.status_var, foreground="gray")
        status.grid(row=19, column=0, columnspan=3, pady=(10, 0), sticky=tk.W)

    def browse_output(self):
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_var.set(path)

    def save(self):
        """保存配置，包含参数校验"""
        errors = []

        # 轨道字段非空校验
        track = self.track_var.get().strip()
        if not track:
            errors.append("【Batch Renamer】目标轨道不能为空")
        seq_track = self.seq_track_var.get().strip()
        if not seq_track:
            errors.append("【Batch Sequential】目标轨道不能为空")
        png_track = self.png_track_var.get().strip()
        if not png_track:
            errors.append("【Timeline to PNG】目标轨道不能为空")

        # 轨道格式校验
        for label, t in [("Renamer", track), ("Sequential", seq_track), ("PNG", png_track)]:
            if t and not (t[0].upper() in ("V", "A") and t[1:].isdigit()):
                errors.append("【{}】轨道格式 '{}' 无效，请使用 V10 / V1 / A1".format(label, t))

        # 数字字段校验
        try:
            seq_start = int(self.seq_start_var.get())
            if seq_start < 0:
                errors.append("【起始编号】不能为负数")
        except ValueError:
            errors.append("【起始编号】必须是整数")

        try:
            seq_step = int(self.seq_step_var.get())
            if seq_step <= 0:
                errors.append("【步长】必须大于 0")
        except ValueError:
            errors.append("【步长】必须是整数")

        try:
            seq_padding = int(self.seq_padding_var.get())
            if seq_padding <= 0 or seq_padding > 10:
                errors.append("【编号位数】必须在 1-10 之间")
        except ValueError:
            errors.append("【编号位数】必须是整数")

        # 输出目录校验（如果填写了）
        output_dir = self.output_var.get().strip()
        if output_dir:
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except Exception as e:
                    errors.append("【输出目录】无法创建目录: {}".format(str(e)))
            elif not os.path.isdir(output_dir):
                errors.append("【输出目录】路径不是有效目录")

        if errors:
            messagebox.showerror("保存失败", "请修正以下错误:\n\n" + "\n".join("  • " + e for e in errors))
            return

        try:
            config = {
                # Replace
                "track": track,
                "search": self.search_var.get(),
                "replace": self.replace_var.get(),
                "remove_suffix": self.suffix_var.get(),
                # Sequential
                "seq_track": seq_track,
                "seq_prefix": self.seq_prefix_var.get(),
                "seq_start": seq_start,
                "seq_step": seq_step,
                "seq_padding": seq_padding,
                "seq_remove_suffix": self.seq_suffix_var.get(),
                # PNG
                "png_track": png_track,
                "output_dir": output_dir,
                "png_remove_suffix": self.png_suffix_var.get(),
            }
            save_config(config)
            self.status_var.set("配置已保存: {}".format(CONFIG_FILE))
            messagebox.showinfo("保存成功", "配置已保存！\n\n现在可以在达芬奇中运行脚本了。\n配置文件路径:\n{}".format(CONFIG_FILE))
        except Exception as e:
            messagebox.showerror("保存失败", "保存配置文件时发生错误:\n{}".format(str(e)))

    def load_defaults(self):
        self.track_var.set("V10")
        self.search_var.set("sq1300")
        self.replace_var.set("sq1400")
        self.suffix_var.set(True)
        self.seq_track_var.set("V10")
        self.seq_prefix_var.set("2Esq1400_")
        self.seq_start_var.set("10")
        self.seq_step_var.set("10")
        self.seq_padding_var.set("4")
        self.seq_suffix_var.set(True)
        self.png_track_var.set("V10")
        self.output_var.set("")
        self.png_suffix_var.set(True)
        self.status_var.set("已加载默认值")


def main():
    root = tk.Tk()
    app = ConfiguratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
