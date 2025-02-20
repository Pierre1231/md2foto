#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Author: HUANG Jingyi
File: screenshotNsave_test.py
Date:  2025-02-19 19:25:45
Email: pierrehuang1998@gmail.com
Description: 
"""
from html2image import Html2Image
import os
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()


# 定义输出路径（确保该路径有写入权限）
output_path = "D:/10.个人兴趣/md2foto/md2foto/output"  # 当前目录
# 测试路径是否有写入权限
test_file = os.path.join(output_path, "test_write.txt")

try:
    with open(test_file, "w") as f:
        f.write("test")
    os.remove(test_file)
    print(f"✅ {output_path} 目录可写")
except PermissionError:
    print(f"❌ {output_path} 目录没有写入权限，请更换路径或调整权限")
    exit(1)

# 初始化 Html2Image
hti = Html2Image(output_path=output_path)

# 定义测试 HTML
html_template = "<!DOCTYPE html><html><body><h1>Hello, Screenshot!</h1></body></html>"

# 生成截图
screenshot_name = "rendered.png"
try:
    hti.screenshot(html_str=html_template, save_as=screenshot_name)
    screenshot_path = os.path.join(output_path, screenshot_name)
    if os.path.exists(screenshot_path):
        print(f"✅ 截图成功保存至 {screenshot_path}")
    else:
        print(f"❌ 截图未成功生成，可能是 html2image 依赖问题")
except Exception as e:
    print(f"⚠️ 发生错误: {e}")
