#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整理 CAE IOS 使用手册 Markdown 文件
- 删除目录（保留图列表、表格列表）
- 删除页眉页脚中的日期和页码行
- 清理多余空行
- 保留所有实质内容
"""

import re

input_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh.md"
output_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 状态标记
in_toc = False
toc_started = False

# 正则：匹配类似 "2017年10月13日" 或 "第 xxx 页" 或 "目录 2017年10月13日 第v页"
# 我们要删除的页眉页脚模式
page_header_footer_patterns = [
    re.compile(r"^\s*2017年10月13日\s*$"),
    re.compile(r"^\s*第\s*[ivxcdlmnIVXCDLMN0-9]+\s*页\s*$"),
    re.compile(r"^\s*目录\s*2017年10月13日\s*第\s*[ivxcdlmnIVXCDLMN0-9]+\s*页\s*$"),
    re.compile(r"^\s*目录\s*$"),  # 单独的 "目录" 行（在目录部分之外如果存在也清理）
    re.compile(r"^\s*图列表\s*2017年10月13日\s*第\s*[ivxcdlmnIVXCDLMN0-9]+\s*页\s*$"),
    re.compile(r"^\s*图表清单\s*2017年10月13日\s*第\s*[ivxcdlmnIVXCDLMN0-9]+\s*页\s*$"),
    re.compile(r"^\s*地图工作区\s*2017年10月13日\s*第\s*[0-9]+\s*页\s*$"),
    re.compile(r"^\s*高级\s*2017年10月13日\s*第\s*[0-9]+\s*页\s*$"),
    re.compile(r"^\s*参考机场选项卡\s*2017年10月13日\s*第\s*[0-9]+\s*页\s*$"),
    re.compile(r"^\s*飞机选项卡\s*2017年10月13日\s*第\s*[0-9]+\s*页\s*$"),
    re.compile(r"^\s*当前条件选项卡\s*2017年10月13日\s*第\s*[0-9]+\s*页\s*$"),
    re.compile(r"^\s*控制台工作区\s*2017年10月13日\s*第\s*[0-9]+\s*页\s*$"),
    re.compile(r"^\s*面板\s*2017年10月13日\s*第\s*[0-9]+\s*页\s*$"),
    re.compile(r"^\s*教案概要工作区\s*2017年10月13日\s*第\s*[0-9]+\s*页\s*$"),
    re.compile(r"^\s*高级\s+2017年10月13日\s+第\s*[0-9]+\s*页\s*$"),
]

# 有些页眉是 "主题 日期 页码" 混在一行，需要更通用的模式
generic_header_pattern = re.compile(
    r"^\s*(目录|图列表|图表清单|地图工作区|高级|参考机场选项卡|飞机选项卡|当前条件选项卡|控制台工作区|面板|教案概要工作区|地图工作区|Advanced|高级)\s+2017年10月13日\s+第\s*[ivxcdlmnIVXCDLMN0-9]+\s*页\s*$",
    re.IGNORECASE,
)

# 通用的 日期+页码 行（前面可能是章节名）
header_footer_generic = re.compile(
    r"^\s*.*2017年10月13日\s*第\s*[ivxcdlmnIVXCDLMN0-9]+\s*页\s*$"
)

out_lines = []
prev_empty = False

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # 检测目录开始
    if stripped == "## 目录":
        in_toc = True
        toc_started = True
        i += 1
        continue

    # 检测目录结束（图列表开始）
    if in_toc and stripped.startswith("## 图列表"):
        in_toc = False
        out_lines.append(line)
        i += 1
        continue

    # 如果在目录中，跳过
    if in_toc:
        i += 1
        continue

    # 检测并跳过页眉页脚行
    skip = False
    for pat in page_header_footer_patterns:
        if pat.match(stripped):
            skip = True
            break
    if not skip and generic_header_pattern.match(stripped):
        skip = True
    if not skip and header_footer_generic.match(stripped):
        skip = True

    # 额外：跳过只包含 "目录" 或章节名+日期的行
    if not skip:
        # 匹配 "XXX 2017年10月13日" 这种（没有页码）
        if re.match(r"^\s*\S+\s+2017年10月13日\s*$", stripped):
            skip = True

    if skip:
        i += 1
        continue

    # 清理行末换行，后续统一处理
    out_lines.append(line.rstrip("\n"))
    i += 1

# 第二阶段：清理多余空行，同时清理独立行 "目录"
final_lines = []
prev_empty = False
for line in out_lines:
    stripped = line.strip()
    if stripped == "":
        if not prev_empty:
            final_lines.append("")
        prev_empty = True
    else:
        final_lines.append(line)
        prev_empty = False

# 写入
with open(output_path, "w", encoding="utf-8-sig") as f:
    for line in final_lines:
        f.write(line + "\n")

print(f"整理完成，已保存至: {output_path}")
print(f"原文件行数: {len(lines)}")
print(f"新文件行数: {len(final_lines)}")
