#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ShotTrackTools Workflow Integration
DaVinci Resolve 官方 Workflow Integration 插件入口

版本: v1.1.0
功能: 批量替换、顺序递增、PNG/XML 导出、去后缀

安装路径:
    %PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Workflow Integration Plugins\com.basefx.shottracktools\
使用方式:
    达芬奇中: Workspace → Workflow Integrations → ShotTrackTools
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import json

# ============================================================
# 路径处理（兼容达芬奇 exec 环境）
# ============================================================
_script_dir = None
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    if hasattr(sys, 'argv') and sys.argv:
        _script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    if not _script_dir:
        _script_dir = os.getcwd()
if _script_dir and _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

import shottracktools_utils as stu
from lib import renamer, sequential, png_exporter, remove_suffix

VERSION = stu.__version__


# ============================================================
# 国际化字典
# ============================================================
I18N = {
    "zh": {
        "title": "ShotTrackTools v{}",
        "batch_renamer": "批量替换",
        "batch_sequential": "顺序递增",
        "png_export": "PNG/XML 导出",
        "remove_suffix": "去后缀",
        "target_track": "目标轨道",
        "search": "查找内容",
        "replace": "替换为",
        "prefix": "前缀",
        "start_num": "起始编号",
        "step": "步长",
        "padding": "编号位数",
        "output_dir": "输出目录",
        "remove_suffix_label": "去掉文件后缀",
        "execute": "执行",
        "save_config": "保存配置",
        "load_defaults": "加载默认",
        "lang": "语言",
        "log": "日志",
        "ready": "就绪",
        "select_function": "请选择功能",
        "track_hint": "如 V10 / V1 / A1",
        "browse": "浏览...",
        "no_timeline": "错误：没有打开的时间线",
        "no_project": "错误：没有打开的项目",
        "done": "完成",
        "error": "错误",
        "warning": "警告",
        "info": "信息",
        "config_saved": "配置已保存",
        "defaults_loaded": "已加载默认值",
        "please_select_func": "请先选择左侧功能",
        "renamer_desc": "将时间线轨道上的 Clip Name 批量替换",
        "sequential_desc": "按固定格式和步长对时间线片段递增命名",
        "png_desc": "生成透明 PNG 占位符 + FCP 7 XML v5",
        "suffix_desc": "去掉媒体池内所有片段的 .png 后缀",
    },
    "en": {
        "title": "ShotTrackTools v{}",
        "batch_renamer": "Batch Replace",
        "batch_sequential": "Sequential",
        "png_export": "PNG/XML Export",
        "remove_suffix": "Remove Suffix",
        "target_track": "Target Track",
        "search": "Search",
        "replace": "Replace",
        "prefix": "Prefix",
        "start_num": "Start Number",
        "step": "Step",
        "padding": "Padding",
        "output_dir": "Output Directory",
        "remove_suffix_label": "Remove File Suffix",
        "execute": "Execute",
        "save_config": "Save Config",
        "load_defaults": "Load Defaults",
        "lang": "Language",
        "log": "Log",
        "ready": "Ready",
        "select_function": "Please select a function",
        "track_hint": "e.g. V10 / V1 / A1",
        "browse": "Browse...",
        "no_timeline": "Error: No open timeline",
        "no_project": "Error: No open project",
        "done": "Done",
        "error": "Error",
        "warning": "Warning",
        "info": "Info",
        "config_saved": "Config saved",
        "defaults_loaded": "Defaults loaded",
        "please_select_func": "Please select a function from the left",
        "renamer_desc": "Batch replace Clip Name on timeline track",
        "sequential_desc": "Sequential naming with fixed prefix and step",
        "png_desc": "Generate transparent PNG + FCP 7 XML v5",
        "suffix_desc": "Remove .png suffix from Media Pool clips",
    }
}


# ============================================================
# 主应用类
# ============================================================
class ShotTrackToolsApp:
    def __init__(self, root):
        self.root = root
        self.lang = "zh"
        self.current_func = None
        self.config = stu.load_config()

        # 窗口设置
        self.root.title(self.t("title").format(VERSION))
        self.root.geometry("780x700")
        self.root.minsize(700, 600)

        # 样式
        self.style = ttk.Style()
        self.style.configure("Func.TButton", padding=5)
        self.style.configure("Active.TButton", padding=5, background="#0078D4")

        # 主布局：左右分栏
        self.main_pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左侧：功能列表
        self._build_left_panel()

        # 右侧：参数 + 日志
        self._build_right_panel()

        # 状态栏
        self.status_var = tk.StringVar(value=self.t("ready"))
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=(0, 5))

        # 默认加载配置
        self._load_config_to_vars()

    def t(self, key):
        """获取当前语言的文本"""
        return I18N.get(self.lang, I18N["zh"]).get(key, key)

    def _build_left_panel(self):
        """构建左侧功能列表"""
        self.left_frame = ttk.Frame(self.main_pane, width=160)
        self.main_pane.add(self.left_frame, weight=0)

        # 标题
        ttk.Label(self.left_frame, text="ShotTrackTools", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        ttk.Label(self.left_frame, text="v{}".format(VERSION), foreground="gray").pack()

        ttk.Separator(self.left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10, padx=5)

        # 功能按钮
        self.func_buttons = {}
        funcs = [
            ("batch_renamer", "renamer_desc"),
            ("batch_sequential", "sequential_desc"),
            ("png_export", "png_desc"),
            ("remove_suffix", "suffix_desc"),
        ]
        for func_key, desc_key in funcs:
            btn_frame = ttk.Frame(self.left_frame)
            btn_frame.pack(fill=tk.X, padx=5, pady=2)
            btn = ttk.Button(btn_frame, text=self.t(func_key),
                           command=lambda fk=func_key: self.select_function(fk))
            btn.pack(fill=tk.X)
            self.func_buttons[func_key] = btn

            # 描述标签
            desc = ttk.Label(btn_frame, text=self.t(desc_key), font=("Arial", 8),
                           foreground="gray", wraplength=140, justify=tk.LEFT)
            desc.pack(fill=tk.X, pady=(2, 5))

        ttk.Separator(self.left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10, padx=5)

        # 语言切换
        ttk.Label(self.left_frame, text=self.t("lang"), font=("Arial", 9, "bold")).pack(pady=(5, 2))
        self.lang_var = tk.StringVar(value=self.lang)
        lang_frame = ttk.Frame(self.left_frame)
        lang_frame.pack(padx=5)
        ttk.Radiobutton(lang_frame, text="中文", variable=self.lang_var, value="zh",
                       command=self.change_language).pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(lang_frame, text="EN", variable=self.lang_var, value="en",
                       command=self.change_language).pack(side=tk.LEFT, padx=2)

    def _build_right_panel(self):
        """构建右侧参数和日志面板"""
        self.right_frame = ttk.Frame(self.main_pane)
        self.main_pane.add(self.right_frame, weight=1)

        # 参数面板（动态内容）
        self.param_frame = ttk.LabelFrame(self.right_frame, text=self.t("select_function"), padding=10)
        self.param_frame.pack(fill=tk.X, padx=5, pady=5)

        # 占位提示
        self.param_placeholder = ttk.Label(self.param_frame, text=self.t("please_select_func"),
                                            foreground="gray", font=("Arial", 10))
        self.param_placeholder.pack(pady=20)

        # 按钮区（执行、保存、默认）
        self.btn_frame = ttk.Frame(self.right_frame)
        self.btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.btn_execute = ttk.Button(self.btn_frame, text=self.t("execute"), command=self.execute)
        self.btn_execute.pack(side=tk.LEFT, padx=5)
        self.btn_save = ttk.Button(self.btn_frame, text=self.t("save_config"), command=self.save_config)
        self.btn_save.pack(side=tk.LEFT, padx=5)
        self.btn_defaults = ttk.Button(self.btn_frame, text=self.t("load_defaults"), command=self.load_defaults)
        self.btn_defaults.pack(side=tk.LEFT, padx=5)

        # 日志区域
        self.log_frame = ttk.LabelFrame(self.right_frame, text=self.t("log"), padding=5)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(self.log_frame, command=self.log_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.log_text.config(yscrollcommand=scrollbar.set)

    # ============================================================
    # 功能切换
    # ============================================================
    def select_function(self, func_key):
        """选择功能，切换参数面板"""
        self.current_func = func_key

        # 更新按钮状态
        for key, btn in self.func_buttons.items():
            if key == func_key:
                btn.config(style="Active.TButton")
            else:
                btn.config(style="Func.TButton")

        # 清空参数面板并重建
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        self.param_frame.config(text=self.t(func_key))

        # 创建对应功能的参数表单
        if func_key == "batch_renamer":
            self._build_renamer_form()
        elif func_key == "batch_sequential":
            self._build_sequential_form()
        elif func_key == "png_export":
            self._build_png_form()
        elif func_key == "remove_suffix":
            self._build_suffix_form()

        # 恢复配置值
        self._load_config_to_vars()

        self.log("[INFO] {} selected".format(self.t(func_key)))

    def _build_renamer_form(self):
        """构建批量替换参数表单"""
        self.renamer_vars = {}

        # 轨道
        ttk.Label(self.param_frame, text=self.t("target_track")).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.renamer_vars["track"] = tk.StringVar(value="V10")
        ttk.Entry(self.param_frame, textvariable=self.renamer_vars["track"], width=15).grid(row=0, column=1, sticky=tk.W, pady=3)
        ttk.Label(self.param_frame, text=self.t("track_hint"), foreground="gray", font=("Arial", 8)).grid(row=0, column=2, sticky=tk.W, padx=5)

        # 查找
        ttk.Label(self.param_frame, text=self.t("search")).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.renamer_vars["search"] = tk.StringVar(value="sq1300")
        ttk.Entry(self.param_frame, textvariable=self.renamer_vars["search"], width=20).grid(row=1, column=1, sticky=tk.W, pady=3)

        # 替换
        ttk.Label(self.param_frame, text=self.t("replace")).grid(row=2, column=0, sticky=tk.W, pady=3)
        self.renamer_vars["replace"] = tk.StringVar(value="sq1400")
        ttk.Entry(self.param_frame, textvariable=self.renamer_vars["replace"], width=20).grid(row=2, column=1, sticky=tk.W, pady=3)

        # 后缀
        self.renamer_vars["remove_suffix"] = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.param_frame, text=self.t("remove_suffix_label"),
                       variable=self.renamer_vars["remove_suffix"]).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

    def _build_sequential_form(self):
        """构建顺序递增参数表单"""
        self.sequential_vars = {}

        # 轨道
        ttk.Label(self.param_frame, text=self.t("target_track")).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.sequential_vars["track"] = tk.StringVar(value="V10")
        ttk.Entry(self.param_frame, textvariable=self.sequential_vars["track"], width=15).grid(row=0, column=1, sticky=tk.W, pady=3)
        ttk.Label(self.param_frame, text=self.t("track_hint"), foreground="gray", font=("Arial", 8)).grid(row=0, column=2, sticky=tk.W, padx=5)

        # 前缀
        ttk.Label(self.param_frame, text=self.t("prefix")).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.sequential_vars["prefix"] = tk.StringVar(value="2Esq1400_")
        ttk.Entry(self.param_frame, textvariable=self.sequential_vars["prefix"], width=20).grid(row=1, column=1, sticky=tk.W, pady=3)

        # 起始
        ttk.Label(self.param_frame, text=self.t("start_num")).grid(row=2, column=0, sticky=tk.W, pady=3)
        self.sequential_vars["start"] = tk.StringVar(value="10")
        ttk.Entry(self.param_frame, textvariable=self.sequential_vars["start"], width=10).grid(row=2, column=1, sticky=tk.W, pady=3)

        # 步长
        ttk.Label(self.param_frame, text=self.t("step")).grid(row=3, column=0, sticky=tk.W, pady=3)
        self.sequential_vars["step"] = tk.StringVar(value="10")
        ttk.Entry(self.param_frame, textvariable=self.sequential_vars["step"], width=10).grid(row=3, column=1, sticky=tk.W, pady=3)

        # 位数
        ttk.Label(self.param_frame, text=self.t("padding")).grid(row=4, column=0, sticky=tk.W, pady=3)
        self.sequential_vars["padding"] = tk.StringVar(value="4")
        ttk.Entry(self.param_frame, textvariable=self.sequential_vars["padding"], width=10).grid(row=4, column=1, sticky=tk.W, pady=3)

        # 后缀
        self.sequential_vars["remove_suffix"] = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.param_frame, text=self.t("remove_suffix_label"),
                       variable=self.sequential_vars["remove_suffix"]).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)

    def _build_png_form(self):
        """构建 PNG 导出参数表单"""
        self.png_vars = {}

        # 轨道
        ttk.Label(self.param_frame, text=self.t("target_track")).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.png_vars["track"] = tk.StringVar(value="V10")
        ttk.Entry(self.param_frame, textvariable=self.png_vars["track"], width=15).grid(row=0, column=1, sticky=tk.W, pady=3)
        ttk.Label(self.param_frame, text=self.t("track_hint"), foreground="gray", font=("Arial", 8)).grid(row=0, column=2, sticky=tk.W, padx=5)

        # 输出目录
        ttk.Label(self.param_frame, text=self.t("output_dir")).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.png_vars["output_dir"] = tk.StringVar(value="")
        ttk.Entry(self.param_frame, textvariable=self.png_vars["output_dir"], width=35).grid(row=1, column=1, sticky=tk.W, pady=3)
        ttk.Button(self.param_frame, text=self.t("browse"), width=8,
                  command=self._browse_output_dir).grid(row=1, column=2, sticky=tk.W, padx=5)

        # 后缀
        self.png_vars["remove_suffix"] = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.param_frame, text=self.t("remove_suffix_label"),
                       variable=self.png_vars["remove_suffix"]).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)

    def _build_suffix_form(self):
        """构建去后缀参数表单（无参数，仅说明）"""
        ttk.Label(self.param_frame, text=self.t("suffix_desc"), wraplength=500, justify=tk.LEFT).pack(pady=20)
        ttk.Label(self.param_frame, text="\n" + self.t("no_timeline") + "\n" + self.t("no_project"),
                 foreground="gray", font=("Arial", 9)).pack()

    def _browse_output_dir(self):
        """浏览输出目录"""
        path = filedialog.askdirectory(title="Select Output Directory" if self.lang == "en" else "选择输出目录")
        if path and self.png_vars:
            self.png_vars["output_dir"].set(path)

    # ============================================================
    # 配置读写
    # ============================================================
    def _load_config_to_vars(self):
        """从配置文件加载值到变量"""
        cfg = self.config
        if self.current_func == "batch_renamer" and hasattr(self, "renamer_vars"):
            self.renamer_vars["track"].set(cfg.get("track", "V10"))
            self.renamer_vars["search"].set(cfg.get("search", "sq1300"))
            self.renamer_vars["replace"].set(cfg.get("replace", "sq1400"))
            self.renamer_vars["remove_suffix"].set(cfg.get("remove_suffix", True))
        elif self.current_func == "batch_sequential" and hasattr(self, "sequential_vars"):
            self.sequential_vars["track"].set(cfg.get("seq_track", "V10"))
            self.sequential_vars["prefix"].set(cfg.get("seq_prefix", "2Esq1400_"))
            self.sequential_vars["start"].set(str(cfg.get("seq_start", 10)))
            self.sequential_vars["step"].set(str(cfg.get("seq_step", 10)))
            self.sequential_vars["padding"].set(str(cfg.get("seq_padding", 4)))
            self.sequential_vars["remove_suffix"].set(cfg.get("seq_remove_suffix", True))
        elif self.current_func == "png_export" and hasattr(self, "png_vars"):
            self.png_vars["track"].set(cfg.get("png_track", "V10"))
            self.png_vars["output_dir"].set(cfg.get("output_dir", ""))
            self.png_vars["remove_suffix"].set(cfg.get("png_remove_suffix", True))

    def save_config(self):
        """保存当前配置"""
        cfg = dict(self.config)  # 复制现有配置

        if self.current_func == "batch_renamer" and hasattr(self, "renamer_vars"):
            cfg.update({
                "track": self.renamer_vars["track"].get(),
                "search": self.renamer_vars["search"].get(),
                "replace": self.renamer_vars["replace"].get(),
                "remove_suffix": self.renamer_vars["remove_suffix"].get(),
            })
        elif self.current_func == "batch_sequential" and hasattr(self, "sequential_vars"):
            cfg.update({
                "seq_track": self.sequential_vars["track"].get(),
                "seq_prefix": self.sequential_vars["prefix"].get(),
                "seq_start": int(self.sequential_vars["start"].get() or 10),
                "seq_step": int(self.sequential_vars["step"].get() or 10),
                "seq_padding": int(self.sequential_vars["padding"].get() or 4),
                "seq_remove_suffix": self.sequential_vars["remove_suffix"].get(),
            })
        elif self.current_func == "png_export" and hasattr(self, "png_vars"):
            cfg.update({
                "png_track": self.png_vars["track"].get(),
                "output_dir": self.png_vars["output_dir"].get(),
                "png_remove_suffix": self.png_vars["remove_suffix"].get(),
            })

        stu.save_config(cfg)
        self.config = cfg
        self.status_var.set(self.t("config_saved"))
        self.log("[INFO] {}".format(self.t("config_saved")))

    def load_defaults(self):
        """加载默认值"""
        if self.current_func == "batch_renamer" and hasattr(self, "renamer_vars"):
            self.renamer_vars["track"].set("V10")
            self.renamer_vars["search"].set("sq1300")
            self.renamer_vars["replace"].set("sq1400")
            self.renamer_vars["remove_suffix"].set(True)
        elif self.current_func == "batch_sequential" and hasattr(self, "sequential_vars"):
            self.sequential_vars["track"].set("V10")
            self.sequential_vars["prefix"].set("2Esq1400_")
            self.sequential_vars["start"].set("10")
            self.sequential_vars["step"].set("10")
            self.sequential_vars["padding"].set("4")
            self.sequential_vars["remove_suffix"].set(True)
        elif self.current_func == "png_export" and hasattr(self, "png_vars"):
            self.png_vars["track"].set("V10")
            self.png_vars["output_dir"].set("")
            self.png_vars["remove_suffix"].set(True)

        self.status_var.set(self.t("defaults_loaded"))
        self.log("[INFO] {}".format(self.t("defaults_loaded")))

    # ============================================================
    # 执行功能
    # ============================================================
    def execute(self):
        """执行当前选中的功能"""
        if not self.current_func:
            messagebox.showwarning(self.t("warning"), self.t("please_select_func"))
            return

        resolve = stu.get_resolve()
        if not resolve:
            self.log("[ERROR] Cannot connect to DaVinci Resolve")
            return

        self.log("-" * 50)
        self.log("[{}] Executing: {}".format(self.t("info"), self.t(self.current_func)))

        try:
            if self.current_func == "batch_renamer":
                cfg = {
                    "track": self.renamer_vars["track"].get(),
                    "search": self.renamer_vars["search"].get(),
                    "replace": self.renamer_vars["replace"].get(),
                    "remove_suffix": self.renamer_vars["remove_suffix"].get(),
                }
                logs = renamer.run(resolve, cfg)
            elif self.current_func == "batch_sequential":
                cfg = {
                    "track": self.sequential_vars["track"].get(),
                    "prefix": self.sequential_vars["prefix"].get(),
                    "start": int(self.sequential_vars["start"].get() or 10),
                    "step": int(self.sequential_vars["step"].get() or 10),
                    "padding": int(self.sequential_vars["padding"].get() or 4),
                    "remove_suffix": self.sequential_vars["remove_suffix"].get(),
                }
                logs = sequential.run(resolve, cfg)
            elif self.current_func == "png_export":
                cfg = {
                    "track": self.png_vars["track"].get(),
                    "output_dir": self.png_vars["output_dir"].get(),
                    "remove_suffix": self.png_vars["remove_suffix"].get(),
                }
                logs = png_exporter.run(resolve, cfg)
            elif self.current_func == "remove_suffix":
                logs = remove_suffix.run(resolve)
            else:
                logs = ["[ERROR] Unknown function"]

            for line in logs:
                self.log(line)

            self.status_var.set("{}: {}".format(self.t("done"), self.t(self.current_func)))
        except Exception as e:
            self.log("[ERROR] {}".format(str(e)))
            self.status_var.set("{}: {}".format(self.t("error"), str(e)))

    # ============================================================
    # 日志和语言
    # ============================================================
    def log(self, message):
        """输出日志到文本区域"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def change_language(self):
        """切换语言"""
        new_lang = self.lang_var.get()
        if new_lang == self.lang:
            return
        self.lang = new_lang

        # 更新窗口标题
        self.root.title(self.t("title").format(VERSION))

        # 更新功能按钮
        func_desc = [
            ("batch_renamer", "renamer_desc"),
            ("batch_sequential", "sequential_desc"),
            ("png_export", "png_desc"),
            ("remove_suffix", "suffix_desc"),
        ]
        for func_key, desc_key in func_desc:
            # 找到按钮对应的 frame，更新按钮文本和描述
            # 这里需要更复杂的更新，暂时只更新按钮文本
            btn = self.func_buttons[func_key]
            btn.config(text=self.t(func_key))

        # 更新参数面板标签
        self.param_frame.config(text=self.t(self.current_func) if self.current_func else self.t("select_function"))

        # 更新按钮
        self.btn_execute.config(text=self.t("execute"))
        self.btn_save.config(text=self.t("save_config"))
        self.btn_defaults.config(text=self.t("load_defaults"))

        # 更新日志区域标签
        self.log_frame.config(text=self.t("log"))

        # 更新状态栏
        self.status_var.set(self.t("ready"))

        # 重新构建当前功能表单以更新语言
        if self.current_func:
            self.select_function(self.current_func)


def main():
    root = tk.Tk()
    app = ShotTrackToolsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
