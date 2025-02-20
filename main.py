#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Author: HUANG Jingyi
File: main.py
Date:  2025-02-17
Email: pierrehuang1998@gmail.com
Description: Markdown 渲染工具（使用 Html2Image）
"""

import sys
import os
import markdown
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QFileDialog, QLabel, QSpinBox, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from html2image import Html2Image
from PIL import Image
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 自动安装 chromedriver
chromedriver_autoinstaller.install()


class MarkdownToImageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Markdown to Image")
        self.setGeometry(100, 100, 900, 700)

        self.textEdit = QTextEdit(self)
        self.loadButton = QPushButton("Load Markdown File", self)
        self.loadButton.clicked.connect(self.loadMarkdown)

        self.widthSpin = QSpinBox(self)
        self.widthSpin.setRange(400, 1600)
        self.widthSpin.setValue(800)

        self.convertButton = QPushButton("Convert to Image", self)
        self.convertButton.clicked.connect(self.convertMarkdown)

        self.savePathButton = QPushButton("Select Output Folder", self)
        self.savePathButton.clicked.connect(self.selectOutputFolder)

        self.outputFolder = os.path.join(os.getcwd(), "output")
        self.folderLabel = QLabel(self)  # 标签显示文件夹路径
        self.folderLabel.setText(f"Output folder: {self.outputFolder}")  # 显示默认路径

        self.imageLabel = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.loadButton)
        buttonLayout.addWidget(QLabel("Width:"))
        buttonLayout.addWidget(self.widthSpin)
        buttonLayout.addWidget(self.savePathButton)
        buttonLayout.addWidget(self.convertButton)

        layout.addLayout(buttonLayout)
        layout.addWidget(self.folderLabel)  # 显示文件夹路径
        layout.addWidget(self.imageLabel)

        self.setLayout(layout)

    def detect_chrome_path(self):
        """尝试自动检测 Chrome 浏览器路径"""
        print("Detecting Chrome browser path...")
        possible_paths = [
            shutil.which("google-chrome"),  # Linux
            shutil.which("chrome"),  # Windows
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # Mac
            "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Windows (默认安装路径)
        ]
        for path in possible_paths:
            if path and os.path.exists(path):
                print(f"Chrome detected at: {path}")
                return path
        print("Chrome not found.")
        return None


    def convertMarkdown(self):
        try:
            print("Converting Markdown to HTML...")
            markdown_text = self.textEdit.toPlainText()
            html_content = markdown.markdown(markdown_text)
            # 加载模板文件
            with open("template.html", "r", encoding="utf-8") as template_file:
                html_template = template_file.read()

            # 将 Markdown 渲染后的 HTML 内容插入模板
            html_template = html_template.replace("{{content}}", html_content)

            # 将新的 HTML 文件保存成临时文件
            with open("test/temp.html", "w", encoding="utf-8") as temp_file:
                temp_file.write(html_template)

            print("Checking Chrome and chromedriver paths...")
            # 获取并检查 Chrome 和 chromedriver
            driver_path = chromedriver_autoinstaller.install()
            chrome_path = self.detect_chrome_path()

            if not driver_path or not chrome_path:
                self.textEdit.setText("Error: Could not find Chrome browser or chromedriver.")
                return

            print(f"Chrome path: {chrome_path}")
            print(f"Chromedriver path: {driver_path}")

            # 确保输出文件夹存在
            print(f"Ensuring output folder exists at: {self.outputFolder}")
            if not os.path.exists(self.outputFolder):
                os.makedirs(self.outputFolder)

            # 配置 Html2Image
            print("Configuring Html2Image...")
            hti = Html2Image(output_path=self.outputFolder, browser_executable=chrome_path)
            output_image_path = os.path.join(self.outputFolder, "rendered.png")

            print(f"Saving screenshot to: {output_image_path}")

            # 执行截图
            # 没办法save
            # hti.screenshot(html_str=html_template, save_as="rendered.png")
            # hti.screenshot(html_str=html_template, save_as="rendered.png", size=(self.widthSpin.value(), 1200))
            hti.screenshot(save_as="rendered.png")
            # 检查截图是否成功保存
            if os.path.exists(output_image_path):
                print(f"Screenshot successfully saved to: {output_image_path}")
                self.splitImage(output_image_path)
            else:
                print("Error: Screenshot was not saved.")

        except Exception as e:
            print(f"Error during conversion: {e}")
            self.textEdit.setText(f"Error: {str(e)}")

    def splitImage(self, image_path):
        """切割图片成适合社交媒体的比例"""
        print(f"Splitting image at {image_path}...")
        img = Image.open(image_path)
        width, height = img.size
        aspect_ratio = 3 / 4
        new_height = int(width * aspect_ratio)

        os.makedirs(os.path.join(self.outputFolder, "split"), exist_ok=True)

        for i in range(0, height, new_height):
            cropped_img = img.crop((0, i, width, min(i + new_height, height)))
            split_image_path = f"{self.outputFolder}/split/part_{i // new_height + 1}.png"
            cropped_img.save(split_image_path)
            print(f"Saved split image part: {split_image_path}")

        pixmap = QPixmap(image_path)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setScaledContents(True)

    def loadMarkdown(self):
        print("Loading Markdown file...")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Markdown File", "",
                                                   "Markdown Files (*.md);;All Files (*)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                markdown_text = file.read()
                self.textEdit.setPlainText(markdown_text)
                print(f"Loaded Markdown file: {file_path}")

    def selectOutputFolder(self):
        print("Selecting output folder...")
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", "")
        if folder:
            self.outputFolder = folder
            self.folderLabel.setText(f"Output folder: {self.outputFolder}")  # 更新文件夹路径显示
            print(f"Selected output folder: {self.outputFolder}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownToImageApp()
    window.show()
    sys.exit(app.exec())
