#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Author: HUANG Jingyi
File: main_1.py
Date:  2025-02-19 19:34:54
Email: pierrehuang1998@gmail.com
Description: 
"""

import sys
import os
import imgkit

import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QFileDialog, QLabel, QSpinBox, QHBoxLayout, QScrollArea
)
from PyQt6.QtGui import QPixmap
from PIL import Image
import chromedriver_autoinstaller
import markdown2

extensions = [
    'extra',  # 表格、脚注等扩展
    'toc',  # 目录支持
    'mdx_math',  # 数学公式
    'markdown_checklist.extension',  # 任务列表
    'pymdownx.magiclink',  # 自动识别超链接
    'pymdownx.caret',  # 上标和下标
    'pymdownx.superfences',  # 代码块增强，支持 mermaid.js
    'pymdownx.betterem',  # 改善粗体和斜体
    'pymdownx.mark',  # 高亮文本
    'pymdownx.highlight',  # 代码高亮
    'pymdownx.tasklist',  # 任务列表
    'pymdownx.tilde',  # 删除线
    'tables',  # 表格
]

class MarkdownToImageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Markdown 转 图片")
        self.setGeometry(100, 100, 900, 700)

        # 文本编辑器
        self.textEdit = QTextEdit(self)
        self.loadButton = QPushButton("加载 Markdown 文件", self)
        self.loadButton.clicked.connect(self.loadMarkdown)

        # 宽度设置
        self.widthSpin = QSpinBox(self)
        self.widthSpin.setRange(400, 1600)
        self.widthSpin.setValue(800)

        # 转换按钮
        self.convertButton = QPushButton("转换为图片", self)
        self.convertButton.clicked.connect(self.convertMarkdown)

        # 选择输出文件夹
        self.savePathButton = QPushButton("选择输出文件夹", self)
        self.savePathButton.clicked.connect(self.selectOutputFolder)

        # 默认输出文件夹
        self.outputFolder = os.path.join(os.getcwd(), "output")
        if not os.path.exists(self.outputFolder):
            os.makedirs(self.outputFolder)

        self.folderLabel = QLabel(self)
        self.folderLabel.setText(f"输出文件夹: {self.outputFolder}")

        # 创建带滚动条的图片显示区域
        self.imageLabel = QLabel(self)
        self.imageLabel.setScaledContents(True)  # 图片自适应标签大小

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)  # 窗口大小调整时自适应
        self.scrollArea.setWidget(self.imageLabel)

        # 布局设置
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.loadButton)
        buttonLayout.addWidget(QLabel("宽度:"))
        buttonLayout.addWidget(self.widthSpin)
        buttonLayout.addWidget(self.savePathButton)
        buttonLayout.addWidget(self.convertButton)

        layout.addLayout(buttonLayout)
        layout.addWidget(self.folderLabel)
        layout.addWidget(self.scrollArea)  # 将滚动区域添加到布局中

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
            print(f"Markdown text: {markdown_text}")
            html_content = markdown2.markdown(markdown_text, extras=extensions)

            # 加载模板文件
            with open("front_end/template1.html", "r", encoding="utf-8") as template_file:
                html_template = template_file.read()

            # 将 Markdown 渲染后的 HTML 内容插入模板
            html_template = html_template.replace("{{content}}", html_content)

            # 将新的 HTML 文件保存成临时文件，若文件已存在则覆盖
            with open("front_end/temp.html", "w", encoding="utf-8") as temp_file:
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

            output_image_path = os.path.join(self.outputFolder, "rendered.png")
            output_image_path = output_image_path.replace("\\", "/")

            print(f"Saving screenshot to: {output_image_path}")
            # print(f"temp_file: {temp_file}")

            # 执行截图
            options = {'encoding': 'utf8'}
            css = 'front_end/styles/new.css'
            imgkit.from_file('front_end/temp.html', output_image_path, options=options, css = css)

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
        aspect_ratio = 4 / 3
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
