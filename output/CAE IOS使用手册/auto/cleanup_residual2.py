#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

input_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"
output_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 需要清理的孤立页眉残余关键词
header_residuals = {
    "当前条件选项卡",
    "控制台工作区",
    "飞机选项卡",
    "参考机场选项卡",
    "面板",
    "地图工作区",
    "高级",
    "教案概要工作区",
}

# 图列表区域的大致范围（从 "## 图列表" 到 "## 表格列表"）
# 我们需要先定位这两个边界
toc_start = None
toc_end = None
for idx, line in enumerate(lines):
    if line.strip() == "## 图列表":
        toc_start = idx
    if line.strip() == "## 表格列表":
        toc_end = idx
        break

out_lines = []
for idx, line in enumerate(lines):
    stripped = line.strip()

    # 1. 清理带空格的日期行：如 "2017 年 10 月 13 日" 及其变体
    if re.match(r"^\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*$", stripped):
        continue

    # 2. 清理孤立的页眉残余（不在图列表区域内）
    if toc_start is not None and toc_end is not None:
        if not (toc_start <= idx <= toc_end):
            if stripped in header_residuals:
                continue
    else:
        if stripped in header_residuals:
            continue

    out_lines.append(line.rstrip("\n"))

# 清理多余空行
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

with open(output_path, "w", encoding="utf-8-sig") as f:
    for line in final_lines:
        f.write(line + "\n")

print(f"三次清理完成，已保存至: {output_path}")
print(f"新文件行数: {len(final_lines)}")
