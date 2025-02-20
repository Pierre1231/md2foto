#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Author: HUANG Jingyi
File: html2foto.py
Date:  2025-02-18 01:15:23
Email: pierrehuang1998@gmail.com
Description: 
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os

# 配置浏览器选项
options = Options()
options.add_argument("--headless")  # 无头模式，后台运行

# 启动浏览器
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# 加载本地 HTML 文件
# 加载同文件夹下的 temp.html 文件
file_path = os.path.abspath("temp.html")
driver.get(file_path)

# 截图并保存
driver.save_screenshot('screenshot.png')

# 关闭浏览器
driver.quit()
