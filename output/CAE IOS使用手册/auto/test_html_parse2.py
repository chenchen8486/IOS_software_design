#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

html = '<td rowspan=1 colspan=1>标签页</td>'
match = re.search(r'<[tdh][^>]*>(.*?)</[tdh]>', html, re.DOTALL | re.IGNORECASE)
print('match:', match)
if match:
    print('group:', match.group(1))

# 测试 findall
cells = re.findall(r'<[tdh][^>]*>(.*?)</[tdh]>', html, re.DOTALL | re.IGNORECASE)
print('cells:', cells)

# 更复杂的测试
html2 = '<tr><td rowspan=1 colspan=1>标签页</td><td rowspan=1 colspan=1>区域</td></tr>'
cells2 = re.findall(r'<[tdh][^>]*>(.*?)</[tdh]>', html2, re.DOTALL | re.IGNORECASE)
print('cells2:', cells2)

# 测试完整表格
html3 = '<table><tr><td rowspan=1 colspan=1>标签页</td><td rowspan=1 colspan=1>区域</td></tr><tr><td>当前条件</td><td></td></tr></table>'
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html3, re.DOTALL | re.IGNORECASE)
print('rows:', len(rows))
for tr in rows:
    print('tr:', repr(tr))
    cells = re.findall(r'<[tdh][^>]*>(.*?)</[tdh]>', tr, re.DOTALL | re.IGNORECASE)
    print('cells:', cells)
