#!/usr/bin/env python3
# -*- coding: utf-8 -*-

input_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"
output_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 找到 "## 6.1 缩略图视图" 到 "图 16 DOCS 选项卡" 的范围
start_idx = None
end_idx = None
for idx, line in enumerate(lines):
    if line.strip() == "## 6.1 缩略图视图":
        start_idx = idx
    if start_idx is not None and "图 16 DOCS 选项卡" in line:
        end_idx = idx
        break

if start_idx is None or end_idx is None:
    print(f"未找到目标区域: start={start_idx}, end={end_idx}")
    exit(1)

print(f"找到目标区域: 行 {start_idx+1} 到 行 {end_idx+1}")

new_section = """## 6. 文档选项卡控件

文档选项卡允许教员查看参考文档，包含以下控件：

| 控件 | 功能 | 图示 |
|------|------|------|
| **缩略图视图** | 提供每个较大页面的小型图形表示列表 | ![](images/4ce59d5e9da2e7e7dd73e69d5d2ac755a8b46d54c7249019549b2cc44801c7a7.jpg) |
| **列表视图** | 提供所有页面标题的列表 | ![](images/b680847ab768a112bebe4178ee72f612c5bd519480ed00ecb9e38c55ff7c25d0.jpg) |
| **上下滚动** | 以"下一页"、"上一页"的方式在文档中上下滚动 | ![](images/ad9bf764771456d4bc411f5e6a4dc2ef731787132c64ce9cb2c361b83a6fa8b7.jpg) |
| **搜索功能** | 允许教员搜索一个单词或一串字符 | ![](images/09622f76266fb233e8270e67f2259828c797bce873006f0241acb9c82b479d4b.jpg) |
| **视图扩展** | 扩展可查看文档的视图 | ![](images/110a64ba87c355a3ed30deb740c192732c07ad43a93babe553be9024755911c3.jpg) |
| **缩放** | 放大和缩小控制 | ![](images/4c1ffa099c0ef8a4ef6ac9296deb24e52798a4ba9afbba4289b5962a5797a098.jpg) |

![](images/68349eb9d04990378adc2b9d3b17ebe772f3530795dbc865791c58f49105c457.jpg)
图 16 DOCS 选项卡
"""

new_lines = lines[:start_idx] + [new_section] + lines[end_idx+1:]

with open(output_path, "w", encoding="utf-8-sig") as f:
    f.writelines(new_lines)

print(f"替换完成，新文件行数: {len(new_lines)}")
