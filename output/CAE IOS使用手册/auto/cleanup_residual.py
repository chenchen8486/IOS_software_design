#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

input_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"
output_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

out_lines = []
in_effective_pages = False

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # 检测有效页面列表开始
    if stripped == "有效页面列表":
        in_effective_pages = True
        i += 1
        continue

    if in_effective_pages:
        # 如果当前行是表格行，继续跳过
        if stripped.startswith("<") or stripped.startswith("<table") or stripped.startswith("<tr") or stripped.startswith("</table>") or stripped.startswith("<td"):
            i += 1
            continue
        # 表格结束后如果遇到空行或非表格行，则退出有效页面列表模式
        if stripped == "" or not (stripped.startswith("<") or stripped.startswith("|")):
            in_effective_pages = False
            # 如果当前行不是空行，则保留它
            if stripped != "":
                out_lines.append(line.rstrip("\n"))
            i += 1
            continue
        i += 1
        continue

    # 跳过独立的页眉页脚行：匹配 "2017年10月13日更新 第X页" 或 "2017年10月13日 第X页"
    if re.match(r"^\s*2017年10月13日\s*更?新?\s*第\s*[0-9]+\s*页\s*$", stripped):
        i += 1
        continue

    out_lines.append(line.rstrip("\n"))
    i += 1

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

print(f"二次清理完成，已保存至: {output_path}")
print(f"新文件行数: {len(final_lines)}")
