#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将文档中过度分散的列表项紧凑化：
- 删除连续的列表项（以 • o ▪ - 开头）之间的多余空行
- 使列表更易读，减少页面离散感
"""

import re

input_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"
output_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 列表项标记的正则
list_marker_pattern = re.compile(r"^(\s*)((?:[•o▪-]\s+)|(?:\d+\.\s+))(.+)$")

out_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.rstrip("\n")

    # 检测是否是列表项
    match = list_marker_pattern.match(stripped)
    if match:
        out_lines.append(stripped)
        i += 1
        # 跳过后续的空行，直到遇到下一个非空行
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        # 如果下一个非空行也是列表项，不添加空行（继续循环）
        # 否则添加一个空行作为段落分隔
        if i < len(lines) and not list_marker_pattern.match(lines[i].strip()):
            # 如果上一行不是列表项的结尾，添加空行
            if out_lines and out_lines[-1] != "":
                out_lines.append("")
        continue
    else:
        out_lines.append(stripped)
        i += 1

# 清理多余空行
final_lines = []
prev_empty = False
for line in out_lines:
    if line == "":
        if not prev_empty:
            final_lines.append("")
        prev_empty = True
    else:
        final_lines.append(line)
        prev_empty = False

with open(output_path, "w", encoding="utf-8-sig") as f:
    for line in final_lines:
        f.write(line + "\n")

print(f"列表紧凑化完成，已保存至: {output_path}")
print(f"原文件行数: {len(lines)}")
print(f"新文件行数: {len(final_lines)}")
