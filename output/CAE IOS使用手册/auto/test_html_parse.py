#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

html = '<table><tr><td rowspan=1 colspan=1>标签页</td><td rowspan=1 colspan=1>区域</td></tr><tr><td>当前条件</td><td></td></tr></table>'

rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL | re.IGNORECASE)
print('rows:', len(rows))
for tr in rows:
    cells = re.findall(r'<[tdh][^>]*>(.*?)</[tdh]>', tr, re.DOTALL | re.IGNORECASE)
    print('cells:', cells)
