#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Author: HUANG Jingyi
File: path_right_detect.py
Date:  2025-02-19 19:23:04
Email: pierrehuang1998@gmail.com
Description: 
"""

import os

output_path = "D:/10.个人兴趣/md2foto/md2foto/output"  # 替换为你的路径

if os.access(output_path, os.W_OK):
    print(f"✅ {output_path} 目录可写")
else:
    print(f"❌ {output_path} 目录不可写，请检查权限")

