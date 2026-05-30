#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

input_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"
output_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 找到 "## 1. 引言" 的索引
intro_idx = None
for idx, line in enumerate(lines):
    if re.match(r"^## 1\.\s*引言\s*$", line.strip()):
        intro_idx = idx
        break

if intro_idx is None:
    print("未找到 '## 1. 引言'，未作更改")
    exit(1)

# 保留从 "## 1. 引言" 开始的内容
out_lines = lines[intro_idx:]

# 清理多余空行
final_lines = []
prev_empty = False
for line in out_lines:
    stripped = line.strip()
    if stripped == "":
        if not prev_empty:
            final_lines.append("\n")
        prev_empty = True
    else:
        final_lines.append(line)
        prev_empty = False

with open(output_path, "w", encoding="utf-8-sig") as f:
    f.writelines(final_lines)

print(f"已删除前 {intro_idx} 行，保留从 '## 1. 引言' 开始的内容")
print(f"新文件行数: {len(final_lines)}")
