#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Author: HUANG Jingyi
File: check_chromedriver.py
Date:  2025-02-18 00:23:42
Email: pierrehuang1998@gmail.com
Description: 
"""
import os
import shutil
import chromedriver_autoinstaller

def detect_chrome_path():
    """尝试自动检测 Chrome 浏览器路径"""
    possible_paths = [
        shutil.which("google-chrome"),  # Linux
        shutil.which("chrome"),  # Windows
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # Mac
        "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Windows (默认安装路径)
    ]
    return next((path for path in possible_paths if path and os.path.exists(path)), None)

def ensure_chromedriver():
    """确保 chromedriver 安装并位于正确的路径"""
    chrome_path = detect_chrome_path()
    if not chrome_path:
        print("Error: Could not find Chrome browser.")
        return None

    print(f"Found Chrome browser at: {chrome_path}")

    # 使用 chromedriver_autoinstaller 确保 chromedriver 已安装
    driver_path = chromedriver_autoinstaller.install()
    if not os.path.exists(driver_path):
        print(f"Error: chromedriver not found at {driver_path}")
        return None

    print(f"chromedriver installed at: {driver_path}")
    return driver_path

if __name__ == "__main__":
    driver_path = ensure_chromedriver()
    if driver_path:
        print(f"chromedriver is correctly installed at: {driver_path}")
    else:
        print("Failed to ensure chromedriver installation.")
